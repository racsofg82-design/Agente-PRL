"""Motor del Agente PRL (Lógica unificada)"""
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from config import GOODMAN_PMP_RULES, SPANISH_REGULATIONS, NTP_CATALOG, BASE_SYSTEM_PROMPT, PMPRule
from models import (
    RiskAssessmentResult, ActivityStep, IdentifiedHazard, HazardType, RiskLevel,
    PMPComplianceCheck, PSSReviewResult, NormativeFinding
)
import json
import re

def get_risk_class(level: int) -> RiskLevel:
    if level <= 3: return RiskLevel.LOW
    if level <= 6: return RiskLevel.MEDIUM
    if level <= 12: return RiskLevel.HIGH
    return RiskLevel.CRITICAL

def check_pmp_compliance(measures: List[str], pmp_rules: Dict[str, PMPRule]) -> PMPComplianceCheck:
    text = " ".join(measures).lower()
    missing = []
    compliant_count = 0
    total = len(pmp_rules)
    
    for rule in pmp_rules.values():
        found = any(kw.lower() in text for kw in rule.keywords)
        if found:
            compliant_count += 1
        elif rule.mandatory:
            missing.append(f"{rule.description} (Ref: {rule.technical_reference})")
            
    pct = (compliant_count / total * 100) if total > 0 else 100
    return PMPComplianceCheck(compliant=len(missing)==0, missing_requirements=missing, compliance_percentage=pct)

def assess_activity(name: str, steps: List[str], location: str, pmp_rules: Dict[str, PMPRule]) -> RiskAssessmentResult:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2) # Usamos gpt-4o-mini por velocidad y coste
    
    ntps_text = ", ".join(NTP_CATALOG.get("trabajos_altura", []))
    rules_text = "\n".join([f"- {r.description} (Ref: {r.technical_reference})" for r in pmp_rules.values()])
    
    prompt = BASE_SYSTEM_PROMPT.format(
        regulations="\n".join(SPANISH_REGULATIONS),
        ntps=ntps_text,
        pmp_rules=rules_text
    )
    
    user_msg = f"""
    Actividad: {name} en {location}.
    Pasos: {json.dumps(steps, ensure_ascii=False)}
    
    Devuelve SOLO un JSON válido con esta estructura exacta, sin markdown:
    {{
      "steps": [
        {{
          "step_number": 1,
          "description": "Paso 1",
          "hazards": [
            {{
              "description": "Peligro",
              "hazard_type": "Mecánico|Eléctrico|Químico|Altura|Tráfico|Otro",
              "probability": 3,
              "severity": 4,
              "justification": "Razón técnica",
              "control_measures": ["Medida 1", "Medida 2"]
            }}
          ]
        }}
      ]
    }}
    """
    
    try:
        response = llm.invoke([SystemMessage(content=prompt), HumanMessage(content=user_msg)])
        # Limpiar respuesta por si el LLM añade ```json
        clean_text = re.sub(r'^```json\s*|\s*```$', '', response.content.strip(), flags=re.MULTILINE)
        data = json.loads(clean_text)
        
        eval_steps = []
        all_measures = []
        critical_count = 0
        
        for s in data.get("steps", []):
            hazards = []
            for h in s.get("hazards", []):
                p = max(1, min(5, int(h.get("probability", 3))))
                sev = max(1, min(5, int(h.get("severity", 3))))
                level = p * sev
                cls = get_risk_class(level)
                
                h_type = h.get("hazard_type", "Otro")
                if h_type not in HazardType.__members__: h_type = "OTRO"
                
                hazards.append(IdentifiedHazard(
                    description=h["description"],
                    hazard_type=HazardType(h_type),
                    probability=p, severity=sev, risk_level=level, classification=cls,
                    justification=h.get("justification", ""),
                    control_measures=h.get("control_measures", [])
                ))
                all_measures.extend(h.get("control_measures", []))
                if cls == RiskLevel.CRITICAL: critical_count += 1
                
            eval_steps.append(ActivityStep(step_number=s["step_number"], description=s["description"], hazards=hazards))
            
        pmp_check = check_pmp_compliance(all_measures, pmp_rules)
        recs = []
        if critical_count > 0: recs.append(f"⚠️ {critical_count} riesgos CRÍTICOS. Revisar método.")
        if not pmp_check.compliant: recs.append(f"❌ Faltan requisitos PMP: {', '.join(pmp_check.missing_requirements[:2])}")
        recs.append("📢 Realizar Toolbox Talk antes de iniciar.")
        
        return RiskAssessmentResult(
            activity_name=name, location=location, steps=eval_steps,
            pmp_compliance=pmp_check,
            overall_risk_level=RiskLevel.CRITICAL if critical_count > 0 else RiskLevel.HIGH,
            critical_hazards_count=critical_count, recommendations=recs
        )
    except Exception as e:
        # Fallback si falla el LLM
        return RiskAssessmentResult(
            activity_name=name, location=location,
            overall_risk_level=RiskLevel.HIGH,
            recommendations=[f"⚠️ Error en el análisis automático: {str(e)}. Revisar manualmente."]
        )

def review_pss(pss_text: str, pmp_rules: Dict[str, PMPRule]) -> PSSReviewResult:
    findings = []
    if "evaluación de riesgos" not in pss_text.lower():
        findings.append(NormativeFinding(severity="Mayor", description="Falta evaluación de riesgos", recommendation="Añadir evaluación detallada"))
    return PSSReviewResult(
        overall_compliance="Cumple con observaciones" if len(findings) < 2 else "No cumple",
        findings=findings
    )

def execute_prl_workflow(name: str, steps: List[str], location: str, pss_text: str = None, pmp_rules: Dict[str, PMPRule] = None):
    if pmp_rules is None: pmp_rules = GOODMAN_PMP_RULES
    
    risk_res = assess_activity(name, steps, location, pmp_rules)
    norm_res = review_pss(pss_text, pmp_rules) if pss_text else None
    
    return {
        "risk_assessment": risk_res,
        "normative_review": norm_res,
        "pmp_validation": risk_res.pmp_compliance,
        "final_report": {
            "executive_summary": f"✅ Evaluación de '{name}' completada. Riesgos críticos: {risk_res.critical_hazards_count}. PMP: {risk_res.pmp_compliance.compliance_percentage}%",
            "recommendations": risk_res.recommendations
        }
    }
