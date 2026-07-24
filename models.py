"""Modelos de datos Pydantic"""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class HazardType(str, Enum):
    MECANICO = "Mecánico"
    ELECTRICO = "Eléctrico"
    QUIMICO = "Químico"
    ERGONOMICO = "Ergonómico"
    ALTURA = "Trabajo en altura"
    TRAFICO = "Tráfico"
    CONFINADO = "Espacio confinado"

class IdentifiedHazard(BaseModel):
    description: str
    hazard_type: HazardType
    probability: int
    severity: int
    risk_level: int
    classification: RiskLevel
    justification_probability: str
    justification_severity: str
    control_measures: List[str]
    residual_risk: Optional[int] = None
    pmp_compliance_notes: Optional[str] = None

class ActivityStep(BaseModel):
    step_number: int
    description: str
    hazards: List[IdentifiedHazard]
    observations: Optional[str] = None

class PMPComplianceCheck(BaseModel):
    compliant: bool
    missing_requirements: List[str] = []
    observations: List[str] = []
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
    finding_type: str
    severity: str
    description: str
    evidence: str
    regulation_reference: str
    recommendation: str

class PSSReviewResult(BaseModel):
    document_name: str
    document_version: str
    client: str
    findings: List[NormativeFinding] = []
    overall_compliance: str = "No evaluado"
    critical_findings_count: int = 0
    summary: str = ""