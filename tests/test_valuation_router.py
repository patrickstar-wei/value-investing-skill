from scripts.routing.select_valuation_models import CompanyProfile, select_valuation_models


def test_bank_routes_to_residual_income():
    company = CompanyProfile(industry="banking", is_bank=True)
    models = select_valuation_models(company)
    assert "Residual Income" in models["primary"]


def test_compounder_routes_to_owner_earnings():
    company = CompanyProfile(industry="consumer", is_high_quality_compounder=True)
    models = select_valuation_models(company)
    assert "Owner Earnings" in models["primary"]
    assert models["base_type"] == "Mature Quality Compounder"


def test_dividend_compounder_adds_shareholder_return_overlay():
    company = CompanyProfile(
        industry="consumer staples",
        is_high_quality_compounder=True,
        shareholder_return_scores={
            "stable_dividend_history": 2,
            "reasonable_payout": 2,
            "fcf_coverage": 2,
            "buyback_or_cancellation": 1,
            "balance_sheet_support": 1,
        },
    )
    models = select_valuation_models(company)
    assert "Dividend / Shareholder Return Overlay" in models["overlays"]
    assert "Two-stage DDM" in models["overlay_models"]["dividend_models"]


def test_tech_enabled_mature_compounder_routes_to_sotp_when_material():
    company = CompanyProfile(
        industry="consumer manufacturing",
        is_high_quality_compounder=True,
        technology_optionality_scores={
            "segment_exists": 2,
            "segment_revenue_disclosed": 2,
            "above_core_growth": 1,
            "profit_path": 1,
            "roic_or_tam_expansion": 1,
        },
        has_separable_technology_segment=True,
        technology_revenue_disclosed=True,
    )
    models = select_valuation_models(company)
    assert models["base_type"] == "Tech-enabled Mature Quality Compounder"
    assert "Technology Optionality Overlay" in models["overlays"]
    assert any("SOTP" in m for m in models["overlay_models"]["technology_models"])


def test_technology_narrative_only_gets_no_separate_premium():
    company = CompanyProfile(
        industry="consumer manufacturing",
        is_high_quality_compounder=True,
        technology_optionality_scores={"segment_exists": 1},
        technology_narrative_only=True,
    )
    models = select_valuation_models(company)
    assert "Technology Narrative Only - No Separate Premium" in models["overlays"]
    assert "No separate valuation premium" in models["overlay_models"]["technology_models"]


def test_nvidia_like_company_uses_ai_semiconductor_route():
    company = CompanyProfile(
        industry="ai semiconductor",
        is_ai_semiconductor_platform=True,
    )
    models = select_valuation_models(company)
    assert models["base_type"] == "AI / Semiconductor Hypergrowth Platform"
    assert "Scenario-weighted DCF" in models["primary"]
    assert models["token_control"]["show_calculation_trace_by_default"] is False


def test_alphabet_like_company_uses_digital_platform_route():
    company = CompanyProfile(
        industry="digital advertising platform and cloud",
        is_digital_platform=True,
        cloud_platform_scores={
            "cloud_revenue_growth": 2,
            "margin_path": 2,
            "capex_intensity": 1,
            "ai_demand": 1,
        },
    )
    models = select_valuation_models(company)
    assert models["base_type"] == "Digital Platform Compounder"
    assert "Segment SOTP" in models["primary"]
    assert len(models["overlays"]) <= 2


def test_unitedhealth_like_company_uses_managed_care_route():
    company = CompanyProfile(
        industry="managed care healthcare services",
        is_managed_care=True,
    )
    models = select_valuation_models(company)
    assert models["base_type"] == "Managed Care / Healthcare Services Compounder"
    assert "Medical Loss Ratio" in models["downside"]


def test_berkshire_like_company_uses_float_holding_company_route():
    company = CompanyProfile(
        industry="insurance holding company",
        is_holding_company=True,
        is_insurance_float_allocator=True,
    )
    models = select_valuation_models(company)
    assert models["base_type"] == "Insurance Float-backed Holding Company"
    assert "look-through earnings" in models["primary"]


def test_amazon_like_company_uses_digital_platform_and_cloud_overlay():
    company = CompanyProfile(
        industry="digital platform cloud ecommerce advertising",
        is_digital_platform=True,
        cloud_platform_scores={
            "cloud_revenue_growth": 2,
            "margin_maturity": 2,
            "capex_intensity": 1,
            "ai_infrastructure": 1,
        },
    )
    models = select_valuation_models(company)
    assert models["base_type"] == "Digital Platform Compounder"
    assert "Cloud / AI Infrastructure Overlay" in models["overlays"]
    assert "cloud_models" in models["overlay_models"]


def test_token_efficiency_caps_l1_overlays():
    company = CompanyProfile(
        industry="consumer manufacturing tech dividend cyclical cloud",
        is_high_quality_compounder=True,
        shareholder_return_scores={"stable": 2, "covered": 2, "buyback": 2},
        technology_optionality_scores={"segment": 2, "revenue": 2, "growth": 2},
        cyclicality_scores={"raw_material": 2, "fx": 2},
        cloud_platform_scores={"cloud": 2, "margin": 2, "ai": 2},
        requested_depth="L1",
    )
    models = select_valuation_models(company)
    assert len(models["overlays"]) <= 2
    assert models["token_mode"] == "lazy_loaded_modular_workflow"


def test_v171_exposes_primary_workflow_and_quality_gate():
    company = CompanyProfile(industry="ai semiconductor", is_ai_semiconductor_platform=True)
    models = select_valuation_models(company)
    assert models["skill_version"] == "v17.1"
    assert models["primary_workflow"] == "workflows/04_ai_semiconductor.md"
    assert "core_quality_gate" in models
    assert "Margin of Safety" in models["core_quality_gate"]["required_final_labels"]
    assert models["token_control"]["one_primary_workflow"] is True


def test_dividend_overlay_loads_dividend_auxiliary_workflow():
    company = CompanyProfile(
        industry="consumer staples",
        is_high_quality_compounder=True,
        shareholder_return_scores={"stable": 2, "covered": 2, "buyback": 2},
    )
    models = select_valuation_models(company)
    assert "workflows/02_dividend_compounder.md" in models["auxiliary_workflows"]
    assert models["primary_workflow"] == "workflows/01_quality_company.md"
