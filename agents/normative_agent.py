"""Agente Normativo"""
from models import PSSReviewResult, NormativeFinding

def review_pss_document(pss_document: str, pmp_rules: dict = None) -> PSSReviewResult:
    findings = []
    
    if "evaluación de riesgos" not in pss_document.lower():
        findings.append(NormativeFinding(
            finding_type="Omisión",
            severity="Mayor",
            description="Falta evaluación de riesgos",
            evidence="No se encontró en el documento",
            regulation_reference="RD 1627/1997",
            recommendation="Añadir evaluación detallada"
        ))
    
    return PSSReviewResult(
        document_name="PSS Revisado",
        document_version="1.0",
        client="Cliente",
        findings=findings,
        overall_compliance="Cumple con observaciones" if len(findings) < 3 else "No cumple",
        critical_findings_count=sum(1 for f in findings if f.severity == "Crítica"),
        summary=f"Total hallazgos: {len(findings)}"
    )