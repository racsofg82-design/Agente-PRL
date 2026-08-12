"""
Workflow Principal - Versión Profesional
Con validación técnica rigurosa y manejo de errores
"""
from typing import List, Optional, Dict, Any
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
    pmp_rules: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Ejecuta el flujo de trabajo PRL con validación técnica rigurosa"""
    if pmp_rules is None:
        pmp_rules = GOODMAN_PMP_RULES
    
    print(f"\n🚀 INICIANDO EVALUACIÓN TÉCNICA: {activity_name}")
    print(f"📍 Lugar: {location}")
    print(f"📋 Pasos: {len(activity_steps)}")
    
    # 1. Evaluación de riesgos (con análisis técnico riguroso)
    print("\n🔍 PASO 1: Evaluación de riesgos técnicos")
    risk_assessment = assess_activity(
        activity_name=activity_name,
        activity_steps=activity_steps,
        location=location,
        pmp_rules=pmp_rules
    )
    
    # 2. Revisión normativa (si hay PSS)
    normative_review = None
    if pss_document:
        print("\n📋 PASO 2: Revisión normativa del PSS/RAMS")
        normative_review = review_pss_document(
            pss_document=pss_document,
            pmp_rules=pmp_rules
        )
    
    # 3. Auditoría PMP (con lógica técnica avanzada)
    print("\n✅ PASO 3: Auditoría PMP con lógica técnica")
    pmp_validation = audit_pmp_compliance(
        risk_assessment=risk_assessment,
        pmp_rules=pmp_rules,
        pmp_document_text=pmp_document
    )
    
    # 4. Supervisión (con validación técnica)
    print("\n🔍 PASO 4: Supervisión técnica final")
    final_report = supervise_assessment(
        activity_name=activity_name,
        location=location,
        risk_assessment=risk_assessment,
        normative_review=normative_review,
        pmp_validation=pmp_validation
    )
    
    # 5. Generar informe técnico
    print("\n📊 PASO 5: Generando informe técnico")
    technical_report = _generate_technical_report(
        risk_assessment,
        normative_review,
        pmp_validation
    )
    
    print("\n✅ EVALUACIÓN TÉCNICA COMPLETADA")
    
    return {
        "risk_assessment": risk_assessment,
        "normative_review": normative_review,
        "pmp_validation": pmp_validation,
        "final_report": final_report,
        "technical_report": technical_report,
        "messages": [
            "Evaluación técnica completada con éxito",
            f"Riesgos críticos: {risk_assessment.critical_hazards_count}",
            f"Cumplimiento PMP: {pmp_validation.compliance_percentage}%"
        ]
    }

def _generate_technical_report(
    risk_assessment: RiskAssessmentResult,
    normative_review: Optional[PSSReviewResult],
    pmp_validation: PMPComplianceCheck
) -> str:
    """Genera un informe técnico detallado"""
    report = [
        "=" * 80,
        "INFORME TÉCNICO DE EVALUACIÓN DE RIESGOS",
        "=" * 80,
        f"Actividad: {risk_assessment.activity_name}",
        f"Lugar: {risk_assessment.location}",
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "=" * 80,
        "\n📋 RESUMEN EJECUTIVO:",
        f"- Nivel de riesgo global: {risk_assessment.overall_risk_level.value}",
        f"- Riesgos críticos: {risk_assessment.critical_hazards_count}",
        f"- Cumplimiento PMP: {pmp_validation.compliance_percentage}%",
        f"- Hallazgos normativos: {normative_review.overall_compliance if normative_review else 'N/A'}",
        "=" * 80,
        "\n🔍 ANÁLISIS DETALLADO:",
    ]
    
    # Análisis de riesgos
    report.append("\n1. ANÁLISIS DE RIESGOS:")
    for step in risk_assessment.steps:
        report.append(f"\nPaso {step.step_number}: {step.description}")
        for hazard in step.hazards:
            report.append(f"\n   • {hazard.description}")
            report.append(f"     Nivel: {hazard.risk_level} ({hazard.classification.value})")
            report.append(f"     Probabilidad: {hazard.probability} - {RISK_MATRIX_RULES['probability'][f'{hazard.probability} - {RISK_MATRIX_RULES['probability'][f'{hazard.probability}']}']")
            report.append(f"     Severidad: {hazard.severity} - {RISK_MATRIX_RULES['severity'][f'{hazard.severity} - {RISK_MATRIX_RULES['severity'][f'{hazard.severity}']}']}")
            report.append(f"     Justificación: {hazard.justification_probability} | {hazard.justification_severity}")
            report.append(f"     Medidas: {', '.join(hazard.control_measures)}")
    
    # Validación PMP
    report.append("\n2. VALIDACIÓN PMP:")
    if pmp_validation.missing_requirements:
        report.append("   ❌ Requisitos faltantes:")
        for req in pmp_validation.missing_requirements:
            report.append(f"      - {req}")
    else:
        report.append("   ✅ Cumple con todos los requisitos del PMP")
    
    # Hallazgos normativos
    if normative_review:
        report.append("\n3. HALLAZGOS NORMATIVOS:")
        for finding in normative_review.findings:
            report.append(f"   [{finding.severity}] {finding.finding_type}")
            report.append(f"      {finding.description}")
            report.append(f"      Referencia: {finding.regulation_reference}")
    
    # Recomendaciones
    report.append("\n4. RECOMENDACIONES TÉCNICAS:")
    for rec in risk_assessment.recommendations:
        report.append(f"   - {rec}")
    
    report.append("\n5. ACCIONES RECOMENDADAS:")
    if risk_assessment.critical_hazards_count > 0:
        report.append("   ⚠️ Revisar el método de trabajo antes de iniciar")
    if not pmp_validation.compliant:
        report.append("   ⚠️ Corregir incumplimientos del PMP")
    report.append("   📢 Realizar toolbox talk con todos los trabajadores")
    report.append("   👷 Verificar formación del personal")
    
    report.append("\n" + "=" * 80)
    report.append("INFORME TÉCNICO GENERADO AUTOMÁTICAMENTE")
    report.append("=" * 80)
    
    return "\n".join(report)
