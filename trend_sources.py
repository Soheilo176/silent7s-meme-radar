import feedparser
def candidates(urls):
 out=[]
 for u in urls:
  try:
   f=feedparser.parse(u)
   for e in f.entries[:100]:
    t=(e.get("title") or "").strip()
    if t: out.append({"title":t,"link":e.get("link","")})
  except Exception: pass
 return out
