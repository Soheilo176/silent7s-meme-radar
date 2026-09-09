import time, requests
BASE="https://api.dexscreener.com"
def latest_solana_profiles():
 r=requests.get(BASE+"/token-profiles/latest/v1",timeout=15); r.raise_for_status()
 return [x for x in r.json() if x.get("chainId")=="solana"]
def normalize(p):
 a=p.get("tokenAddress")
 r=requests.get(f"{BASE}/token-pairs/v1/solana/{a}",timeout=15); pairs=r.json() or []
 best=max(pairs,key=lambda x:float((x.get("liquidity") or {}).get("usd") or 0),default={})
 b=best.get("baseToken") or {}; created=best.get("pairCreatedAt")
 age=(time.time()*1000-created)/60000 if created else None
 return {"address":a,"name":b.get("name",""),"symbol":b.get("symbol",""),"icon":p.get("icon") or (best.get("info") or {}).get("imageUrl"),"url":best.get("url") or p.get("url"),"liquidity":float((best.get("liquidity") or {}).get("usd") or 0),"volume5m":float((best.get("volume") or {}).get("m5") or 0),"buys5m":int((best.get("txns") or {}).get("m5",{}).get("buys") or 0),"sells5m":int((best.get("txns") or {}).get("m5",{}).get("sells") or 0),"age":age}
