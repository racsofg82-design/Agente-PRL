"""
Agente Evaluador de Riesgos - Versión Profesional
Con análisis técnico riguroso y cumplimiento normativo
"""
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from models import (
    RiskAssessmentResult, 
    ActivityStep, 
    IdentifiedHazard, 
    HazardType, 
    RiskLevel
)
from tools.risk_matrix import calculate_risk_level
from tools.pmp_validator import check_pmp_compliance
from config import (
    BASE_SYSTEM_PROMPT, 
    SPANISH_REGULATIONS, 
    GOODMAN_PMP_RULES,
    NTP_CATALOG,
    RISK_MATRIX_RULES
)
import json
import re

def format_ntps_for_prompt(activity_type: str) -> str:
    """Formatea NTPs relevantes para el prompt con referencias técnicas"""
    relevant_ntps = NTP_CATALOG.get(activity_type, {}).get("ntps", {})
    if not relevant_ntps:
        return "No hay NTPs específicas aplicables a esta actividad."
    
    formatted = []
    for ntp_number, ntp_title in relevant_ntps.items():
        # Extraer categorías técnicas de la NTP
        if "Trabajos en altura" in ntp_title:
            formatted.append(f"- {ntp_number}: {ntp_title} (NTP de seguridad en altura)")
        elif "EPIs" in ntp_title:
            formatted.append(f"- {ntp_number}: {ntp_title} (NTP de equipos de protección)")
        else:
            formatted.append(f"- {ntp_number}: {ntp_title}")
    
    return "\n".join(formatted)

def create_risk_assessor_prompt(
    activity_name: str,
    activity_steps: List[str],
    location: str,
    pmp_rules: Dict[str, Any]
) -> str:
    """Crea el prompt técnico completo para el evaluador de riesgos"""
    
    # Formatear reglas PMP
    pmp_rules_text = "\n".join([
        f"- {rule.id}: {rule.description} (Ref: {rule.technical_reference})"
        for rule in pmp_rules.values()
    ])
    
    # Formatear NTPs relevantes
    relevant_activity_types = []
    if any("altura" in step.lower() for step in activity_steps):
        relevant_activity_types.append("trabajos_altura")
    if any("tráfico" in step.lower() for step in activity_steps):
        relevant_activity_types.append("gestion_trafico")
    
    ntp_text = ""
    if relevant_activity_types:
        ntp_text = "\n".join([
            format_ntps_for_prompt(activity_type)
            for activity_type in relevant_activity_types
        ])
    else:
        ntp_text = "No hay NTPs específicas identificadas para esta actividad."

    return BASE_SYSTEM_PROMPT.format(
        regulations="\n".join(SPANISH_REGULATIONS),
        ntps=ntp_text,
        pmp_rules=pmp_rules_text
    )

def parse_llm_response(response: str) -> List[ActivityStep]:
    """Parsea la respuesta del LLM con validación técnica rigurosa"""
    try:
        # Intentar parsear como JSON
        data = json.loads(response)
        
        # Validación técnica avanzada
        activity_steps = []
        for step_data in data["steps"]:
            hazards = []
            for hazard_data in step_data["hazards"]:
                # Validar probabilidad y severidad
                if not (1 <= hazard_data["probability"] <= 5):
                    hazard_data["probability"] = 3  # Valor por defecto
                if not (1 <= hazard_data["severity"] <= 5):
                    hazard_data["severity"] = 3
                
                # Validar tipo de peligro
                hazard_type = hazard_data.get("hazard_type", "Mecánico")
                if hazard_type not in HazardType.__members__:
                    hazard_type = "Mecánico"
                
                # Calcular nivel de riesgo
                risk_level = hazard_data["probability"] * hazard_data["severity"]
                
                hazards.append(IdentifiedHazard(
                    description=hazard_data["description"],
                    hazard_type=HazardType(hazard_type),
                    probability=hazard_data["probability"],
                    severity=hazard_data["severity"],
                    risk_level=risk_level,
                    classification=RiskLevel.LOW if risk_level <= 3 else 
                                   RiskLevel.MEDIUM if risk_level <= 6 else
                                   RiskLevel.HIGH if risk_level <= 12 else
                                   RiskLevel.CRITICAL,
                    justification_probability=hazard_data.get("justification_probability", "No justificación proporcionada"),
                    justification_severity=hazard_data.get("justification_severity", "No justificación proporcionada"),
                    control_measures=hazard_data["control_measures"],
                    residual_risk=hazard_data.get("residual_risk")
                ))
            
            activity_steps.append(ActivityStep(
                step_number=step_data["step_number"],
                description=step_data["description"],
                hazards=hazards,
                observations=step_data.get("observations")
            ))
        
        return activity_steps
    
    except Exception as e:
        print(f"Error parsing LLM response: {str(e)}")
        # En caso de fallo, generar análisis manual
        return _fallback_risk_analysis(activity_steps, location)

def _fallback_risk_analysis(activity_steps: List[str], location: str) -> List[ActivityStep]:
    """Análisis de respaldo con lógica técnica para casos de error"""
    steps = []
    for i, step_desc in enumerate(activity_steps):
        hazards = []
        
        # Identificar peligros por palabra clave
        if "altura" in step_desc.lower() or "cubierta" in step_desc.lower() or "andamio" in step_desc.lower():
            hazards.append(IdentifiedHazard(
                description="Caída a distinto nivel",
                hazard_type=HazardType.ALTURA,
                probability=3,
                severity=5,
                risk_level=15,
                classification=RiskLevel.CRITICAL,
                justification_probability="Trabajo en altura sin protección adecuada",
                justification_severity="Caída desde >2m con potencial de lesión catastrófica",
                control_measures=[
                    "Uso de PEMP con cesta (NTP 421)",
                    "Arnés de seguridad con doble cabo anclado a estructura (NTP 423)",
                    "Plan de rescate activado (NTP 424)",
                    "Personal competente certificado (RD 39/1997)"
                ],
                residual_risk=6
            ))
        
        if "tráfico" in step_desc.lower() or "vehículo" in step_desc.lower():
            hazards.append(IdentifiedHazard(
                description="Atropello por vehículo",
                hazard_type=HazardType.TRAFICO,
                probability=4,
                severity=4,
                risk_level=16,
                classification=RiskLevel.CRITICAL,
                justification_probability="Alta frecuencia de exposición en obra",
                justification_severity="Posible lesión grave o muerte",
                control_measures=[
                    "Límite de velocidad 10 km/h (NTP 803)",
                    "Segregación física con barreras (NTP 801)",
                    "Personal de control de tráfico dedicado"
                ],
                residual_risk=8
            ))
        
        steps.append(ActivityStep(
            step_number=i + 1,
            description=step_desc,
            hazards=hazards
        ))
    
    return steps

def assess_activity(
    activity_name: str,
    activity_steps: List[str],
    location: str = "No especificada",
    pmp_rules: Dict[str, Any] = None
) -> RiskAssessmentResult:
    """Evaluación de riesgos con análisis técnico riguroso"""
    if pmp_rules is None:
        pmp_rules = GOODMAN_PMP_RULES
    
    # Crear prompt técnico
    system_prompt = create_risk_assessor_prompt(
        activity_name, 
        activity_steps, 
        location,
        pmp_rules
    )
    
    # Inicializar LLM
    llm = ChatOpenAI(
        model="gpt-4-turbo-preview",
        temperature=0.1,
        max_tokens=4000
    )
    
    # Crear mensaje de usuario
    user_prompt = f"""
EVALUACIÓN DE RIESGOS - ACTIVIDAD: {activity_name}
LUGAR: {location}

PASOS A EVALUAR:
{chr(10).join([f"{i+1}. {step}" for i, step in enumerate(activity_steps)])}

INSTRUCCIONES:
1. Para CADA PASO, identifica TODOS los peligros relevantes
2. Para CADA peligro, evalúa:
   - Probabilidad (1-5) con justificación TÉCNICA
   - Severidad (1-5) con justificación TÉCNICA
   - Calcula el nivel (P × S)
3. Propón medidas de control siguiendo JERARQUÍA TÉCNICA:
   a) Eliminación del peligro
   b) Sustitución
   c) Controles de ingeniería (EPCs)
   d) Controles administrativos
   e) Equipos de protección individual (EPIs)
4. Calcula el riesgo residual tras medidas
5. Verifica cumplimiento de reglas PMP (cita referencias técnicas)

FORMATO DE RESPUESTA (JSON estricto):
{{
    "steps": [
        {{
            "step_number": 1,
            "description": "Descripción del paso",
            "hazards": [
                {{
                    "description": "Descripción del peligro",
                    "hazard_type": "Mecánico|Eléctrico|Químico|Ergonómico|Altura|Tráfico",
                    "probability": 1-5,
                    "severity": 1-5,
                    "justification_probability": "Justificación TÉCNICA",
                    "justification_severity": "Justificación TÉCNICA",
                    "control_measures": ["medida 1", "medida 2"],
                    "residual_risk": número (opcional)
                }}
            ],
            "observations": "Observaciones técnicas (opcional)"
        }}
    ]
}}

RECUERDA:
- Sé específico, no genérico
- Cita NTPs y normativa cuando corresponda
- Justifica siempre tus valoraciones
- Si un riesgo es Critical (rojo), PROPÓN alternativas
- Incluye referencias a NTPs para medidas técnicas
"""

    try:
        # Ejecutar LLM
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        # Parsear respuesta
        evaluated_steps = parse_llm_response(response.content)
        
        # Validar PMP
        all_measures = []
        for step in evaluated_steps:
            for hazard in step.hazards:
                all_measures.extend(hazard.control_measures)
        
        pmp_validation = check_pmp_compliance(
            "all",
            all_measures,
            pmp_rules
        )
        
        # Calcular riesgos críticos
        critical_count = sum(
            1 
            for step in evaluated_steps 
            for hazard in step.hazards 
            if hazard.classification == RiskLevel.CRITICAL
        )
        
        # Generar recomendaciones técnicas
        recommendations = []
        if critical_count > 0:
            recommendations.append(
                f"⚠️ Existen {critical_count} riesgo(s) crítico(s) que requieren revisión del método de trabajo"
            )
        if not pmp_validation.compliant:
            recommendations.append(
                f"❌ Incumplimiento del PMP: {', '.join(pmp_validation.missing_requirements)}"
            )
        recommendations.append("📢 Realizar toolbox talk con todos los trabajadores")
        recommendations.append("👷 Verificar formación y competencia del personal")
        
        return RiskAssessmentResult(
            activity_name=activity_name,
            location=location,
            steps=evaluated_steps,
            pmp_compliance=pmp_validation,
            overall_risk_level=RiskLevel.CRITICAL if critical_count > 0 else RiskLevel.HIGH,
            critical_hazards_count=critical_count,
            recommendations=recommendations
        )
    
    except Exception as e:
        print(f"Error en evaluación: {str(e)}")
        # En caso de error, usar análisis de respaldo
        evaluated_steps = _fallback_risk_analysis(activity_steps, location)
        
        # Validar PMP
        all_measures = []
        for step in evaluated_steps:
            for hazard in step.hazards:
                all_measures.extend(hazard.control_measures)
        
        pmp_validation = check_pmp_compliance(
            "all",
            all_measures,
            pmp_rules
        )
        
        critical_count = sum(
            1 
            for step in evaluated_steps 
            for hazard in step.hazards 
            if hazard.classification == RiskLevel.CRITICAL
        )
        
        recommendations = [
            "⚠️ Análisis parcial debido a error técnico",
            "Revisar manualmente los pasos críticos"
        ]
        
        return RiskAssessmentResult(
            activity_name=activity_name,
            location=location,
            steps=evaluated_steps,
            pmp_compliance=pmp_validation,
            overall_risk_level=RiskLevel.CRITICAL if critical_count > 0 else RiskLevel.HIGH,
            critical_hazards_count=critical_count,
            recommendations=recommendations
        )
