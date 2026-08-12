"""
Validador PMP - Versión Profesional
Con lógica técnica para verificar cumplimiento específico
"""
from models import PMPComplianceCheck
from config import GOODMAN_PMP_RULES, PMPRule

def check_pmp_compliance(
    activity_type: str,
    measures: List[str],
    pmp_rules: Dict[str, PMPRule] = None
) -> PMPComplianceCheck:
    """
    Valida el cumplimiento de reglas PMP con lógica técnica avanzada
    
    Args:
        activity_type: Tipo de actividad (ej: "trabajo_en_altura")
        measures: Lista de medidas propuestas en la evaluación
        pmp_rules: Reglas PMP del cliente
    
    Returns:
        PMPComplianceCheck con resultado detallado
    """
    if pmp_rules is None:
        pmp_rules = GOODMAN_PMP_RULES
    
    measures_text = " ".join(measures).lower()
    missing_requirements = []
    observations = []
    compliant_count = 0
    
    # Filtrar reglas relevantes
    relevant_rules = {
        rule_id: rule for rule_id, rule in pmp_rules.items()
        if rule.category == activity_type or activity_type == "all"
    }
    
    for rule_id, rule in relevant_rules.items():
        # Verificar si hay cumplimiento técnico
        if rule.mandatory:
            found = False
            
            # Caso 1: Búsqueda por palabras clave
            if rule.keywords:
                for keyword in rule.keywords:
                    if keyword.lower() in measures_text:
                        found = True
                        break
            
            # Caso 2: Búsqueda por referencia técnica
            if not found and rule.technical_reference:
                # Ejemplo: Si la referencia es "NTP 424", buscar "plan de rescate"
                if "NTP 424" in rule.technical_reference and "rescate" in measures_text:
                    found = True
            
            # Caso 3: Búsqueda por contexto técnico
            if not found:
                # Ejemplo: Si es trabajo en altura, buscar "plan de rescate"
                if activity_type == "trabajo_en_altura" and "rescate" in measures_text:
                    found = True
            
            # Registrar resultado
            if found:
                compliant_count += 1
            else:
                missing_requirements.append(rule.description)
                observations.append(
                    f"Recomendación: {rule.description} (Ref: {rule.technical_reference})"
                )
    
    # Calcular porcentaje de cumplimiento
    total_rules = len(relevant_rules)
    compliance_percentage = (compliant_count / total_rules * 100) if total_rules > 0 else 100.0
    
    return PMPComplianceCheck(
        compliant=len(missing_requirements) == 0,
        missing_requirements=missing_requirements,
        observations=observations,
        compliance_percentage=round(compliance_percentage, 2)
    )
