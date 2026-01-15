import weasyprint
from datetime import datetime
from typing import List, Dict, Any
from app.config import settings


def generate_brief_pdf(articles: List[Dict[str, Any]], profile_name: str = "MedBrief Summary") -> bytes:
    """
    Generate PDF from articles list.

    Args:
        articles: List of article dictionaries with keys:
                 title, authors, journal, pub_date, doi, abstract
        profile_name: Name of the brief/profile

    Returns:
        PDF content as bytes
    """
    # Sort articles by journal name alphabetically
    sorted_articles = sorted(articles, key=lambda x: x.get('journal', '').lower())

    # Generate HTML content
    html_content = _generate_html_content(sorted_articles, profile_name)

    # Convert HTML to PDF
    html_doc = weasyprint.HTML(string=html_content)
    pdf_bytes = html_doc.write_pdf()

    return pdf_bytes


def _generate_html_content(articles: List[Dict[str, Any]], profile_name: str) -> str:
    """Generate HTML content for PDF."""

    # Group articles by journal
    journals = {}
    for article in articles:
        journal = article.get('journal', 'Unknown Journal')
        if journal not in journals:
            journals[journal] = []
        journals[journal].append(article)

    # Generate table of contents if multiple journals
    toc_html = ""
    if len(journals) > 1:
        toc_html = _generate_table_of_contents(journals)

    # Generate articles content
    articles_html = _generate_articles_content(journals)

    # Generate complete HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{profile_name}</title>
        <style>
            @font-face {{
                font-family: 'Charter';
                src: local('Bitstream Charter'), local('Charter');
            }}

            body {{
                font-family: 'Charter', 'Bitstream Charter', Georgia, serif;
                font-size: 11pt;
                line-height: 1.6;
                margin: 1in;
                color: #1a1a1a;
            }}

            .page-header {{
                position: fixed;
                top: 0.5in;
                left: 1in;
                right: 1in;
                font-size: 9pt;
                color: #666666;
                border-bottom: 1pt solid #e0e0e0;
                padding-bottom: 8pt;
                font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
                font-weight: 500;
            }}

            .page-header-content {{
                display: flex;
                justify-content: space-between;
                align-items: baseline;
            }}

            .page-title {{
                font-weight: 600;
            }}

            .page-number {{
                font-weight: 400;
            }}

            .content {{
                margin-top: 0.8in;
            }}

            .header {{
                margin-bottom: 48pt;
                border-bottom: 2pt solid #e07a5f;
                padding-bottom: 12pt;
            }}

            .header h1 {{
                font-size: 18pt;
                margin: 0;
                font-weight: 600;
                color: #1a1a1a;
                font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
                letter-spacing: -0.3px;
            }}

            .generated-date {{
                font-size: 9pt;
                color: #666666;
                margin-top: 6pt;
                font-weight: 500;
            }}

            .toc-header {{
                font-size: 16pt;
                font-weight: 600;
                margin-bottom: 24pt;
                text-align: center;
                font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
                page-break-after: avoid;
            }}

            .toc-entry {{
                font-size: 11pt;
                margin-bottom: 8pt;
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                page-break-inside: avoid;
            }}

            .toc-journal {{
                flex: 1;
                font-weight: 500;
            }}

            .toc-dots {{
                flex: 1;
                border-bottom: 1pt dotted #999;
                margin: 0 12pt;
                position: relative;
                top: -4pt;
            }}

            .toc-page {{
                font-weight: 600;
                color: #666666;
            }}

            .journal-section {{
                margin-bottom: 48pt;
                page-break-inside: avoid;
            }}

            .journal-name {{
                font-size: 14pt;
                font-weight: 600;
                margin-bottom: 20pt;
                color: #1a1a1a;
                font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
                page-break-after: avoid;
            }}

            .article {{
                margin-bottom: 36pt;
                page-break-inside: avoid;
            }}

            .article-title {{
                font-size: 13pt;
                font-weight: 600;
                margin-bottom: 8pt;
                line-height: 1.4;
                color: #1a1a1a;
            }}

            .article-meta {{
                font-size: 10pt;
                margin-bottom: 16pt;
                color: #4a4a4a;
                line-height: 1.5;
            }}

            .authors {{
                margin-bottom: 6pt;
            }}

            .published {{
                margin-bottom: 6pt;
            }}

            .links {{
                margin-bottom: 16pt;
            }}

            .link {{
                margin-right: 16pt;
                color: #2563eb;
                text-decoration: none;
                font-weight: 500;
            }}

            .link:hover {{
                text-decoration: underline;
            }}

            .abstract {{
                margin-top: 16pt;
            }}

            .abstract-label {{
                font-weight: 600;
                font-size: 10pt;
                margin-bottom: 6pt;
                font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
            }}

            .abstract-text {{
                text-align: justify;
                font-size: 10pt;
                line-height: 1.7;
                text-indent: 0;
            }}

            .divider {{
                border-top: 0.5pt solid #d0d0d0;
                margin: 24pt 0;
                page-break-inside: avoid;
            }}

            @page {{
                margin: 1in;
                @top {{
                    content: element(pageHeader);
                }}
                @bottom-center {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 9pt;
                    color: #666666;
                    font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
                    font-weight: 500;
                }}
            }}

            .page-header {{
                position: running(pageHeader);
            }}
        </style>
    </head>
    <body>
        <div class="page-header">
            <div class="page-header-content">
                <span class="page-title">MedBrief</span>
                <span class="page-number">Page <span class="page-num"></span></span>
            </div>
        </div>

        <div class="content">
            <div class="header">
                <h1>{profile_name}</h1>
                <div class="generated-date">Generated: {datetime.now().strftime('%B %d, %Y')}</div>
            </div>

            {toc_html}

            {articles_html}
        </div>
    </body>
    </html>
    """

    return html


def _generate_table_of_contents(journals: Dict[str, List[Dict[str, Any]]]) -> str:
    """Generate table of contents HTML."""
    if len(journals) <= 1:
        return ""

    toc_entries = []
    page_num = 2  # ToC starts on page 1, articles on page 2

    for journal_name in sorted(journals.keys()):
        toc_entries.append(f"""
            <div class="toc-entry">
                <span class="toc-journal">{journal_name}</span>
                <span class="toc-dots"></span>
                <span class="toc-page">{page_num}</span>
            </div>
        """)
        page_num += 1  # Each journal gets its own page

    return f"""
        <div class="toc-header">Table of Contents</div>
        {"".join(toc_entries)}
        <div style="page-break-after: always;"></div>
    """


def _generate_articles_content(journals: Dict[str, List[Dict[str, Any]]]) -> str:
    """Generate articles content HTML."""
    html_parts = []

    for journal_name in sorted(journals.keys()):
        articles = journals[journal_name]

        journal_html = f"""
            <div class="journal-section">
                <div class="journal-name">{journal_name}</div>
        """

        for article in articles:
            journal_html += _generate_article_html(article)

        journal_html += "</div>"

        # Add page break between journals (except for the last one)
        if journal_name != list(sorted(journals.keys()))[-1]:
            journal_html += '<div style="page-break-after: always;"></div>'

        html_parts.append(journal_html)

    return "".join(html_parts)


def _generate_article_html(article: Dict[str, Any]) -> str:
    """Generate HTML for a single article."""

    title = article.get('title', 'No Title')
    authors_list = article.get('authors', [])
    pub_date = article.get('pub_date', 'No Date')
    pubmed_id = article.get('pubmed_id')
    doi = article.get('doi')
    abstract = article.get('abstract')

    # Format authors (truncate with et al. like in the UI)
    if authors_list and len(authors_list) > 0:
        if len(authors_list) <= 3:
            authors_display = ', '.join(authors_list)
        else:
            authors_display = ', '.join(authors_list[:3]) + ' et al.'
    else:
        authors_display = 'No authors listed'

    # Format date
    try:
        if isinstance(pub_date, str):
            # Try to parse and reformat date
            parsed_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
            formatted_date = parsed_date.strftime('%B %d, %Y')
        else:
            formatted_date = str(pub_date)
    except:
        formatted_date = str(pub_date)

    links_html = ""
    if pubmed_id:
        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
        links_html += f'<a href="{pubmed_url}" class="link">PMID: {pubmed_id}</a>'
    if doi:
        doi_url = f"https://doi.org/{doi}"
        links_html += f'<a href="{doi_url}" class="link">DOI: {doi}</a>'

    abstract_html = ""
    if abstract and abstract.strip():
        abstract_html = f"""
            <div class="abstract">
                <div class="abstract-label">Abstract</div>
                <div class="abstract-text">{abstract}</div>
            </div>
        """
    else:
        abstract_html = f"""
            <div class="abstract">
                <div class="abstract-label">Abstract</div>
                <div class="abstract-text">No abstract available for this article.</div>
            </div>
        """

    html = f"""
            <div class="article">
                <div class="article-title">{title}</div>
                <div class="article-meta">
                    <div class="authors">{authors_display}</div>
                    <div class="published">Published: {formatted_date}</div>
                    <div class="links">{links_html}</div>
                </div>
                {abstract_html}
            </div>
            <div class="divider"></div>
    """

    return html