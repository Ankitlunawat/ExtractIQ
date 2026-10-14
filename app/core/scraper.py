import hashlib,json,re,time
from decimal import Decimal
from urllib.parse import urljoin,urlparse
from urllib.robotparser import RobotFileParser
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
SOURCE="https://books.toscrape.com/"
def allowed(url):
    p=urlparse(url)
    if p.scheme!="https" or p.netloc!="books.toscrape.com" or p.username or p.password:raise ValueError("Source is not approved.")
    return url
def parse_page(html,url):
    soup=BeautifulSoup(html,"html.parser")
    cards=soup.select("article.product_pod")
    if not cards:raise ValueError("No product cards found. Check the source adapter.")
    rows=[];rejected=0
    for card in cards:
        try:
            a=card.select_one("h3 a");title=" ".join(a["title"].split())
            price=Decimal(re.sub(r"[^0-9.]","",card.select_one(".price_color").get_text()))
            if not title or not price.is_finite() or price<0:raise ValueError("Invalid record")
            link=allowed(urljoin(url,a["href"]))
            rating=next((i for i,w in enumerate(["One","Two","Three","Four","Five"],1) if w in card.select_one(".star-rating").get("class",[])),0)
            if not rating:raise ValueError("Missing rating")
            rows.append({"title":title,"url":link,"price":str(price),"currency":"GBP","rating":rating,"available":"In stock" in card.select_one(".availability").get_text(),"fingerprint":hashlib.sha256(link.encode()).hexdigest()})
        except (AttributeError,KeyError,ValueError,ArithmeticError):rejected+=1
    next_link=soup.select_one("li.next a")
    return rows,allowed(urljoin(url,next_link["href"])) if next_link else None,rejected
def crawl(pages=2,cache=None):
    if not 1<=pages<=5:raise ValueError("Choose 1–5 pages.")
    session=requests.Session()
    session.headers.update({"User-Agent":"ExtractIQ-Portfolio/1.0"})
    session.mount("https://",HTTPAdapter(max_retries=Retry(total=2,backoff_factor=1,status_forcelist=[429,500,502,503,504],allowed_methods=["GET"])))
    robot=RobotFileParser()
    robots=session.get(SOURCE+"robots.txt",timeout=20,allow_redirects=False)
    if robots.status_code==404:robot.parse(["User-agent: *","Disallow:"])
    else:
        robots.raise_for_status()
        if robots.status_code!=200:raise ValueError("Unexpected robots response")
        robot.parse(robots.text.splitlines())
    url=SOURCE;seen={};duplicates=0;rejected=0;count=0;visited=set()
    while url and count<pages:
        allowed(url)
        if url in visited:raise ValueError("Pagination loop detected")
        if not robot.can_fetch("ExtractIQ-Portfolio",url):raise ValueError("Source disallows crawling")
        visited.add(url)
        response=session.get(url,timeout=20,allow_redirects=False)
        response.raise_for_status()
        if response.status_code!=200:raise ValueError("Unexpected redirect")
        response.encoding="utf-8";html=response.text
        if cache:
            folder=Path(cache);folder.mkdir(parents=True,exist_ok=True);(folder/f"page-{count+1}.html").write_text(html)
        rows,url,bad=parse_page(html,url);rejected+=bad;count+=1
        for row in rows:
            if row["fingerprint"] in seen:duplicates+=1
            else:seen[row["fingerprint"]]=row
        if url and count<pages:time.sleep(1)
    return list(seen.values()),{"pages":count,"duplicates":duplicates,"rejected":rejected}
