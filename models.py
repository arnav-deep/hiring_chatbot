from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class MercorUsers(BaseModel):
    userId: str = Field(..., max_length=255)
    email: EmailStr
    name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=255)
    residence: Optional[Dict[str, Any]] = None
    profilePic: Optional[str] = None
    createdAt: datetime
    lastLogin: datetime
    notes: Optional[str] = None
    referralCode: str = Field(default_factory=lambda: str(uuid.uuid4()), max_length=255)
    isGptEnabled: bool = False
    preferredRole: Optional[str] = Field(None, max_length=255)
    fullTimeStatus: Optional[str] = Field(None, max_length=255)
    workAvailability: Optional[str] = Field(None, max_length=255)
    fullTimeSalaryCurrency: Optional[str] = Field(None, max_length=255)
    fullTimeSalary: Optional[str] = Field(None, max_length=255)
    partTimeSalaryCurrency: Optional[str] = Field(None, max_length=255)
    partTimeSalary: Optional[str] = Field(None, max_length=255)
    fullTime: bool = False
    fullTimeAvailability: Optional[int] = None
    partTime: bool = False
    partTimeAvailability: Optional[int] = None
    w8BenUrl: Optional[Dict[str, Any]] = None
    tosUrl: Optional[str] = None
    policyUrls: Optional[Dict[str, Any]] = None
    isPreVetted: bool = False
    isActive: bool = False
    isComplete: bool = False
    summary: Optional[str] = None
    preVettedAt: Optional[datetime] = None


class Skills(BaseModel):
    skillId: str = Field(..., max_length=255)
    skillName: str = Field(..., max_length=255)
    skillValue: str = Field(..., max_length=255)


class MercorUserSkills(BaseModel):
    userId: str = Field(..., max_length=255)
    skillId: str = Field(..., max_length=255)
    isPrimary: bool = False
    order: int = 0


class Message(BaseModel):
    role: str
    content: str


class MessageResponse(BaseModel):
    messages: List[Message]
    users: List[MercorUsers] = []
