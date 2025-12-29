"""
NLM Catalog Service - Search for journals in NCBI's NLM Catalog.
Uses NCBI E-utilities API: https://www.ncbi.nlm.nih.gov/books/NBK25500/
"""
import httpx
import xml.etree.ElementTree as ET
from typing import List, Optional
from pydantic import BaseModel


class NLMJournal(BaseModel):
    """Journal data from NLM Catalog."""
    name: str
    issn: Optional[str] = None
    iso_abbreviation: Optional[str] = None
    nlm_id: Optional[str] = None


EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


async def search_nlm_journals(query: str, limit: int = 20) -> List[NLMJournal]:
    """
    Search NLM Catalog for journals matching the query.
    
    Args:
        query: Search term (journal name or ISSN)
        limit: Maximum number of results to return
        
    Returns:
        List of NLMJournal objects, sorted with exact matches first
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Detect if query is an ISSN (8 digits, optionally with hyphen)
        issn_pattern = query.replace("-", "").strip()
        is_issn = len(issn_pattern) == 8 and issn_pattern.isdigit()
        
        if is_issn:
            # Format as ISSN for search (####-####)
            formatted_issn = f"{issn_pattern[:4]}-{issn_pattern[4:]}"
            search_term = f'{formatted_issn}[ISSN]'
            fetch_limit = limit  # ISSN searches are precise
        else:
            # Search NLM Catalog using correct field tags:
            # [ti] = Title, [ta] = Title Abbreviation
            search_term = f'("{query}"[ti] OR "{query}"[ta])'
            fetch_limit = limit * 3  # Fetch more to filter/sort
        
        # Step 1: Search for journal IDs
        search_url = f"{EUTILS_BASE}/esearch.fcgi"
        search_params = {
            "db": "nlmcatalog",
            "term": search_term,
            "retmax": fetch_limit,
            "retmode": "json",
        }
        
        try:
            search_resp = await client.get(search_url, params=search_params)
            search_resp.raise_for_status()
            search_data = search_resp.json()
        except Exception as e:
            print(f"NLM search error: {e}")
            return []
        
        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return []
        
        # Step 2: Fetch details for each ID
        fetch_url = f"{EUTILS_BASE}/efetch.fcgi"
        fetch_params = {
            "db": "nlmcatalog",
            "id": ",".join(id_list),
            "rettype": "xml",
        }
        
        try:
            fetch_resp = await client.get(fetch_url, params=fetch_params)
            fetch_resp.raise_for_status()
        except Exception as e:
            print(f"NLM fetch error: {e}")
            return []
        
        # Parse XML response
        journals = _parse_nlm_response(fetch_resp.text)
        
        # Filter: Only include journals with ISSN (more likely to be valid PubMed journals)
        journals = [j for j in journals if j.issn]
        
        # Sort: Prioritize exact title matches, then shorter titles (more likely to be the main journal)
        query_lower = query.lower().strip()
        def sort_key(j):
            name_lower = j.name.lower()
            # Exact match gets highest priority (0)
            if name_lower == query_lower:
                return (0, len(j.name))
            # Starts with query gets second priority (1)
            if name_lower.startswith(query_lower):
                return (1, len(j.name))
            # Contains query somewhere (2)
            return (2, len(j.name))
        
        journals.sort(key=sort_key)
        
        return journals[:limit]


def _parse_nlm_response(xml_text: str) -> List[NLMJournal]:
    """Parse NLM Catalog XML response into journal objects."""
    journals = []
    
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
        return []
    
    # NLM Catalog returns NLMCatalogRecord elements
    for record in root.findall(".//NLMCatalogRecord"):
        try:
            # Get title
            title_elem = record.find(".//TitleMain/Title")
            if title_elem is None or not title_elem.text:
                continue
            name = title_elem.text.strip()
            
            # Get ISSN (prefer print ISSN)
            issn = None
            for issn_elem in record.findall(".//ISSN"):
                issn = issn_elem.text
                if issn_elem.get("IssnType") == "Print":
                    break
            
            # Get ISO abbreviation
            iso_abbr = None
            iso_elem = record.find(".//ISOAbbreviation")
            if iso_elem is not None and iso_elem.text:
                iso_abbr = iso_elem.text.strip()
            
            # Get NLM Unique ID
            nlm_id = None
            nlm_id_elem = record.find(".//NlmUniqueID")
            if nlm_id_elem is not None and nlm_id_elem.text:
                nlm_id = nlm_id_elem.text.strip()
            
            journals.append(NLMJournal(
                name=name,
                issn=issn,
                iso_abbreviation=iso_abbr,
                nlm_id=nlm_id,
            ))
        except Exception as e:
            print(f"Error parsing record: {e}")
            continue
    
    return journals
