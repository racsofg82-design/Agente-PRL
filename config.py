"""Configuración del Agente PRL Senior - Con Biblioteca INSST Completa"""
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

# Reglas PMP de Goodman
GOODMAN_PMP_RULES: Dict[str, PMPRule] = {
    "ALTURA_001": PMPRule("ALTURA_001", "Plan de rescate claro y disponible", "trabajo_en_altura", True, ["rescate", "evacuación", "plan de rescate"], "NTP 424"),
    "ALTURA_002": PMPRule("ALTURA_002", "Personal competente y certificado", "trabajo_en_altura", True, ["competente", "certificado", "formación"], "RD 39/1997"),
    "ALTURA_003": PMPRule("ALTURA_003", "Inspección previa de equipos", "trabajo_en_altura", True, ["inspección", "revisión", "mantenimiento"], "NTP 289"),
    "TRAFCO_001": PMPRule("TRAFCO_001", "Límite de velocidad 10 km/h", "gestion_trafico", True, ["10 km/h", "velocidad"], "NTP 803"),
    "TRAFCO_002": PMPRule("TRAFCO_002", "Segregación física peatones/vehículos", "gestion_trafico", True, ["segregación", "barrera", "separación"], "NTP 801")
}

# Normativa Española Base
SPANISH_REGULATIONS = [
    "Ley 31/1995 de Prevención de Riesgos Laborales",
    "RD 1627/1997 (Seguridad en obras de construcción)",
    "RD 2177/2004 (Trabajos en altura)",
    "RD 1215/1997 (Utilización de equipos de trabajo)",
    "RD 39/1997 (Reglamento de los Servicios de Prevención)",
    "RD 773/1997 (Equipos de protección individual - EPIs)",
    "RD 614/2001 (Riesgo eléctrico)",
    "RD 374/2001 (Agentes químicos)",
    "RD 286/2006 (Espacios confinados)",
    "RD 487/1997 (Manipulación manual de cargas)",
    "RD 1311/2005 (Ruido)",
    "RD 486/1997 (Lugares de trabajo)"
]

# CATÁLOGO COMPLETO DE NTPs DEL INSST
NTP_CATALOG = {
    "altura": {
        "keywords": ["altura", "caída", "andamio", "escalera", "cubierta", "PEMP", "arnés", "línea de vida"],
        "ntps": [
            "NTP 415: Trabajos en altura: Prevención de caídas",
            "NTP 416: Sistemas de protección colectiva",
            "NTP 417: Sistemas de protección individual",
            "NTP 418: Trabajos con cuerdas (trabajos verticales)",
            "NTP 419: Andamios tubulares de fachada",
            "NTP 420: Andamios colgados motorizados",
            "NTP 421: Plataformas elevadoras móviles de personal (PEMP)",
            "NTP 422: Escaleras de mano",
            "NTP 423: Líneas de vida",
            "NTP 424: Plan de rescate en trabajos en altura",
            "NTP 742: Caídas a distinto nivel: Evaluación y prevención"
        ],
        "regulations": ["RD 2177/2004", "RD 1215/1997"]
    },
    "electrico": {
        "keywords": ["eléctrico", "tensión", "cuadro", "cable", "arco eléctrico", "LOTO"],
        "ntps": [
            "NTP 225: Riesgo eléctrico: Evaluación y prevención",
            "NTP 226: Contactos directos",
            "NTP 227: Contactos indirectos",
            "NTP 228: Trabajos en tensión",
            "NTP 229: Trabajos sin tensión",
            "NTP 230: Distancias de seguridad",
            "NTP 233: Procedimientos de bloqueo y etiquetado (LOTO)"
        ],
        "regulations": ["RD 614/2001", "REBT (RD 842/2002)"]
    },
    "quimico": {
        "keywords": ["químico", "producto químico", "disolvente", "pintura", "FDS", "etiquetado"],
        "ntps": [
            "NTP 150: Riesgo químico: Evaluación y prevención",
            "NTP 151: Agentes químicos peligrosos",
            "NTP 152: Fichas de datos de seguridad (FDS)",
            "NTP 156: Ventilación y extracción localizada",
            "NTP 157: Equipos de protección respiratoria",
            "NTP 166: Límites de exposición profesional (LEP)"
        ],
        "regulations": ["RD 374/2001", "REACH (CE 1907/2006)"]
    },
    "confinado": {
        "keywords": ["confinado", "espacio confinado", "depósito", "silo", "zanja profunda"],
        "ntps": [
            "NTP 610: Espacios confinados: Evaluación y prevención",
            "NTP 611: Atmósferas peligrosas",
            "NTP 612: Ventilación y purga",
            "NTP 613: Permisos de trabajo en espacios confinados",
            "NTP 614: Equipos de protección y rescate",
            "NTP 617: Vigilancia de la atmósfera"
        ],
        "regulations": ["RD 286/2006", "RD 2177/2004"]
    },
    "trafico": {
        "keywords": ["tráfico", "vehículo", "carretilla", "grúa", "movimiento de tierras"],
        "ntps": [
            "NTP 800: Gestión del tráfico en obras",
            "NTP 801: Segregación de peatones y vehículos",
            "NTP 802: Señalización y balizamiento",
            "NTP 803: Límites de velocidad",
            "NTP 404: Carretillas elevadoras: Evaluación y prevención"
        ],
        "regulations": ["RD 1627/1997", "RD 1215/1997"]
    },
    "cargas": {
        "keywords": ["carga", "levantamiento", "manual", "peso", "ergonómico"],
        "ntps": [
            "NTP 500: Manipulación manual de cargas: Evaluación y prevención",
            "NTP 501: Método INSST para MMC",
            "NTP 502: Método NIOSH",
            "NTP 508: Equipos auxiliares para MMC"
        ],
        "regulations": ["RD 487/1997"]
    },
    "ruido": {
        "keywords": ["ruido", "sonido", "decibelios", "auditivo"],
        "ntps": [
            "NTP 180: Ruido: Evaluación y prevención",
            "NTP 181: Medición y control",
            "NTP 182: Protectores auditivos"
        ],
        "regulations": ["RD 1311/2005"]
    },
    "incendio": {
        "keywords": ["incendio", "fuego", "soldadura", "trabajo en caliente", "extintor"],
        "ntps": [
            "NTP 100: Prevención de incendios",
            "NTP 102: Extintores",
            "NTP 109: Trabajos en caliente",
            "NTP 651: Permisos de trabajo en caliente"
        ],
        "regulations": ["RD 1627/1997", "Código Técnico de la Edificación (DB-SI)"]
    }
}

def find_relevant_ntps(text: str) -> Dict[str, List[str]]:
    """
    Busca NTPs y normativa relevante según el contenido del texto
    """
    text_lower = text.lower()
    relevant = {"ntps": [], "regulations": []}
    
    for category, data in NTP_CATALOG.items():
        # Si alguna palabra clave de la categoría está en el texto
        if any(keyword in text_lower for keyword in data["keywords"]):
            relevant["ntps"].extend(data["ntps"])
            relevant["regulations"].extend(data["regulations"])
    
    # Eliminar duplicados
    relevant["ntps"] = list(set(relevant["ntps"]))
    relevant["regulations"] = list(set(relevant["regulations"]))
    
    return relevant

# Prompt base del sistema
BASE_SYSTEM_PROMPT = """Eres un Técnico Superior en PRL con 15 años de experiencia en España.
Tu especialidad es el análisis técnico riguroso de procedimientos de trabajo.

NORMATIVA BASE: {regulations}

INSTRUCCIONES:
1. Analiza el procedimiento paso a paso.
2. Identifica TODOS los peligros (no solo los obvios).
3. Para cada peligro, CITA la NTP y normativa específica aplicable.
4. Evalúa P y S con criterios técnicos objetivos.
5. Propón medidas siguiendo la jerarquía (Eliminación > Sustitución > EPC > Admin > EPI).
6. Compara contra PSS y PMP para detectar incumplimientos.

MATRIZ 5x5: P(1-5) x S(1-5). 1-3:Low, 4-6:Medium, 8-12:High, 15-25:Critical."""
