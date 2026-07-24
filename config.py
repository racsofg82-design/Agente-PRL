"""
Configuración del Agente PRL Senior
"""
from enum import Enum
from typing import Dict, List
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
    id: str
    description: str
    category: str
    mandatory: bool = True
    keywords: List[str] = None

RISK_MATRIX_CONFIG = {
    "probability_labels": {
        1: "Rare (Improbable)",
        2: "Unlikely (Poco probable)",
        3: "Possible (Posible)",
        4: "Likely (Probable)",
        5: "Almost certain (Casi cierto)"
    },
    "severity_labels": {
        1: "Minor (Leve)",
        2: "Moderate (Moderado)",
        3: "Serious (Grave)",
        4: "Major (Muy grave)",
        5: "Major Catastrophic (Catastrófico)"
    },
    "thresholds": {
        "low": {"min": 1, "max": 3, "color": ColorCode.GREEN.value},
        "medium": {"min": 4, "max": 6, "color": ColorCode.YELLOW.value},
        "high": {"min": 8, "max": 12, "color": ColorCode.ORANGE.value},
        "critical": {"min": 15, "max": 25, "color": ColorCode.RED.value}
    }
}

GOODMAN_PMP_RULES: Dict[str, PMPRule] = {
    "ALTURA_001": PMPRule(
        id="ALTURA_001",
        description="Plan de rescate claro y disponible para trabajos en altura",
        category="trabajo_en_altura",
        mandatory=True,
        keywords=["rescate", "emergencia", "plan de rescate", "evacuación"]
    ),
    "ALTURA_002": PMPRule(
        id="ALTURA_002",
        description="Personal competente (formación + experiencia demostrable)",
        category="trabajo_en_altura",
        mandatory=True,
        keywords=["competente", "cualificado", "experiencia", "certificación"]
    ),
    "ALTURA_003": PMPRule(
        id="ALTURA_003",
        description="Inspección y mantenimiento regular de equipos",
        category="trabajo_en_altura",
        mandatory=True,
        keywords=["inspección", "mantenimiento", "revisión", "verificación"]
    ),
    "ALTURA_004": PMPRule(
        id="ALTURA_004",
        description="Evaluación de riesgos específica del sitio",
        category="trabajo_en_altura",
        mandatory=True,
        keywords=["específica", "sitio", "lugar", "ubicación"]
    ),
    "TRAFCO_001": PMPRule(
        id="TRAFCO_001",
        description="Límite de velocidad 10 km/h en obra",
        category="gestion_trafico",
        mandatory=True,
        keywords=["10 km/h", "velocidad", "límite velocidad"]
    ),
    "TRAFCO_002": PMPRule(
        id="TRAFCO_002",
        description="Segregación física entre peatones y vehículos",
        category="gestion_trafico",
        mandatory=True,
        keywords=["segregación", "barrera", "separación", "delimitación"]
    )
}

SPANISH_REGULATIONS = [
    "Ley 31/1995 de Prevención de Riesgos Laborales",
    "RD 1627/1997 (Disposiciones mínimas de seguridad en obras de construcción)",
    "RD 2177/2004 (Trabajos en altura)",
    "RD 1215/1997 (Utilización de equipos de trabajo)",
    "RD 39/1997 (Reglamento de los Servicios de Prevención)",
    "RD 773/1997 (Equipos de protección individual)",
    "RD 614/2001 (Riesgo eléctrico)",
    "RD 374/2001 (Agentes químicos)",
    "RD 286/2006 (Espacios confinados)",
]

NTP_CATALOG = {
    "trabajos_altura": {
        "category_name": "Trabajos en Altura y Caídas",
        "ntps": {
            "NTP 415": "Trabajos en altura: Prevención de caídas",
            "NTP 421": "Plataformas elevadoras móviles de personal (PEMP)",
            "NTP 423": "Líneas de vida",
            "NTP 424": "Plan de rescate",
        }
    },
    "epis": {
        "category_name": "Equipos de Protección Individual",
        "ntps": {
            "NTP 275": "EPIs: Selección y utilización",
            "NTP 283": "Protección contra caídas: Arnés y sistemas de anclaje",
        }
    }
}

def get_relevant_ntps(activity_type: str) -> Dict[str, str]:
    if activity_type in NTP_CATALOG:
        return NTP_CATALOG[activity_type]["ntps"]
    return {}

def format_ntps_for_prompt(activity_type: str) -> str:
    relevant_ntps = get_relevant_ntps(activity_type)
    if not relevant_ntps:
        return "No hay NTPs específicas aplicables."
    return "\n".join([f"- {k}: {v}" for k, v in relevant_ntps.items()])

BASE_SYSTEM_PROMPT = """Eres un Técnico Superior en Prevención de Riesgos Laborales con más de 15 años de experiencia en España.

NORMATIVA DE REFERENCIA:
{regulations}

NTPs APLICABLES:
{ntps}

REGLAS PMP DEL CLIENTE (OBLIGATORIAS):
{pmp_rules}

MATRIZ DE RIESGOS 5x5:
- Probabilidad (1-5): Rare, Unlikely, Possible, Likely, Almost certain
- Consecuencias (1-5): Minor, Moderate, Serious, Major, Major Catastrophic
- Nivel = P × S
  • 1-3 (Low/Verde): Aceptable
  • 4-6 (Medium/Amarillo): Requiere control adicional
  • 8-12 (High/Naranja): Medidas adicionales OBLIGATORIAS
  • 15-25 (Critical/Rojo): Actividad intrínsecamente insegura

JERARQUÍA DE CONTROLES:
1. Eliminación del peligro
2. Sustitución
3. Controles de ingeniería (EPCs)
4. Controles administrativos
5. EPIs"""