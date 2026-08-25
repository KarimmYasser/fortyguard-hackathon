"""
Thermal Sentinel Grid — Statistical Analytics Engine
Provides Exploratory Data Analysis (EDA), correlation analysis,
risk distribution profiling, microclimate divergence testing,
and temporal pattern analysis on the Gold feature dataset.
"""

from __future__ import annotations

import logging
import math
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger("thermal_sentinel.data_science.analytics")


# Columns that are tautological duplicates or pure linear/shift transforms of
# another Gold feature already in the dataset (e.g. hour_of_day = hour_index + 6,
# safety_margin_c = 140 - estimated_hot_spot_c). These always correlate at
# |r| == 1 by construction and would drown out genuinely interesting
# relationships in the "strongest correlations" report, so they are excluded
# from correlation analysis (they remain visible in the EDA / stats views).
_TRIVIAL_DERIVED_COLUMNS = {
    "hour_of_day",              # = hour_index + 6
    "delta_microclimate_c",     # duplicate of intra_aoi_spread_c (same formula)
    "voltage_deviation_pu",     # = 0.02 * baseline_load_ratio_k
    "safety_margin_c",          # = 140 - estimated_hot_spot_c
    "diurnal_recovery_deficit", # = estimated_top_oil_rise_c - min(estimated_top_oil_rise_c)
}

# Derivation lineage for Gold features that are CLOSED-FORM functions of other
# Gold features (see etl_pipeline._build_gold). A pair where one side is an
# ancestor of the other is a restatement of the formula, not an empirical
# finding: estimated_winding_gradient_c = 23 * K**0.8 is monotone in K, so it
# reports r ~ +1.000 / rho = +1.000 forever, on any dataset, by algebra.
# Such pairs stay in the matrix but are ranked separately from real findings.
_DERIVED_FROM: Dict[str, set] = {
    "rolling_3h_avg_ambient": {"fortyguard_2m_ambient_c"},
    "cumulative_degree_hours_above_40": {"fortyguard_2m_ambient_c"},
    "thermal_soak_index_derived": {"cumulative_degree_hours_above_40", "hour_index"},
    "estimated_top_oil_rise_c": {"baseline_load_ratio_k", "cooling_derate_eta_cool"},
    "estimated_winding_gradient_c": {"baseline_load_ratio_k"},
    "estimated_hot_spot_c": {
        "fortyguard_2m_ambient_c",
        "estimated_top_oil_rise_c",
        "estimated_winding_gradient_c",
    },
    "aging_factor_v": {"estimated_hot_spot_c"},
    "bess_soc_gradient": {"bess_soc_pct"},
    "intra_aoi_spread_c": {"fortyguard_2m_ambient_c", "coolest_tile_2m_c"},
}

# Pairs that are not formula-linked but are co-authored by the same scenario
# curve (one hand-written ramp scaled two ways), or are two measurements of the
# same physical field. Their correlation describes the fixture, not the grid.
_STRUCTURAL_PAIRS = {
    frozenset({"baseline_load_ratio_k", "hospital_critical_load_mw"}),
    frozenset({"fortyguard_2m_ambient_c", "coolest_tile_2m_c"}),
}


def _alias_class(col: str) -> frozenset:
    """
    Features linked by _STRUCTURAL_PAIRS are near-perfect proxies for each other
    (r > 0.999), so a relationship involving one is the same relationship for the
    other. Collapse them into an equivalence class before checking lineage --
    otherwise hospital_critical_load_mw silently launders every tautology that
    baseline_load_ratio_k has.
    """
    cls = {col}
    changed = True
    while changed:
        changed = False
        for pair in _STRUCTURAL_PAIRS:
            if cls & pair and not pair <= cls:
                cls |= set(pair)
                changed = True
    return frozenset(cls)


def _ancestors(col: str, _seen: set | None = None) -> set:
    """Transitive closure of _DERIVED_FROM, widened by structural aliases."""
    _seen = set() if _seen is None else _seen
    out = set()
    for alias in _alias_class(col):
        for parent in _DERIVED_FROM.get(alias, ()):
            if parent in _seen:
                continue
            _seen.add(parent)
            out |= _alias_class(parent)
            out |= _ancestors(parent, _seen)
    return out


def _pair_kind(a: str, b: str) -> str:
    """'derived' | 'structural' | 'empirical' for a feature pair."""
    cls_a, cls_b = _alias_class(a), _alias_class(b)
    anc_a, anc_b = _ancestors(a), _ancestors(b)

    # one side is computed from the other (or from the other's proxy)
    if cls_b & anc_a or cls_a & anc_b:
        return "derived"
    # siblings: both computed from a shared ancestor
    if anc_a & anc_b:
        return "derived"
    if cls_a & cls_b:
        return "structural"
    return "empirical"


def _pearson_p_value(r: float, n: int) -> float | None:
    """Two-sided p-value for a Pearson r via the t approximation."""
    if n < 3 or abs(r) >= 1.0:
        return 0.0 if abs(r) >= 1.0 and n >= 3 else None
    dof = n - 2
    t = abs(r) * math.sqrt(dof / (1.0 - r * r))
    # Regularised incomplete beta via continued fraction is overkill here;
    # use the survival function of Student-t through its beta relation.
    x = dof / (dof + t * t)
    p = _betainc_half(0.5 * dof, x)
    p = min(max(p, 0.0), 1.0)
    # 3 significant figures, so p = 1.8e-07 does not round away to 0.0
    return float(f"{p:.3g}")


def _betainc_half(a: float, x: float) -> float:
    """I_x(a, 0.5) — regularised incomplete beta, series form, enough for p-values."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    b = 0.5
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(a * math.log(x) + b * math.log(1.0 - x) - lbeta) / a
    # Lentz continued fraction
    f, c, d = 1.0, 1.0, 0.0
    for i in range(0, 300):
        m = i // 2
        if i == 0:
            num = 1.0
        elif i % 2 == 0:
            num = (m * (b - m) * x) / ((a + 2 * m - 1) * (a + 2 * m))
        else:
            num = -((a + m) * (a + b + m) * x) / ((a + 2 * m) * (a + 2 * m + 1))
        d = 1.0 + num * d
        d = 1e-30 if abs(d) < 1e-30 else d
        d = 1.0 / d
        c = 1.0 + num / (c if abs(c) > 1e-30 else 1e-30)
        delta = c * d
        f *= delta
        if abs(1.0 - delta) < 1e-10:
            break
    return front * (f - 1.0)


class ThermalAnalyticsEngine:
    """
    Statistical analytics engine operating on Gold ETL features.
    """

    def compute_eda_summary(self, gold_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Full exploratory data analysis: descriptive stats, distribution shapes,
        skewness, kurtosis, and null percentages per column.
        """
        if gold_df.empty:
            return {"error": "Empty dataset"}

        numeric_df = gold_df.select_dtypes(include=[np.number])

        features: List[Dict[str, Any]] = []
        for col in numeric_df.columns:
            series = numeric_df[col]
            features.append({
                "feature": col,
                "count": int(series.count()),
                "mean": round(float(series.mean()), 4),
                "std": round(float(series.std()), 4),
                "min": round(float(series.min()), 4),
                "q1": round(float(series.quantile(0.25)), 4),
                "median": round(float(series.median()), 4),
                "q3": round(float(series.quantile(0.75)), 4),
                "max": round(float(series.max()), 4),
                "skewness": round(float(series.skew()), 4),
                "kurtosis": round(float(series.kurtosis()), 4),
                "null_pct": round(float(series.isna().mean() * 100), 2),
            })

        return {
            "total_records": len(gold_df),
            "total_features": len(gold_df.columns),
            "numeric_features": len(numeric_df.columns),
            "categorical_features": len(gold_df.select_dtypes(include=["category", "object", "string", "str"]).columns),
            "overall_null_pct": round(float(gold_df.isna().mean().mean() * 100), 2),
            "feature_statistics": features,
        }

    def compute_correlation_analysis(self, gold_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Pearson & Spearman correlation matrices with top-10 strongest pairs.
        """
        if gold_df.empty:
            return {"error": "Empty dataset"}

        numeric_df = gold_df.select_dtypes(include=[np.number])
        # Filter for columns that actually vary across observations, and drop
        # tautological/derived duplicates that would otherwise dominate the
        # "strongest correlations" report with meaningless |r| == 1 pairs.
        varying_cols = [
            c for c in numeric_df.columns
            if numeric_df[c].std() > 1e-8 and c not in _TRIVIAL_DERIVED_COLUMNS
        ]
        if not varying_cols:
            varying_cols = [c for c in numeric_df.columns if numeric_df[c].std() > 1e-8] or numeric_df.columns.tolist()

        sub_df = numeric_df[varying_cols]
        columns = varying_cols

        pearson_corr = sub_df.corr(method="pearson").fillna(0.0)
        spearman_corr = sub_df.corr(method="spearman").fillna(0.0)

        n_obs = int(len(sub_df))

        # Extract Pearson pairs, tagged by provenance
        pairs = []
        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                p_r = float(pearson_corr.iloc[i, j])
                s_rho = float(spearman_corr.iloc[i, j])
                if np.isnan(p_r):
                    continue
                pairs.append({
                    "feature_a": columns[i],
                    "feature_b": columns[j],
                    "pearson_r": round(p_r, 4),
                    "spearman_rho": round(s_rho, 4),
                    "kind": _pair_kind(columns[i], columns[j]),
                    "p_value": _pearson_p_value(p_r, n_obs),
                })

        by_strength = sorted(pairs, key=lambda x: abs(x["pearson_r"]), reverse=True)
        empirical = [p for p in by_strength if p["kind"] == "empirical"]
        tautological = [p for p in by_strength if p["kind"] != "empirical"]

        warnings: List[str] = []
        if n_obs < 30:
            warnings.append(
                f"n = {n_obs} observations. Correlations on this few points are "
                "unstable; treat |r| as directional only."
            )
        if tautological:
            warnings.append(
                f"{len(tautological)} pair(s) are derived or co-authored by construction "
                "and are ranked separately from empirical findings."
            )

        return {
            "columns": columns,
            "n_observations": n_obs,
            "pearson_matrix": pearson_corr.round(4).values.tolist(),
            "spearman_matrix": spearman_corr.round(4).values.tolist(),
            # Headline list now contains only relationships that could have
            # come out otherwise. Formula-linked pairs are shown, but boxed off.
            "top_10_strongest_pairs": empirical[:10],
            "tautological_pairs": tautological[:10],
            "top_5_positive": [p for p in empirical if p["pearson_r"] > 0][:5],
            "top_5_negative": [p for p in empirical if p["pearson_r"] < 0][:5],
            "warnings": warnings,
        }

    def compute_risk_distribution(self, gold_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Classify hourly transformer states into risk tiers based on T_hs thresholds.
        """
        if "risk_tier" not in gold_df.columns and "estimated_hot_spot_c" not in gold_df.columns:
            return {"error": "No hot-spot data available"}

        if "risk_tier" in gold_df.columns:
            tier_col = gold_df["risk_tier"]
        else:
            conditions = [
                gold_df["estimated_hot_spot_c"] >= 140,
                gold_df["estimated_hot_spot_c"] >= 120,
                gold_df["estimated_hot_spot_c"] >= 100,
            ]
            choices = ["CRITICAL", "HIGH", "MODERATE"]
            tier_col = pd.Series(np.select(conditions, choices, default="LOW"))

        total = len(tier_col)
        counts = tier_col.value_counts().to_dict()

        tiers = []
        for tier_name in ["LOW", "MODERATE", "HIGH", "CRITICAL"]:
            count = counts.get(tier_name, 0)
            tiers.append({
                "tier": tier_name,
                "count": int(count),
                "percentage": round(100 * count / max(total, 1), 2),
            })

        return {
            "total_records": total,
            "risk_tiers": tiers,
            "dominant_tier": max(tiers, key=lambda x: x["count"])["tier"],
        }

    def compute_microclimate_divergence(self, gold_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Paired comparison between the hottest and coolest 2m tile inside the AOI.

        The second series is the coolest measured tile, NOT an airport station -
        we probed Sky Harbor and it reads warmer than downtown. The labels here
        used to say "airport" long after the column was renamed.
        """
        if "fortyguard_2m_ambient_c" not in gold_df.columns or "coolest_tile_2m_c" not in gold_df.columns:
            return {"error": "Temperature comparison columns not available"}

        fg = gold_df["fortyguard_2m_ambient_c"].values
        ap = gold_df["coolest_tile_2m_c"].values
        delta = fg - ap

        # Analytical Paired t-test
        n = len(delta)
        mean_d = float(np.mean(delta))
        std_d = float(np.std(delta, ddof=1)) if n > 1 else 1e-8
        se_d = std_d / math.sqrt(n) if n > 0 else 1e-8
        t_stat = mean_d / max(se_d, 1e-8)
        
        # Approximate 2-tailed p-value from t-stat and degrees of freedom
        df = max(n - 1, 1)
        # Using accurate regularized incomplete beta / standard normal approximation for t-stat
        p_value = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t_stat) / math.sqrt(2.0))))

        # Cohen's d (effect size)
        pooled_std = np.sqrt((np.std(fg, ddof=1)**2 + np.std(ap, ddof=1)**2) / 2)
        cohens_d = float(np.mean(delta) / max(pooled_std, 1e-8))

        # Effect size interpretation
        if abs(cohens_d) >= 0.8:
            effect_label = "LARGE"
        elif abs(cohens_d) >= 0.5:
            effect_label = "MEDIUM"
        elif abs(cohens_d) >= 0.2:
            effect_label = "SMALL"
        else:
            effect_label = "NEGLIGIBLE"

        return {
            "test_name": "Paired t-test: hottest vs coolest 2m tile within the AOI",
            "fortyguard_mean_c": round(float(np.mean(fg)), 2),
            "coolest_tile_mean_c": round(float(np.mean(ap)), 2),
            "mean_delta_c": round(float(np.mean(delta)), 2),
            "max_delta_c": round(float(np.max(delta)), 2),
            "t_statistic": round(float(t_stat), 4),
            "p_value": float(p_value),
            "is_significant": bool(p_value < 0.05),
            "cohens_d": round(cohens_d, 4),
            "effect_size": effect_label,
            # Report significance and effect size separately. A p-value this
            # small on n=12 says the sign of the difference is reliable; it
            # says nothing about whether the difference matters. Claiming a
            # "confirmed heat trap" next to a NEGLIGIBLE Cohen's d was the
            # textbook significance-vs-effect-size error.
            "interpretation": (
                f"The hottest tile runs +{mean_d:.2f}°C above the coolest tile in the same AOI "
                f"(paired t={t_stat:.2f}, p={p_value:.2e}). The difference is statistically "
                f"reliable but the effect size is {effect_label.lower()} (Cohen's d={cohens_d:.3f}), "
                f"so intra-AOI spread is not the driver here - the sustained duration above 40°C is."
                if abs(cohens_d) < 0.5 else
                f"The hottest tile runs +{mean_d:.2f}°C above the coolest tile in the same AOI "
                f"(paired t={t_stat:.2f}, p={p_value:.2e}, Cohen's d={cohens_d:.3f} [{effect_label}]), "
                f"a materially significant microclimate divergence."
            ),
            "hourly_deltas": [round(float(d), 2) for d in delta],
        }

    def compute_temporal_patterns(self, gold_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Hourly aggregation revealing peak risk windows and diurnal recovery cycles.
        """
        if gold_df.empty:
            return {"error": "Empty dataset"}

        agg_cols = {}
        if "estimated_hot_spot_c" in gold_df.columns:
            agg_cols["estimated_hot_spot_c"] = "mean"
        if "aging_factor_v" in gold_df.columns:
            agg_cols["aging_factor_v"] = "mean"
        if "bess_soc_pct" in gold_df.columns:
            agg_cols["bess_soc_pct"] = "mean"
        if "fortyguard_2m_ambient_c" in gold_df.columns:
            agg_cols["fortyguard_2m_ambient_c"] = "mean"
        if "safety_margin_c" in gold_df.columns:
            agg_cols["safety_margin_c"] = "mean"
        if "baseline_load_ratio_k" in gold_df.columns:
            agg_cols["baseline_load_ratio_k"] = "mean"

        if not agg_cols:
            return {"error": "No aggregatable columns found"}

        # Since we have 12 hourly records, each row is already 1 hour
        hourly_records = []
        for _, row in gold_df.iterrows():
            record: Dict[str, Any] = {
                "hour_index": int(row.get("hour_index", 0)),
                "time_label": str(row.get("time_label", "")),
                "hour_of_day": int(row.get("hour_of_day", row.get("hour_index", 0) + 6)),
            }
            for col in agg_cols:
                if col in row.index:
                    record[col] = round(float(row[col]), 2)
            hourly_records.append(record)

        # Identify peak risk hour
        if "estimated_hot_spot_c" in gold_df.columns:
            peak_idx = int(gold_df["estimated_hot_spot_c"].idxmax())
            peak_hour = gold_df.iloc[peak_idx]
            peak_info = {
                "peak_hour_index": int(peak_hour.get("hour_index", peak_idx)),
                "peak_time_label": str(peak_hour.get("time_label", "")),
                "peak_hot_spot_c": round(float(peak_hour["estimated_hot_spot_c"]), 2),
                "peak_aging_factor": round(float(peak_hour.get("aging_factor_v", 0)), 2),
            }
        else:
            peak_info = {}

        return {
            "total_hours": len(hourly_records),
            "hourly_records": hourly_records,
            "peak_risk_window": peak_info,
            "analysis_period": {
                "start": str(gold_df.iloc[0].get("time_label", "06:00 AM")) if len(gold_df) > 0 else "",
                "end": str(gold_df.iloc[-1].get("time_label", "05:00 PM")) if len(gold_df) > 0 else "",
            },
        }

    def compute_spatial_correlations(self, custom_parcels: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Compute empirical bivariate regressions and Global Moran's I spatial autocorrelation
        across urban land-cover morphology (canopy, asphalt, canyon aspect) and microclimate metrics.
        """
        from .spatial_correlation import SpatialCorrelationEngine
        return SpatialCorrelationEngine.get_full_spatial_correlation_suite(custom_parcels)

