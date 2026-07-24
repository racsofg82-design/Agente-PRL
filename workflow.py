"""Workflow Principal"""
from typing import List, Optional
from agents.risk_assessor import assess_activity
from agents.normative_agent import review_pss_document
from agents.pmp_auditor import audit_pmp_compliance
from agents.supervisor import supervise_assessment
from config import GOODMAN_PMP_RULES

def execute_prl_workflow(
    activity_name: str,
    activity_steps: List[str],
    location: str = "No especificada",
    pss_document: str = None,
    pmp_document: str = None,
    pmp_rules: dict = None
) -> dict:
    if pmp_rules is None:
        pmp_rules = GOODMAN_PMP_RULES
    
    print(f"🚀 Evaluando: {activity_name}")
    
    # 1. Evaluación de riesgos
    risk_assessment = assess_activity(activity_name, activity_steps, location, pmp_rules)
    print(f"✅ Evaluación completada: {len(risk_assessment.steps)} pasos")
    
    # 2. Revisión normativa
    normative_review = None
    if pss_document:
        normative_review = review_pss_document(pss_document, pmp_rules)
        print(f"✅ Revisión PSS: {normative_review.overall_compliance}")
    
    # 3. Auditoría PMP
    pmp_validation = audit_pmp_compliance(risk_assessment, pmp_rules, pmp_document)
    print(f"✅ PMP: {'CUMPLE' if pmp_validation.compliant else 'NO CUMPLE'} ({pmp_validation.compliance_percentage}%)")
    
    # 4. Supervisión
    final_report = supervise_assessment(activity_name, location, risk_assessment, normative_review, pmp_validation)
    
    return {
        "risk_assessment": risk_assessment,
        "normative_review": normative_review,
        "pmp_validation": pmp_validation,
        "final_report": final_report,
        "messages": ["Workflow completado exitosamente"]
    }