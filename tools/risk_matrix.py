"""Calculadora Matriz 5x5"""
from config import RISK_MATRIX_CONFIG, RiskClassification, ColorCode

def calculate_risk_level(probability: int, severity: int) -> dict:
    if not (1 <= probability <= 5 and 1 <= severity <= 5):
        raise ValueError("P y S deben estar entre 1 y 5")
    
    risk_value = probability * severity
    
    if risk_value <= 3:
        classification = RiskClassification.LOW
        color = ColorCode.GREEN
        action = "Aceptable con controles estándar"
        requires_additional = False
    elif risk_value <= 6:
        classification = RiskClassification.MEDIUM
        color = ColorCode.YELLOW
        action = "Requiere control adicional. Lista HECA, mayor supervisión"
        requires_additional = True
    elif risk_value <= 12:
        classification = RiskClassification.HIGH
        color = ColorCode.ORANGE
        action = "Riesgo no suficientemente controlado. Medidas adicionales OBLIGATORIAS"
        requires_additional = True
    else:
        classification = RiskClassification.CRITICAL
        color = ColorCode.RED
        action = "Actividad intrínsecamente insegura. Revisar método de trabajo"
        requires_additional = True
    
    return {
        "probability": probability,
        "severity": severity,
        "risk_value": risk_value,
        "classification": classification.value,
        "color": color.name,
        "color_hex": color.value,
        "action_required": action,
        "requires_additional_controls": requires_additional,
        "acceptable": not requires_additional
    }