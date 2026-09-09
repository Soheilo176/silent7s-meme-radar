from rapidfuzz.fuzz import token_set_ratio
def score(t, trends):
 best=(0,None)
 for x in trends:
  s=max(token_set_ratio(t["name"].lower(),x["title"].lower()),token_set_ratio(t["symbol"].lower(),x["title"].lower()))
  if s>best[0]: best=(s,x)
 relation=best[0]
 timing=100 if (t["age"] is not None and t["age"]<=10) else 75
 market=min(100,t["liquidity"]/10000*50+t["volume5m"]/2500*50)
 total=.55*relation+.2*timing+.2*market+.05*min(100,t["buys5m"]*5)
 return round(total,1),relation,best[1]
