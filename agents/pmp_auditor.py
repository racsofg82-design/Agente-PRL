"""Auditor PMP"""
from models import RiskAssessmentResult, PMPComplianceCheck
from tools.pmp_validator import check_pmp_compliance

def audit_pmp_compliance(
    risk_assessment: RiskAssessmentResult,
    pmp_rules: dict = None,
    pmp_document_text: str = None
) -> PMPComplianceCheck:
    all_measures = []
    for step in risk_assessment.steps:
        for hazard in step.hazards:
            all_measures.extend(hazard.control_measures)
    
    return check_pmp_compliance("all", all_measures, pmp_rules or {})