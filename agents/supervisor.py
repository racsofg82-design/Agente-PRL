"""Agente Supervisor"""
from models import RiskAssessmentResult, PSSReviewResult, PMPComplianceCheck
from datetime import datetime

def supervise_assessment(
    activity_name: str,
    location: str,
    risk_assessment: RiskAssessmentResult = None,
    normative_review: PSSReviewResult = None,
    pmp_validation: PMPComplianceCheck = None
) -> dict:
    recommendations = []
    
    if risk_assessment and risk_assessment.critical_hazards_count > 0:
        recommendations.append(f"⚠️ {risk_assessment.critical_hazards_count} riesgo(s) crítico(s) requieren aprobación")
    
    if pmp_validation and not pmp_validation.compliant:
        recommendations.append(f"❌ Incumplimiento PMP: {', '.join(pmp_validation.missing_requirements[:2])}")
    
    recommendations.append("📢 Realizar toolbox talk antes de iniciar")
    
    approval_required = (
        (risk_assessment and risk_assessment.critical_hazards_count > 0) or
        (pmp_validation and not pmp_validation.compliant)
    )
    
    summary = f"""
================================================================================
INFORME DE EVALUACIÓN - {activity_name}
================================================================================
Actividad: {activity_name}
Lugar: {location}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Riesgos críticos: {risk_assessment.critical_hazards_count if risk_assessment else 0}
Cumplimiento PMP: {pmp_validation.compliance_percentage if pmp_validation else 'N/A'}%

APROBACIÓN: {'REQUERIDA ✅' if approval_required else 'NO REQUERIDA'}
================================================================================
"""
    
    return {
        "executive_summary": summary,
        "recommendations": recommendations,
        "approval_required": approval_required,
        "risk_assessment": risk_assessment,
        "normative_review": normative_review,
        "pmp_validation": pmp_validation
    }