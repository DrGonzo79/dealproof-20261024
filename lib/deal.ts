export type Adjustment={id:string;label:string;claimed:number;supported:number;replacementCost:number;evidence:string};
export type DealInput={id:string;name:string;sector:string;askingPrice:number;reportedEarnings:number;equityPercent:number;sellerNote:number;interestRate:number;termYears:number;customerConcentration:number;adjustments:Adjustment[]};
export type DealResult={normalizedEarnings:number;unsupportedAddbacks:number;replacementCost:number;loanNeeded:number;annualDebtService:number;dscr:number;maxSupportedLoan:number;equityGap:number;verdict:"GO"|"RENEGOTIATE"|"WALK";risks:string[]};

function annualPayment(principal:number,ratePercent:number,years:number):number{const r=ratePercent/1200;const n=years*12;return principal*(r*(1+r)**n)/((1+r)**n-1)*12;}

export function stressTestDeal(deal:DealInput):DealResult{
  if(deal.askingPrice<=0||deal.reportedEarnings<=0)throw new Error("Price and earnings must be positive.");
  if(deal.equityPercent<10||deal.equityPercent>100)throw new Error("Equity must be between 10% and 100%.");
  if(deal.termYears<=0||deal.interestRate<=0)throw new Error("Debt terms must be positive.");
  const unsupportedAddbacks=deal.adjustments.reduce((s,x)=>s+Math.max(0,x.claimed-x.supported),0);
  const replacementCost=deal.adjustments.reduce((s,x)=>s+x.replacementCost,0);
  const normalizedEarnings=Math.max(0,deal.reportedEarnings-unsupportedAddbacks-replacementCost);
  const loanNeeded=Math.max(0,deal.askingPrice-deal.askingPrice*deal.equityPercent/100-deal.sellerNote);
  const annualDebtService=annualPayment(loanNeeded,deal.interestRate,deal.termYears);
  const dscr=annualDebtService?normalizedEarnings/annualDebtService:99;
  const maxSupportedLoan=normalizedEarnings/1.25/annualPayment(1,deal.interestRate,deal.termYears);
  const equityGap=Math.max(0,loanNeeded-maxSupportedLoan);
  const risks=[...(unsupportedAddbacks>deal.reportedEarnings*.1?["More than 10% of reported earnings rests on unsupported addbacks"]:[]),...(replacementCost>deal.reportedEarnings*.15?["Owner replacement cost materially reduces cash flow"]:[]),...(deal.customerConcentration>=25?[`Top-customer concentration is ${deal.customerConcentration}%`]:[]),...(dscr<1.25?["Estimated DSCR misses the 1.25x lender floor"]:[])];
  const verdict:DealResult["verdict"]=dscr>=1.35&&deal.customerConcentration<25?"GO":dscr>=1.05&&equityGap<deal.askingPrice*.15?"RENEGOTIATE":"WALK";
  return{normalizedEarnings,unsupportedAddbacks,replacementCost,loanNeeded,annualDebtService,dscr,maxSupportedLoan,equityGap,verdict,risks};
}
