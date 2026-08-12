"""
Motor del Agente PRL Senior - Con Biblioteca INSST Integrada
Analiza procedimientos citando NTPs y normativa específica
"""
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from config import (
    GOODMAN_PMP_RULES, SPANISH_REGULATIONS, NTP_CATALOG, 
    BASE_SYSTEM_PROMPT, PMPRule, find_relevant_ntps
)
from models import (
    RiskAssessmentResult, ActivityStep, IdentifiedHazard, HazardType, RiskLevel,
    PMPComplianceCheck
)
import json
import re

def get_risk_class(level: int) -> RiskLevel:
    if level <= 3: return RiskLevel.LOW
    if level <= 6: return RiskLevel.MEDIUM
    if level <= 12: return RiskLevel.HIGH
    return RiskLevel.CRITICAL

def clean_json_response(text: str) -> str:
    text = text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return text

def analyze_procedure_with_normative(
    procedure_text: str, 
    pss_text: str, 
    pmp_text: str,
    pmp_rules: Dict[str, PMPRule]
) -> RiskAssessmentResult:
    """
    Analiza el procedimiento integrando NTPs y normativa específica
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    
    # PASO 1: Identificar NTPs y normativa relevante según el contenido
    relevant_normative = find_relevant_ntps(procedure_text)
    
    # Construir contexto normativo enriquecido
    normative_context = ""
    if relevant_normative["ntps"]:
        normative_context += "NTPs APLICABLES A ESTA ACTIVIDAD:\n"
        for ntp in relevant_normative["ntps"]:
            normative_context += f"  • {ntp}\n"
        normative_context += "\n"
    
    if relevant_normative["regulations"]:
        normative_context += "NORMATIVA ESPECÍFICA APLICABLE:\n"
        for reg in relevant_normative["regulations"]:
            normative_context += f"  • {reg}\n"
        normative_context += "\n"
    
    # Reglas PMP
    rules_text = "\n".join([f"- {r.id}: {r.description} (Ref: {r.technical_reference})" for r in pmp_rules.values()])
    
    # Contexto de referencia (PSS y PMP)
    ref_context = ""
    if pss_text:
        ref_context += f"--- PSS DEL CLIENTE (Plan de Seguridad y Salud) ---\n{pss_text[:1500]}\n\n"
    if pmp_text:
        ref_context += f"--- PMP DEL CLIENTE (Políticas) ---\n{pmp_text[:1500]}\n\n"

    system_prompt = BASE_SYSTEM_PROMPT.format(
        regulations=", ".join(SPANISH_REGULATIONS)
    )

    user_prompt = f"""
{normative_context}
{ref_context}

--- REGLAS PMP OBLIGATORIAS ---
{rules_text}

--- PROCEDIMIENTO / BORRADOR RAMS A ANALIZAR ---
{procedure_text}

INSTRUCCIONES CRÍTICAS:
1. Extrae los pasos del procedimiento.
2. Para cada paso, identifica TODOS los peligros relevantes.
3. Para CADA peligro, CITA las NTPs y normativa específica aplicable (usa las del contexto normativo).
4. Evalúa P y S con rigor técnico.
5. Propón medidas siguiendo la jerarquía (Eliminación > Sustitución > EPC > Admin > EPI).
6. Compara contra PSS y PMP. Si hay incumplimiento, márcalo.

Devuelve SOLO un JSON válido con esta estructura exacta:
{{
  "activity_name": "Nombre de la actividad",
  "location": "Ubicación",
  "steps": [
    {{
      "step_number": 1,
      "description": "Descripción del paso",
      "hazards": [
        {{
          "description": "Peligro específico",
          "hazard_type": "Mecánico|Eléctrico|Químico|Altura|Tráfico|Confinado|Incendio|Ergonómico|Ruido|Otro",
          "probability": 3,
          "severity": 4,
          "justification": "Justificación técnica de P y S",
          "control_measures": ["Medida 1 (EPC)", "Medida 2 (Admin)", "Medida 3 (EPI)"],
          "normative_references": ["NTP 415", "RD 2177/2004"],
          "pmp_compliance": "Cumple PMP/PSS: SÍ/NO. Motivo."
        }}
      ]
    }}
  ],
  "pmp_missing_requirements": ["Requisito PMP no cumplido 1"],
  "recommendations": ["Recomendación 1"]
}}"""

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        data = json.loads(clean_json_response(response.content))
        
        # Procesar a modelos Pydantic
        eval_steps = []
        all_measures = []
        critical_count = 0
        pmp_missing = data.get("pmp_missing_requirements", [])
        
        for s in data.get("steps", []):
            hazards = []
            for h in s.get("hazards", []):
                p = max(1, min(5, int(h.get("probability", 3))))
                sev = max(1, min(5, int(h.get("severity", 3))))
                level = p * sev
                cls = get_risk_class(level)
                
                h_type = h.get("hazard_type", "Otro")
                if h_type not in HazardType.__members__: h_type = "OTRO"
                
                measures = h.get("control_measures", [])
                all_measures.extend(measures)
                if cls == RiskLevel.CRITICAL: critical_count += 1
                
                hazards.append(IdentifiedHazard(
                    description=h["description"],
                    hazard_type=HazardType(h_type),
                    probability=p, severity=sev, risk_level=level, classification=cls,
                    justification=h.get("justification", ""),
                    control_measures=measures,
                    normative_references=h.get("normative_references", []),
                    residual_risk=h.get("residual_risk")
                ))
            eval_steps.append(ActivityStep(step_number=s["step_number"], description=s["description"], hazards=hazards))
        
        # Validación PMP
        pmp_compliant = len(pmp_missing) == 0
        pmp_pct = ((len(pmp_rules) - len(pmp_missing)) / len(pmp_rules) * 100) if pmp_rules else 100
        
        recs = data.get("recommendations", [])
        if critical_count > 0:
            recs.insert(0, f"⚠️ {critical_count} riesgos CRÍTICOS detectados. Revisar método.")
        if not pmp_compliant:
            recs.insert(0, f"❌ Incumplimientos PMP/PSS: {', '.join(pmp_missing[:3])}")
        
        overall_level = RiskLevel.CRITICAL if critical_count > 0 else RiskLevel.HIGH
        
        return RiskAssessmentResult(
            activity_name=data.get("activity_name", "Actividad no identificada"),
            location=data.get("location", "No especificada"),
            steps=eval_steps,
            pmp_compliance=PMPComplianceCheck(
                compliant=pmp_compliant, 
                missing_requirements=pmp_missing, 
                compliance_percentage=pmp_pct
            ),
            overall_risk_level=overall_level,
            critical_hazards_count=critical_count,
            recommendations=recs
        )
        
    except Exception as e:
        print(f"Error en el motor IA: {e}")
        return RiskAssessmentResult(
            activity_name="Error en el análisis",
            location="N/A",
            overall_risk_level=RiskLevel.HIGH,
            recommendations=[f"Error: {str(e)}. Verifica que el texto sea legible."]
        )

def execute_prl_workflow(procedure_text: str, pss_text: str = "", pmp_text: str = "") -> Dict:
    """Orquesta el flujo completo"""
    print("🚀 Iniciando análisis con integración normativa...")
    
    risk_res = analyze_procedure_with_normative(procedure_text, pss_text, pmp_text, GOODMAN_PMP_RULES)
    
    summary = f"""
📊 INFORME DE ANÁLISIS PRL CON NORMATIVA INSST
------------------------------------------------
Actividad: {risk_res.activity_name}
Ubicación: {risk_res.location}
Pasos analizados: {len(risk_res.steps)}
Riesgos Críticos: {risk_res.critical_hazards_count}
Cumplimiento PMP/PSS: {risk_res.pmp_compliance.compliance_percentage}%

NORMATIVA APLICADA:
{chr(10).join(['  • ' + ref for step in risk_res.steps for h in step.hazards for ref in h.normative_references])[:500]}
"""
    
    return {
        "risk_assessment": risk_res,
        "final_report": {
            "executive_summary": summary,
            "recommendations": risk_res.recommendations
        }
    }
