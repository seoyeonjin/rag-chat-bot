from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from datetime import datetime

class UserInfo(BaseModel):
    solarspaceId: Optional[int] = Field(None, example=13232017)
    businessNumber: Optional[str] = Field(None, example="5650102273")
    firmName: Optional[str] = Field(None, example="이봉금태양광발전소")
    representativePhone: Optional[str] = Field(None, example="0614731261")
    plantName: Optional[str] = Field(None, example="이봉금태양광발전소")
    facilityConfirm: Optional[bool] = Field(None, example=True)
    facilityCode: Optional[str] = Field(None, example="PV15-S-01234")
    facilityCapa: Optional[str] = Field(None, example="99.63")
    facilityWeight: Optional[str] = Field(None, example="1.5")
    permitNumber: Optional[str] = Field(None, example="영암제1234호")
    permitCapa: Optional[str] = Field(None, example="98.44")
    ppaContractTarget: Optional[str] = Field(None, example="한국전력공사")
    ppaContractNumber: Optional[str] = Field(None, example="5001012345")
    taxRegistrationId: Optional[str] = Field(None, example="0159")
    ppaBranchOffice: Optional[str] = Field(None, example="한국전력공사 영암지사")
    ppaContactPhone: Optional[str] = Field(None, example="062-260-5101")
    recTradingType: Optional[Literal["FIXED", "MARKET"]] = Field(None, example="FIXED")
    recContractTarget: Optional[str] = Field(None, example="한국수력원자력(주)")
    commercialDate: Optional[str] = Field(None, example="2023-06-23")
    recStartDate: Optional[str] = Field(None, example="2023-06-23")
    subscription: Optional[Literal["ACTIVE", "INACTIVE"]] = Field(None, example="ACTIVE")
    certificateExpiresAt: Optional[datetime] = Field(None, example="2025-03-24T23:59:59")
    representativeName: Optional[str] = Field(None, example="최파나")
    contactName: Optional[str] = Field(None, example="조나아")
    contactPhone: Optional[str] = Field(None, example="01037652656")
    contactMail: Optional[str] = Field(None, example="x22e45gf@kakao.com")

class QueryRequest(BaseModel):
    question: str = Field(..., example="내 발전소 관리자가 누구야?")
    user: UserInfo
    history: Optional[List[str]] = Field(
        default=None,
        example=[
            "지난달 매출은 1,200,000원이었어요.",
            "계약 대상은 한국전력공사입니다."
        ]
    )

class QueryResponse(BaseModel):
    answer: str
    summary: str
