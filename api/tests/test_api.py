from fastapi.testclient import TestClient
from api.main import app
client=TestClient(app)

def payload(**overrides):
    data={"deal_id":"DP-3104","asking_price":3800000,"reported_earnings":800000,"equity_percent":10,"seller_note":190000,"interest_rate":10.5,"term_years":10,"customer_concentration":18,"adjustments":[{"label":"Owner vehicle","claimed":24000,"supported":0,"replacement_cost":0},{"label":"Owner salary","claimed":180000,"supported":180000,"replacement_cost":145000},{"label":"Spouse bookkeeping","claimed":72000,"supported":72000,"replacement_cost":48000}]}
    data.update(overrides);return data

def test_health():assert client.get("/health").json()=={"status":"ok"}
def test_stress_test_returns_lender_view():
    response=client.post("/deals/stress-test",json=payload());assert response.status_code==200
    body=response.json();assert body["normalized_earnings"]==583000;assert body["unsupported_addbacks"]==24000;assert body["verdict"] in {"GO","RENEGOTIATE","WALK"};assert body["dscr"]>0
def test_flags_concentration_and_weak_cash_flow():
    response=client.post("/deals/stress-test",json=payload(customer_concentration=50,reported_earnings=300000));assert response.status_code==200
    assert any("concentration" in risk for risk in response.json()["risks"]);assert response.json()["verdict"]=="WALK"
def test_rejects_equity_below_sba_demo_floor():assert client.post("/deals/stress-test",json=payload(equity_percent=5)).status_code==422
def test_rejects_impossible_seller_note():
    response=client.post("/deals/stress-test",json=payload(seller_note=4000000));assert response.status_code==422;assert "cannot exceed" in response.json()["detail"]
