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


def test_v172_exposes_primary_workflow_quality_gate_and_output_contract():
    company = CompanyProfile(industry="ai semiconductor", is_ai_semiconductor_platform=True)
    models = select_valuation_models(company)
    assert models["skill_version"] == "v18"
    assert models["primary_workflow"] == "workflows/04_ai_semiconductor.md"
    assert "core_quality_gate" in models
    assert "Margin of Safety" in models["core_quality_gate"]["required_final_labels"]
    assert models["token_control"]["one_primary_workflow"] is True
    assert models["output_contract"]["valuation_range_required"] is True
    assert models["output_contract"]["position_aware_actions_required"] is True
    assert "references/valuation_rules/structured_assumption_policy.md" in models["active_route_files"]
    assert "scripts/valuation/valuation_scenario.py" in models["valuation_algorithm_files"]
    assert "scripts/valuation/valuation_reverse_dcf.py" in models["valuation_algorithm_files"]


def test_dividend_overlay_loads_dividend_auxiliary_workflow():
    company = CompanyProfile(
        industry="consumer staples",
        is_high_quality_compounder=True,
        shareholder_return_scores={"stable": 2, "covered": 2, "buyback": 2},
    )
    models = select_valuation_models(company)
    assert "workflows/02_dividend_compounder.md" in models["auxiliary_workflows"]
    assert models["primary_workflow"] == "workflows/01_quality_company.md"
    assert "scripts/valuation/valuation_ddm.py" in models["valuation_algorithm_files"]


def test_fixed_renderer_preserves_valuation_range_and_action_framework():
    from scripts.report.generate_markdown import render_report, validate_report

    payload = {
        "target_name": "Sample",
        "executive_conclusion": {
            "rating": "Watchlist",
            "style_classification": "Quality Compounder",
            "one_line_judgment": "Good business, wait for price.",
            "key_reasons": ["✅ Quality", "⚠️ Valuation", "➡️ Wait for zone"],
            "bottom_line": "Keep on watchlist."
        },
        "decision_snapshot": [{"dimension": "Action", "judgment": "Watch", "signal": "➡️"}],
        "company_classification": {
            "base_type": "Mature Quality Compounder",
            "overlays": [],
            "primary_workflow": "workflows/01_quality_company.md",
            "auxiliary_workflows": [],
            "classification_confidence": "high",
            "classification_interpretation": "Stable cash flow business."
        },
        "core_thesis": {"bull_case": ["Moat"], "bear_case": ["Valuation"]},
        "key_evidence": [{"fact": "FCF positive", "interpretation": "Cash flow supports value", "investment_implication": "Valuation range usable"}],
        "valuation_summary": {
            "selected_models": ["Owner Earnings DCF"],
            "bear_value": "80",
            "base_value": "100",
            "bull_value": "120",
            "current_price": "90",
            "margin_of_safety": "10%",
            "valuation_status": "fair",
            "key_assumptions": ["FCF stable"],
            "sensitivity_summary": "Margin sensitivity"
        },
        "risks": ["Multiple compression"],
        "execution_gate_checklist": [{"gate": "MOS", "status": "⚠️", "comment": "Not enough"}],
        "investor_action_framework": {
            "price_zones": [
                {"zone": "Deep Value", "price_range": "<=56", "interpretation": "Strong MOS"},
                {"zone": "Accumulation", "price_range": "56-85", "interpretation": "Attractive"},
                {"zone": "Watchlist", "price_range": "85-100", "interpretation": "Monitor"},
                {"zone": "Fair Value", "price_range": "100-132", "interpretation": "Fair"},
                {"zone": "Trim", "price_range": "132-156", "interpretation": "Trim"},
                {"zone": "Sell / Avoid", "price_range": ">156", "interpretation": "Avoid"}
            ],
            "position_aware_suggestions": [
                {"investor_type": "Empty Position", "suggested_action": "Wait", "rationale": "MOS limited"},
                {"investor_type": "Half Position", "suggested_action": "Hold", "rationale": "Fair"},
                {"investor_type": "Full Position", "suggested_action": "Hold", "rationale": "Quality"},
                {"investor_type": "Overweight Position", "suggested_action": "Trim if risk rises", "rationale": "Concentration"}
            ],
            "tranche_plan": {
                "starter_range": "85-100",
                "add_range": "56-85",
                "strong_add_range": "<=56",
                "hold_range": "85-132",
                "trim_range": "132-156",
                "exit_review_range": ">156"
            },
            "key_conditions": {
                "add_only_if": "Thesis intact",
                "hold_only_if": "FCF stable",
                "trim_if": "Above bull case",
                "exit_or_avoid_if": "Thesis breaks"
            }
        },
        "data_provenance": {"data_confidence": "medium", "missing_data": []}
    }

    report = render_report(payload)
    assert "Bear value" in report
    assert "Base value" in report
    assert "Bull value" in report
    assert "Position-Aware Suggestions" in report
    assert "Empty Position" in report
    assert "Overweight Position" in report
    assert validate_report(report) == []


def test_fixed_renderer_uses_chinese_when_requested():
    from scripts.report.generate_markdown import render_report, validate_report

    payload = {
        "target_name": "NVIDIA",
        "output_language": "zh-CN",
        "executive_conclusion": {
            "rating": "观察",
            "style_classification": "AI / Semiconductor Hypergrowth Platform",
            "one_line_judgment": "好公司，但需要估值纪律。",
            "key_reasons": ["业务质量高", "估值依赖 AI 增长假设", "需要反向 DCF 校验"],
            "bottom_line": "等待足够安全边际。"
        },
        "decision_snapshot": [{"dimension": "Action", "judgment": "Watch", "signal": "Review"}],
        "company_classification": {
            "base_type": "AI / Semiconductor Hypergrowth Platform",
            "overlays": [],
            "primary_workflow": "workflows/04_ai_semiconductor.md",
            "auxiliary_workflows": [],
            "classification_confidence": "high",
            "classification_interpretation": "AI 半导体平台。"
        },
        "core_thesis": {"bull_case": ["AI 需求持续"], "bear_case": ["估值过高"]},
        "key_evidence": [{"fact": "数据中心收入增长", "interpretation": "需求强", "investment_implication": "支撑增长假设"}],
        "valuation_summary": {
            "selected_models": ["Scenario-weighted DCF"],
            "bear_value": "80",
            "base_value": "100",
            "bull_value": "140",
            "current_price": "90",
            "margin_of_safety": "10%",
            "valuation_status": "fair",
            "key_assumptions": ["FCF margin stable"],
            "sensitivity_summary": "对增长和折现率敏感"
        },
        "risks": ["AI capex cycle"],
        "execution_gate_checklist": [{"gate": "MOS", "status": "Review", "comment": "有限"}],
        "investor_action_framework": {
            "price_zones": [
                {"zone": "Deep Value", "price_range": "<=56", "interpretation": "Strong MOS"}
            ],
            "position_aware_suggestions": [
                {"investor_type": "Empty Position", "suggested_action": "Wait", "rationale": "MOS limited"}
            ],
            "tranche_plan": {
                "starter_range": "85-100",
                "add_range": "56-85",
                "strong_add_range": "<=56",
                "hold_range": "85-132",
                "trim_range": "132-156",
                "exit_review_range": ">156"
            },
            "key_conditions": {
                "add_only_if": "Thesis intact",
                "hold_only_if": "FCF stable",
                "trim_if": "Above bull case",
                "exit_or_avoid_if": "Thesis breaks"
            }
        },
        "data_provenance": {"data_confidence": "medium", "missing_data": []}
    }

    report = render_report(payload)
    assert "## 执行结论" in report
    assert "## 估值摘要" in report
    assert "## 投资者行动框架" in report
    assert "Bear value" not in report
    assert validate_report(report) == []


def test_fixed_renderer_infers_chinese_from_user_request():
    from scripts.report.generate_markdown import render_report

    payload = {
        "target_name": "NVDA",
        "output_language": "auto",
        "user_request": "请用这个 skill 分析 NVDA",
        "executive_conclusion": {},
        "valuation_summary": {
            "bear_value": "Blocked",
            "base_value": "Blocked",
            "bull_value": "Blocked",
            "current_price": "Blocked",
            "margin_of_safety": "Blocked",
            "valuation_status": "blocked",
            "key_assumptions": [],
            "sensitivity_summary": "N/A"
        },
        "investor_action_framework": {
            "price_zones": [],
            "position_aware_suggestions": [],
            "tranche_plan": {},
            "key_conditions": {}
        }
    }
    report = render_report(payload)
    assert "# NVDA 投资分析" in report
    assert "## 执行结论" in report
