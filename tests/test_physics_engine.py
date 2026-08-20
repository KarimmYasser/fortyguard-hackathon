import pytest
import math
from src.physics.transformer_thermal import TransformerThermalEngine
from src.physics.soil_cable import SoilCableEngine
from src.physics.urban_canyon import UrbanCanyonEngine
from src.physics.virtual_moisture import VirtualMoistureEngine
from src.physics.economic_model import EconomicEngine
from src.api.fortyguard_client import load_phoenix_fixture


def test_transformer_thermal_odes_and_aging():
    engine = TransformerThermalEngine()

    # Solar increment test
    solar_inc = engine.calculate_solar_increment(980.0)
    assert 1.5 <= solar_inc <= 4.0

    # Effective ambient
    t_eff = engine.effective_ambient(47.6, 980.0)
    assert t_eff > 47.6

    # Arrhenius factor: V = 1.0 at 110 °C
    v_110 = engine.arrhenius_aging_factor(110.0)
    assert pytest.approx(v_110, rel=1e-3) == 1.0

    # At 140 °C, V ~ 17.2x acceleration
    v_140 = engine.arrhenius_aging_factor(140.0)
    assert 15.0 <= v_140 <= 18.5

    # Discrete step numerical stability
    th_o, th_w, t_eff, t_o, t_hs = engine.step_discrete(
        theta_o_prev=45.0,
        theta_w_prev=20.0,
        t_ambient_2m=45.0,
        solar_irradiance_w_m2=800.0,
        load_k=1.0,
        dt_hours=1.0,
    )
    assert t_o > 45.0
    assert t_hs > t_o

    # 12-hour simulation on Phoenix fixture
    fixture = load_phoenix_fixture()
    forecast = fixture["hourly_forecast_12h"]
    trajectory = engine.simulate_trajectory("TX-04", forecast)

    assert len(trajectory.steps) == 12
    assert trajectory.peak_hot_spot_c > 130.0
    assert trajectory.total_loss_of_life_hours > 0.0


def test_soil_cable_dryout_physics():
    engine = SoilCableEngine()

    # Moisture depletion
    moisture = engine.estimate_volumetric_soil_moisture(
        initial_moisture=0.18, consecutive_heatwave_days=24
    )
    assert moisture < 0.10

    # Resistivity surge
    rho_soil = engine.calculate_soil_thermal_resistivity(moisture)
    assert rho_soil > 2.0  # surges towards 2.5 K·m/W

    # Ampacity derate
    derate = engine.compute_cable_ampacity_derate(rho_soil)
    assert derate < 0.85

    # Compound site margin
    res = engine.evaluate_compound_site_margin(
        consecutive_heatwave_days=24,
        initial_moisture=0.18,
        cable_load_k=0.95,
        transformer_top_oil_c=104.0,
        transformer_hot_spot_c=136.0,
    )
    assert "compound_site_margin_c" in res
    assert res["soil_thermal_resistivity_rho_soil"] > 2.0


def test_urban_canyon_aerodynamics():
    engine = UrbanCanyonEngine()
    kappa = engine.calculate_morphological_sheltering()
    assert 0.40 <= kappa <= 0.80

    res = engine.calculate_cooling_derate_factor(
        fortyguard_2m_ambient_c=47.6,
        reference_wind_speed_m_s=3.0,
    )
    assert "cooling_derate_eta_cool" in res
    assert res["cooling_derate_eta_cool"] < 0.85


def test_virtual_moisture_sensor():
    engine = VirtualMoistureEngine()
    w_sat = engine.oil_moisture_saturation_limit(104.0)
    assert w_sat > 50.0  # ppm solubility at 104°C

    step_res = engine.step_moisture_migration(
        paper_moisture_pct=2.5,
        oil_moisture_ppm=18.0,
        t_hot_spot_c=138.0,
        t_oil_c=104.0,
        dt_hours=1.0,
    )
    assert "relative_saturation_rs_oil" in step_res
    assert step_res["oil_moisture_ppm"] > 18.0


def test_economic_model_roi():
    engine = EconomicEngine()
    roi_eval = engine.evaluate_net_avoided_loss()

    assert roi_eval["net_avoided_loss_usd"] > 100000.0
    assert roi_eval["roi_multiple"] > 15.0
    assert roi_eval["baseline_failure_probability_pct"] > roi_eval["mitigated_failure_probability_pct"]
