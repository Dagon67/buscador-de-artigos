from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import feedparser
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI(
    title="Academic Papers Search API",
    description="API for searching academic papers across multiple sources",
    version="1.0.0"
)

class SearchQuery(BaseModel):
    query: str
    max_results: Optional[int] = 10

class ArticleBase(BaseModel):
    title: str
    abstract: Optional[str] = None
    url: Optional[str] = None
    published: Optional[str] = None
    source: str

class SearchResponse(BaseModel):
    source: str
    results: List[ArticleBase]
    error: Optional[str] = None

# PubMed Search
def search_pubmed(query: str, max_results: int = 10) -> SearchResponse:
    API_KEY = os.getenv("PUBMED_API_KEY")
    EMAIL = os.getenv("PUBMED_EMAIL")
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    try:
        # Search for article IDs
        search_url = f"{base_url}esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "api_key": API_KEY,
            "retmode": "json",
            "email": EMAIL
        }
        response = requests.get(search_url, params=params)
        data = response.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])
        
        if not id_list:
            return SearchResponse(source="PubMed", results=[], error="No results found")
        
        # Fetch article details
        fetch_url = f"{base_url}efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "xml",
            "api_key": API_KEY,
            "email": EMAIL
        }
        response = requests.get(fetch_url, params=params)
        
        # Parse XML response
        root = ET.fromstring(response.text)
        articles = []
        
        for article in root.findall(".//PubmedArticle"):
            title = article.find(".//ArticleTitle")
            abstract = article.find(".//Abstract/AbstractText")
            pmid = article.find(".//PMID")
            
            articles.append(ArticleBase(
                title=title.text if title is not None else "No title",
                abstract=abstract.text if abstract is not None else None,
                url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid.text}/" if pmid is not None else None,
                source="PubMed"
            ))
            
        return SearchResponse(source="PubMed", results=articles)
    
    except Exception as e:
        return SearchResponse(source="PubMed", results=[], error=str(e))

# OpenAlex Search
def search_openalex(query: str, max_results: int = 10) -> SearchResponse:
    try:
        # For latest papers, use date sorting
        if query == "*":
            url = f"https://api.openalex.org/works?sort=publication_date:desc&per_page={max_results}"
        else:
            url = f"https://api.openalex.org/works?search={query}&per_page={max_results}"
        
        response = requests.get(url)
        data = response.json()
        
        articles = []
        for work in data.get("results", []):
            articles.append(ArticleBase(
                title=work.get("title", "No title"),
                abstract=work.get("abstract", None),
                url=work.get("doi", None),
                published=work.get("publication_date", None),
                source="OpenAlex"
            ))
            
        return SearchResponse(source="OpenAlex", results=articles)
    
    except Exception as e:
        return SearchResponse(source="OpenAlex", results=[], error=str(e))

# Semantic Scholar Search
def search_semantic_scholar(query: str, max_results: int = 10) -> SearchResponse:
    try:
        # For latest papers, use date sorting
        if query == "*":
            # Use a recent year to get latest papers
            current_year = datetime.now().year
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query=year:{current_year}&limit={max_results}&sort=publicationDate:desc"
        else:
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={max_results}"
        
        response = requests.get(url)
        data = response.json()
        
        articles = []
        for paper in data.get("data", []):
            articles.append(ArticleBase(
                title=paper.get("title", "No title"),
                abstract=paper.get("abstract", None),
                url=paper.get("url", None),
                published=str(paper.get("year", "")),  # Convert to string to avoid type issues
                source="Semantic Scholar"
            ))
            
        return SearchResponse(source="Semantic Scholar", results=articles)
    
    except Exception as e:
        return SearchResponse(source="Semantic Scholar", results=[], error=str(e))

# CrossRef Search
def search_crossref(query: str, max_results: int = 10) -> SearchResponse:
    try:
        # For latest papers, use date sorting
        if query == "*":
            url = f"https://api.crossref.org/works?sort=published&order=desc&rows={max_results}"
        else:
            url = f"https://api.crossref.org/works?query={query}&rows={max_results}"
        
        response = requests.get(url)
        data = response.json()
        
        articles = []
        for work in data.get("message", {}).get("items", []):
            # Handle date parts properly
            date_parts = work.get("published-print", {}).get("date-parts", [[]])[0]
            published = str(date_parts[0]) if date_parts else None
            
            articles.append(ArticleBase(
                title=work.get("title", ["No title"])[0],
                abstract=None,  # CrossRef doesn't provide abstracts
                url=work.get("URL", None),
                published=published,
                source="CrossRef"
            ))
            
        return SearchResponse(source="CrossRef", results=articles)
    
    except Exception as e:
        return SearchResponse(source="CrossRef", results=[], error=str(e))

# arXiv Search with date sorting
def search_arxiv(query: str, max_results: int = 10) -> SearchResponse:
    try:
        # For latest papers, we use a date range if no specific query is provided
        if query == "*":
            # Get papers from the last 7 days
            today = datetime.now()
            last_week = today - timedelta(days=7)
            date_query = f"submittedDate:[{last_week.strftime('%Y%m%d')}000000 TO {today.strftime('%Y%m%d')}235959]"
            query = date_query

        # Add sorting by submission date
        url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&start=0&max_results={max_results}"
        response = requests.get(url)
        feed = feedparser.parse(response.content)
        
        articles = []
        for entry in feed.entries:
            articles.append(ArticleBase(
                title=entry.title,
                abstract=entry.summary,
                url=entry.link,
                published=entry.published,
                source="arXiv"
            ))
            
        return SearchResponse(source="arXiv", results=articles)
    
    except Exception as e:
        return SearchResponse(source="arXiv", results=[], error=str(e))

# Article Scraping
def scrape_article(url: str) -> ArticleBase:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        title = soup.title.string if soup.title else "No title"
        
        # Try to find abstract
        abstract = None
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc and meta_desc.get("content"):
            abstract = meta_desc.get("content")
        else:
            abstract_tag = soup.find(lambda tag: tag.name in ["div", "p"] and 
                                   (tag.get("id") and "abstract" in tag.get("id").lower() or 
                                    tag.get("class") and any("abstract" in c.lower() for c in tag.get("class"))))
            if abstract_tag:
                abstract = abstract_tag.get_text(strip=True)
        
        return ArticleBase(
            title=title,
            abstract=abstract,
            url=url,
            source="Web Scraping"
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API Endpoints
@app.post("/search/{source}", response_model=SearchResponse)
async def search_papers(source: str, query: SearchQuery):
    source = source.lower()
    search_functions = {
        "pubmed": search_pubmed,
        "openalex": search_openalex,
        "semanticscholar": search_semantic_scholar,
        "crossref": search_crossref,
        "arxiv": search_arxiv
    }
    
    if source not in search_functions:
        raise HTTPException(status_code=400, detail=f"Invalid source. Available sources: {', '.join(search_functions.keys())}")
    
    return search_functions[source](query.query, query.max_results)

@app.post("/search/all", response_model=List[SearchResponse])
async def search_all_sources(query: SearchQuery):
    results = []
    for source in ["pubmed", "openalex", "semanticscholar", "crossref", "arxiv"]:
        result = await search_papers(source, query)
        results.append(result)
    return results

@app.post("/scrape", response_model=ArticleBase)
async def scrape_article_endpoint(url: str):
    return scrape_article(url)

# New endpoint for latest articles
@app.get("/latest", response_model=List[SearchResponse])
async def get_latest_articles(max_results: int = 10, query: str = "*"):
    results = []
    
    # Get latest from arXiv
    arxiv_result = search_arxiv(query, max_results)
    results.append(arxiv_result)
    
    # Get latest from PubMed
    pubmed_result = search_pubmed(query, max_results)
    results.append(pubmed_result)
    
    # Get latest from OpenAlex
    openalex_result = search_openalex(query, max_results)
    results.append(openalex_result)
    
    # Get latest from Semantic Scholar
    semantic_result = search_semantic_scholar(query, max_results)
    results.append(semantic_result)
    
    # Get latest from CrossRef
    crossref_result = search_crossref(query, max_results)
    results.append(crossref_result)
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 