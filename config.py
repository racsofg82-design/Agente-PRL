"""Configuración del Agente PRL Senior"""
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass

class RiskClassification(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class PMPRule:
    id: str
    description: str
    category: str
    mandatory: bool = True
    keywords: List[str] = None
    technical_reference: str = ""

GOODMAN_PMP_RULES: Dict[str, PMPRule] = {
    "ALTURA_001": PMPRule("ALTURA_001", "Plan de rescate claro y disponible", "trabajo_en_altura", True, ["rescate", "evacuación", "plan de rescate"], "NTP 424"),
    "ALTURA_002": PMPRule("ALTURA_002", "Personal competente y certificado", "trabajo_en_altura", True, ["competente", "certificado", "formación"], "RD 39/1997"),
    "ALTURA_003": PMPRule("ALTURA_003", "Inspección previa de equipos", "trabajo_en_altura", True, ["inspección", "revisión", "mantenimiento"], "NTP 289"),
    "TRAFCO_001": PMPRule("TRAFCO_001", "Límite de velocidad 10 km/h", "gestion_trafico", True, ["10 km/h", "velocidad"], "NTP 803"),
    "TRAFCO_002": PMPRule("TRAFCO_002", "Segregación física peatones/vehículos", "gestion_trafico", True, ["segregación", "barrera", "separación"], "NTP 801")
}

SPANISH_REGULATIONS = [
    "Ley 31/1995 de Prevención de Riesgos Laborales",
    "RD 1627/1997 (Seguridad en obras)",
    "RD 2177/2004 (Trabajos en altura)",
    "RD 1215/1997 (Equipos de trabajo)",
    "RD 773/1997 (EPIs)"
]

NTP_CATALOG = {
    "trabajos_altura": ["NTP 415 (Caídas)", "NTP 421 (PEMP)", "NTP 423 (Líneas de vida)", "NTP 424 (Rescate)"],
    "gestion_trafico": ["NTP 800 (Gestión tráfico)", "NTP 801 (Segregación)", "NTP 803 (Velocidad)"],
    "epis": ["NTP 275 (Selección EPIs)", "NTP 283 (Arnés)"]
}

BASE_SYSTEM_PROMPT = """Eres un Técnico Superior en PRL con 15 años de experiencia en España.
NORMATIVA: {regulations}
NTPs: {ntps}
PMP: {pmp_rules}

MATRIZ 5x5: P(1-5) x S(1-5). 1-3:Low, 4-6:Medium, 8-12:High, 15-25:Critical.
JERARQUÍA: 1)Eliminación 2)Sustitución 3)EPC 4)Admin 5)EPI.
Analiza con rigor técnico. Cita NTPs."""
