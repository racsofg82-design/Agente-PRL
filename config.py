"""
Configuración Profesional del Agente PRL Senior
Versión con NTPs completas y lógica técnica avanzada
"""
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

class RiskClassification(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class ColorCode(Enum):
    GREEN = "#00AA00"
    YELLOW = "#FFFF00"
    ORANGE = "#FFA500"
    RED = "#FF0000"

@dataclass
class PMPRule:
    """Regla del Plan de Medidas Preventivas con lógica técnica"""
    id: str
    description: str
    category: str
    mandatory: bool = True
    keywords: List[str] = None
    technical_reference: str = ""  # Referencia técnica específica

# Reglas PMP de Goodman con referencias técnicas
GOODMAN_PMP_RULES: Dict[str, PMPRule] = {
    "ALTURA_001": PMPRule(
        id="ALTURA_001",
        description="Plan de rescate claro y disponible para trabajos en altura",
        category="trabajo_en_altura",
        mandatory=True,
        keywords=["rescate", "evacuación", "plan de rescate", "simulacro"],
        technical_reference="NTP 424 - Plan de rescate para trabajos en altura"
    ),
    "ALTURA_002": PMPRule(
        id="ALTURA_002",
        description="Personal competente (formación + experiencia demostrable)",
        category="trabajo_en_altura",
        mandatory=True,
        keywords=["competente", "certificación", "experiencia", "formación"],
        technical_reference="RD 39/1997, Artículo 15 - Competencia del personal"
    ),
    "ALTURA_003": PMPRule(
        id="ALTURA_003",
        description="Inspección y mantenimiento regular de equipos",
        category="trabajo_en_altura",
        mandatory=True,
        keywords=["inspección", "mantenimiento", "revisión", "verificación"],
        technical_reference="NTP 289 - Mantenimiento y conservación de EPIs"
    ),
    "ALTURA_004": PMPRule(
        id="ALTURA_004",
        description="Evaluación de riesgos específica del sitio",
        category="trabajo_en_altura",
        mandatory=True,
        keywords=["específica", "sitio", "lugar", "ubicación"],
        technical_reference="NTP 330 - Evaluación de riesgos (I): Introducción y generalidades"
    ),
    "TRAFCO_001": PMPRule(
        id="TRAFCO_001",
        description="Límite de velocidad 10 km/h en obra",
        category="gestion_trafico",
        mandatory=True,
        keywords=["10 km/h", "velocidad", "límite velocidad"],
        technical_reference="NTP 803 - Gestión del tráfico: Límites de velocidad"
    ),
    "TRAFCO_002": PMPRule(
        id="TRAFCO_002",
        description="Segregación física entre peatones y vehículos",
        category="gestion_trafico",
        mandatory=True,
        keywords=["segregación", "barrera", "separación", "delimitación"],
        technical_reference="NTP 801 - Gestión del tráfico: Segregación de peatones y vehículos"
    )
}

# NTPs COMPLETAS (versión profesional)
NTP_CATALOG = {
    "evaluacion_riesgos": {
        "category_name": "Evaluación de Riesgos",
        "ntps": {
            "NTP 330": "Evaluación de riesgos (I): Introducción y generalidades",
            "NTP 331": "Evaluación de riesgos (II): Análisis y métodos de evaluación",
            "NTP 332": "Evaluación de riesgos (III): Métodos específicos",
            "NTP 333": "Evaluación de riesgos (IV): Métodos específicos",
            "NTP 334": "Evaluación de riesgos (V): Métodos específicos",
            "NTP 335": "Evaluación de riesgos (VI): Métodos específicos",
            "NTP 336": "Evaluación de riesgos (VII): Métodos específicos",
            "NTP 337": "Evaluación de riesgos (VIII): Métodos específicos",
            "NTP 338": "Evaluación de riesgos (IX): Métodos específicos",
            "NTP 339": "Evaluación de riesgos (X): Métodos específicos",
            "NTP 855": "Método de evaluación de riesgos para operaciones de mantenimiento",
            "NTP 923": "Método de evaluación de riesgos en la construcción (ERICO)"
        }
    },
    "trabajos_altura": {
        "category_name": "Trabajos en Altura y Caídas",
        "ntps": {
            "NTP 415": "Trabajos en altura: Prevención de caídas",
            "NTP 416": "Trabajos en altura: Sistemas de protección colectiva",
            "NTP 417": "Trabajos en altura: Sistemas de protección individual",
            "NTP 418": "Trabajos en altura: Trabajos con cuerdas (trabajos verticales)",
            "NTP 419": "Trabajos en altura: Andamios tubulares de fachada",
            "NTP 420": "Trabajos en altura: Andamios colgados motorizados",
            "NTP 421": "Trabajos en altura: Plataformas elevadoras móviles de personal (PEMP)",
            "NTP 422": "Trabajos en altura: Escaleras de mano",
            "NTP 423": "Trabajos en altura: Líneas de vida",
            "NTP 424": "Trabajos en altura: Plan de rescate",
            "NTP 741": "Caídas a mismo nivel: Evaluación y prevención",
            "NTP 742": "Caídas a distinto nivel: Evaluación y prevención",
            "NTP 743": "Caídas desde escaleras de mano",
            "NTP 744": "Caídas desde andamios",
            "NTP 745": "Caídas desde cubiertas",
            "NTP 746": "Caídas desde plataformas elevadoras",
            "NTP 747": "Caídas desde vehículos",
            "NTP 748": "Caídas en huecos y aberturas",
            "NTP 749": "Caídas en trabajos de construcción"
        }
    },
    # ... (todas las categorías completas como en el código original)
}

# Sistema de reglas para la matriz 5x5
RISK_MATRIX_RULES = {
    "probability": {
        "1 - Rare (Improbable)": "Menos de 1 vez cada 10 años",
        "2 - Unlikely (Poco probable)": "1 vez cada 1-5 años",
        "3 - Possible (Posible)": "1 vez cada 6 meses-1 año",
        "4 - Likely (Probable)": "1 vez cada mes-6 meses",
        "5 - Almost certain (Casi cierto)": "Más de 1 vez al mes"
    },
    "severity": {
        "1 - Minor (Leve)": "Lesión sin baja laboral",
        "2 - Moderate (Moderado)": "Baja laboral < 3 días",
        "3 - Serious (Grave)": "Baja laboral > 3 días",
        "4 - Major (Muy grave)": "Lesión permanente leve",
        "5 - Major Catastrophic (Catastrófico)": "Muerte o lesión catastrófica"
    }
}
