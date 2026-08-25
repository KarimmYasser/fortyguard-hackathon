"""Unit tests for Commercial Early Adopter Archetypes & COCO Customer Discovery Framework."""

import pytest
from src.models.commercial_presets import (
    COMMERCIAL_ARCHETYPES_CATALOG,
    CommercialArchetype,
    COCOExecutiveBrief,
)
from src.operations.portfolio import generate_coco_executive_brief


def test_commercial_archetypes_catalog_integrity():
    """Verify that all 4 commercial archetypes are present and have complete physical/economic parameters."""
    expected_sectors = ["SOLAR_FARM", "DATA_CENTER", "HOSPITAL_FEEDER", "UTILITY_SUBSTATION"]
    assert set(expected_sectors).issubset(set(COMMERCIAL_ARCHETYPES_CATALOG.keys()))
    
    for sector_id, arch in COMMERCIAL_ARCHETYPES_CATALOG.items():
        assert isinstance(arch, CommercialArchetype)
        assert arch.nameplate_capacity_mva > 0
        assert arch.critical_thermal_ceiling_c >= 45.0
        assert arch.bess_capacity_mwh > 0
        assert arch.voll_rate_per_kwh > 0
        assert arch.monthly_saas_tier_usd > 0
        assert arch.roi_multiplier > 50.0
        assert len(arch.coco_context) > 20
        assert len(arch.coco_outcomes) > 20
        assert len(arch.coco_constraints) > 20
        assert len(arch.coco_options) > 20


def test_generate_coco_executive_brief_solar_farm():
    """Verify COCO brief generation for a Solar Farm operator."""
    brief_dict = generate_coco_executive_brief(
        sector_id="SOLAR_FARM",
        prepared_for="NextEra Sunbelt Solar IPP",
    )
    
    assert brief_dict["buyer_persona"] is not None
    assert "Solar" in brief_dict["target_sector"]
    assert brief_dict["total_nameplate_mva"] == 200.0  # 8 * 25 MVA
    assert brief_dict["net_customer_roi_multiplier"] > 20.0
    assert brief_dict["payback_period_days"] < 30.0  # Under 30 days payback
    assert "NextEra Sunbelt Solar IPP" in brief_dict["executive_recommendation"]


def test_generate_coco_executive_brief_data_center():
    """Verify COCO brief generation for an AI Data Center operator."""
    brief_dict = generate_coco_executive_brief(
        sector_id="DATA_CENTER",
        prepared_for="Equinix Hyperscale Cluster Phoenix",
    )
    
    assert "Data Center" in brief_dict["target_sector"]
    assert brief_dict["gross_avoided_outage_loss_usd"] > 1000000.0
    assert brief_dict["net_customer_roi_multiplier"] > 30.0
