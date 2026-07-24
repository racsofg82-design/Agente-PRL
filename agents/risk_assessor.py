"""Agente Evaluador de Riesgos"""
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from models import RiskAssessmentResult, ActivityStep, IdentifiedHazard, HazardType, RiskLevel
from tools.risk_matrix import calculate_risk_level
from tools.pmp_validator import check_pmp_compliance
from config import BASE_SYSTEM_PROMPT, SPANISH_REGULATIONS, GOODMAN_PMP_RULES, format_ntps_for_prompt

def assess_activity(
    activity_name: str,
    activity_steps: List[str],
    location: str = "No especificada",
    pmp_rules: dict = None
) -> RiskAssessmentResult:
    if pmp_rules is None:
        pmp_rules = GOODMAN_PMP_RULES
    
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.1)
    
    evaluated_steps = []
    
    for idx, step_desc in enumerate(activity_steps):
        prompt = BASE_SYSTEM_PROMPT.format(
            regulations="\n".join(SPANISH_REGULATIONS),
            ntps=format_ntps_for_prompt("trabajos_altura"),
            pmp_rules="\n".join([f"- {r.description}" for r in pmp_rules.values()])
        )
        
        user_prompt = f"""
Evalúa el paso {idx + 1}: {step_desc}

Actividad: {activity_name}
Lugar: {location}

Devuelve JSON con estructura de ActivityStep.
"""
        try:
            response = llm.invoke([SystemMessage(content=prompt), HumanMessage(content=user_prompt)])
            
            # Por ahora, creamos un hazard de ejemplo
            # En producción, parsear la respuesta JSON del LLM
            hazards = [
                IdentifiedHazard(
                    description="Caída a distinto nivel",
                    hazard_type=HazardType.ALTURA,
                    probability=3,
                    severity=5,
                    risk_level=15,
                    classification=RiskLevel.CRITICAL,
                    justification_probability="Trabajo en altura sin protección",
                    justification_severity="Caída desde >2m",
                    control_measures=["Arnés doble cabo", "Línea de vida", "Plan de rescate"]
                )
            ]
            
            step = ActivityStep(
                step_number=idx + 1,
                description=step_desc,
                hazards=hazards
            )
            evaluated_steps.append(step)
        except Exception as e:
            print(f"Error en paso {idx}: {e}")
    
    # Validar PMP
    all_measures = []
    for step in evaluated_steps:
        for h in step.hazards:
            all_measures.extend(h.control_measures)
    
    pmp_check = check_pmp_compliance("all", all_measures, pmp_rules)
    
    critical_count = sum(1 for s in evaluated_steps for h in s.hazards if h.classification == RiskLevel.CRITICAL)
    
    return RiskAssessmentResult(
        activity_name=activity_name,
        location=location,
        steps=evaluated_steps,
        pmp_compliance=pmp_check,
        overall_risk_level=RiskLevel.CRITICAL if critical_count > 0 else RiskLevel.HIGH,
        critical_hazards_count=critical_count,
        recommendations=["Revisar método de trabajo", "Aprobar por responsable HSE"] if critical_count > 0 else []
    )