"""Modelos de datos"""
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class HazardType(str, Enum):
    MECANICO = "Mecánico"
    ELECTRICO = "Eléctrico"
    QUIMICO = "Químico"
    ALTURA = "Trabajo en altura"
    TRAFICO = "Tráfico"
    OTRO = "Otro"

class IdentifiedHazard(BaseModel):
    description: str
    hazard_type: HazardType = HazardType.OTRO
    probability: int
    severity: int
    risk_level: int
    classification: RiskLevel
    justification: str
    control_measures: List[str]
    residual_risk: Optional[int] = None

class ActivityStep(BaseModel):
    step_number: int
    description: str
    hazards: List[IdentifiedHazard]

class PMPComplianceCheck(BaseModel):
    compliant: bool
    missing_requirements: List[str] = []
    compliance_percentage: float = 100.0

class RiskAssessmentResult(BaseModel):
    activity_name: str
    location: str
    steps: List[ActivityStep] = []
    pmp_compliance: Optional[PMPComplianceCheck] = None
    overall_risk_level: RiskLevel = RiskLevel.MEDIUM
    critical_hazards_count: int = 0
    recommendations: List[str] = []

class NormativeFinding(BaseModel):
    severity: str
    description: str
    recommendation: str

class PSSReviewResult(BaseModel):
    overall_compliance: str = "No evaluado"
    findings: List[NormativeFinding] = []
