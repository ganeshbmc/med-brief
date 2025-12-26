"""
PubMed Entrez API service for fetching articles.
"""
import httpx
from datetime import date
from typing import List
from xml.etree import ElementTree
import asyncio

from app.config import settings

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


async def fetch_articles_for_journals(
    issns: List[str],
    start_date: date,
    end_date: date,
) -> List[dict]:
    """
    Fetch recent articles from PubMed for the given journal ISSNs.
    Returns list of article dicts with pmid, title, authors, journal, pub_date, abstract, pubmed_url.
    """
    if not issns:
        return []

    # Build query: (ISSN1[ISSN] OR ISSN2[ISSN]) AND date_range
    issn_query = " OR ".join([f'"{issn}"[ISSN]' for issn in issns])
    date_range = f'("{start_date.strftime("%Y/%m/%d")}"[PDAT] : "{end_date.strftime("%Y/%m/%d")}"[PDAT])'
    query = f"({issn_query}) AND {date_range}"

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Step 1: ESearch to get PMIDs (sorted by publication date, newest first)
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": 500,
            "sort": "pub_date",  # Sort by publication date (newest first)
            "usehistory": "y",
            "email": settings.PUBMED_EMAIL,
            "retmode": "json",
        }
        try:
            search_resp = await client.get(ESEARCH_URL, params=search_params)
            search_data = search_resp.json()
        except Exception as e:
            print(f"PubMed search error: {e}")
            return []

        esearch_result = search_data.get("esearchresult", {})
        
        # Check for errors in the response
        if "error" in esearch_result:
            print(f"PubMed error: {esearch_result['error']}")
            return []
        
        id_list = esearch_result.get("idlist", [])
        count = esearch_result.get("count", "0")
        print(f"PubMed query returned {count} total results, fetching {len(id_list)} articles")
        
        if not id_list:
            return []

        # Rate limit: wait 350ms between requests (< 3/sec)
        await asyncio.sleep(0.35)

        # Step 2: EFetch to get article details (batch in chunks to avoid URI too long)
        all_articles = []
        batch_size = 100
        
        for i in range(0, len(id_list), batch_size):
            batch_ids = id_list[i:i + batch_size]
            
            # Rate limit: wait 350ms between requests (<3/sec)
            if i > 0:
                await asyncio.sleep(0.35)
            
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(batch_ids),
                "rettype": "xml",
                "email": settings.PUBMED_EMAIL,
            }
            try:
                fetch_resp = await client.get(EFETCH_URL, params=fetch_params)
                batch_articles = _parse_pubmed_xml(fetch_resp.text)
                all_articles.extend(batch_articles)
                print(f"Fetched batch {i//batch_size + 1}: {len(batch_articles)} articles")
            except Exception as e:
                print(f"EFetch error for batch {i//batch_size + 1}: {e}")
                continue  # Continue with other batches even if one fails
        
        print(f"Total articles fetched: {len(all_articles)}")

    return all_articles


def _parse_pubmed_xml(xml_text: str) -> List[dict]:
    """Parse PubMed XML response into article dicts."""
    articles = []
    try:
        root = ElementTree.fromstring(xml_text)
        for article in root.findall(".//PubmedArticle"):
            pmid = article.findtext(".//PMID", "")
            title = article.findtext(".//ArticleTitle", "")
            journal = article.findtext(".//Journal/Title", "")

            # Authors
            authors = []
            for author in article.findall(".//Author"):
                last = author.findtext("LastName", "")
                fore = author.findtext("ForeName", "")
                if last:
                    authors.append(f"{fore} {last}".strip())

            # Date
            pub_date_elem = article.find(".//PubDate")
            if pub_date_elem is not None:
                year = pub_date_elem.findtext("Year", "")
                month = pub_date_elem.findtext("Month", "")
                day = pub_date_elem.findtext("Day", "")
                pub_date = f"{year}-{month}-{day}".strip("-")
            else:
                pub_date = ""

            # Abstract - join all AbstractText elements (for structured abstracts)
            abstract_parts = []
            for abs_elem in article.findall(".//AbstractText"):
                label = abs_elem.get("Label", "")
                text = abs_elem.text or ""
                if label:
                    abstract_parts.append(f"{label}: {text}")
                else:
                    abstract_parts.append(text)
            abstract = " ".join(abstract_parts) if abstract_parts else ""

            # DOI
            doi = ""
            for eloc in article.findall(".//ELocationID"):
                if eloc.get("EIdType") == "doi":
                    doi = eloc.text or ""
                    break

            articles.append({
                "pmid": pmid,
                "title": title,
                "authors": authors,
                "journal": journal,
                "pub_date": pub_date,
                "abstract": abstract,
                "doi": doi,
                "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            })
    except Exception:
        pass  # Return empty list on parse error
    return articles
