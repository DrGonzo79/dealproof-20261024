from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app=FastAPI(title="DealProof API",version="1.0.0")

class Adjustment(BaseModel):
    label:str=Field(min_length=1,max_length=100)
    claimed:float=Field(ge=0,le=10_000_000)
    supported:float=Field(ge=0,le=10_000_000)
    replacement_cost:float=Field(ge=0,le=10_000_000)

class StressTestRequest(BaseModel):
    deal_id:str=Field(pattern=r"^DP-[0-9]{4,}$",max_length=30)
    asking_price:float=Field(gt=0,le=100_000_000)
    reported_earnings:float=Field(gt=0,le=20_000_000)
    equity_percent:float=Field(ge=10,le=100)
    seller_note:float=Field(ge=0,le=100_000_000)
    interest_rate:float=Field(gt=0,le=30)
    term_years:int=Field(gt=0,le=30)
    customer_concentration:float=Field(ge=0,le=100)
    adjustments:list[Adjustment]=Field(max_length=100)

class StressTestResponse(BaseModel):
    deal_id:str
    normalized_earnings:float
    unsupported_addbacks:float
    replacement_cost:float
    loan_needed:float
    annual_debt_service:float
    dscr:float
    max_supported_loan:float
    equity_gap:float
    verdict:Literal["GO","RENEGOTIATE","WALK"]
    risks:list[str]

def annual_payment(principal:float,rate_percent:float,years:int)->float:
    rate=rate_percent/1200
    months=years*12
    return principal*(rate*(1+rate)**months)/((1+rate)**months-1)*12

@app.get("/health")
def health()->dict[str,str]:return{"status":"ok"}

@app.post("/deals/stress-test",response_model=StressTestResponse)
def stress_test(payload:StressTestRequest)->StressTestResponse:
    if payload.seller_note>payload.asking_price:
        raise HTTPException(status_code=422,detail="Seller note cannot exceed asking price")
    unsupported=sum(max(0,a.claimed-a.supported) for a in payload.adjustments)
    replacement=sum(a.replacement_cost for a in payload.adjustments)
    normalized=max(0,payload.reported_earnings-unsupported-replacement)
    needed=max(0,payload.asking_price*(1-payload.equity_percent/100)-payload.seller_note)
    debt_service=annual_payment(needed,payload.interest_rate,payload.term_years) if needed else 0
    dscr=normalized/debt_service if debt_service else 99
    factor=annual_payment(1,payload.interest_rate,payload.term_years)
    max_loan=normalized/1.25/factor
    gap=max(0,needed-max_loan)
    risks=[]
    if unsupported>payload.reported_earnings*.1:risks.append("More than 10% of reported earnings rests on unsupported addbacks")
    if replacement>payload.reported_earnings*.15:risks.append("Owner replacement cost materially reduces cash flow")
    if payload.customer_concentration>=25:risks.append(f"Top-customer concentration is {payload.customer_concentration:g}%")
    if dscr<1.25:risks.append("Estimated DSCR misses the 1.25x lender floor")
    verdict:Literal["GO","RENEGOTIATE","WALK"]="GO" if dscr>=1.35 and payload.customer_concentration<25 else "RENEGOTIATE" if dscr>=1.05 and gap<payload.asking_price*.15 else "WALK"
    return StressTestResponse(deal_id=payload.deal_id,normalized_earnings=round(normalized,2),unsupported_addbacks=round(unsupported,2),replacement_cost=round(replacement,2),loan_needed=round(needed,2),annual_debt_service=round(debt_service,2),dscr=round(dscr,3),max_supported_loan=round(max_loan,2),equity_gap=round(gap,2),verdict=verdict,risks=risks)
