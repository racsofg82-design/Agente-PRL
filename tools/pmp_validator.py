"""Validador PMP"""
from models import PMPComplianceCheck
from config import GOODMAN_PMP_RULES, PMPRule

def check_pmp_compliance(
    activity_type: str,
    measures: list,
    pmp_rules: dict = None
) -> PMPComplianceCheck:
    if pmp_rules is None:
        pmp_rules = GOODMAN_PMP_RULES
    
    measures_text = " ".join(measures).lower()
    missing = []
    observations = []
    compliant_count = 0
    
    for rule_id, rule in pmp_rules.items():
        if rule.category == activity_type or activity_type == "all":
            found = any(kw.lower() in measures_text for kw in rule.keywords)
            if found:
                compliant_count += 1
            else:
                if rule.mandatory:
                    missing.append(rule.description)
    
    total_rules = len([r for r in pmp_rules.values() if r.category == activity_type or activity_type == "all"])
    compliance_percentage = (compliant_count / total_rules * 100) if total_rules > 0 else 100.0
    
    return PMPComplianceCheck(
        compliant=len(missing) == 0,
        missing_requirements=missing,
        observations=observations,
        compliance_percentage=round(compliance_percentage, 2)
    )