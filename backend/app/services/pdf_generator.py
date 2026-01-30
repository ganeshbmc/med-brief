import html
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
                font-family: 'Charter', 'Bitstream Charter', Georgia, 'Times New Roman', serif;
                font-size: 11pt;
                line-height: 1.65;
                margin: 0.5in;
                color: #1a1a1a;
            }}

            .page-header {{
                position: fixed;
                top: 0.35in;
                left: 0.5in;
                right: 0.5in;
                font-size: 9pt;
                color: #666666;
                border-bottom: 1pt solid #e0e0e0;
                padding-bottom: 8pt;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
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
                margin-top: 0.7in;
            }}

            .header {{
                margin-bottom: 40pt;
                border-bottom: 2pt solid #e07a5f;
                padding-bottom: 10pt;
            }}

            .header h1 {{
                font-size: 18pt;
                margin: 0;
                font-weight: 600;
                color: #1a1a1a;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
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
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                page-break-after: avoid;
            }}

            .toc-journal-header {{
                font-size: 12pt;
                font-weight: 600;
                margin-bottom: 12pt;
                margin-top: 16pt;
                color: #1a1a1a;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                page-break-inside: avoid;
            }}

            .toc-article-entry {{
                font-size: 10pt;
                margin-bottom: 6pt;
                margin-left: 20pt;
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                page-break-inside: avoid;
            }}

            .toc-article-link {{
                flex: 1;
                color: #C65D45;
                text-decoration: none;
                font-weight: 500;
            }}

            .toc-article-link:hover {{
                text-decoration: underline;
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
                font-size: 9pt;
            }}

            .toc-section-spacer {{
                margin-bottom: 20pt;
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
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                page-break-after: avoid;
            }}

            .article {{
                margin-bottom: 36pt;
                page-break-inside: avoid;
            }}

            .article-journal {{
                font-size: 10pt;
                font-weight: 600;
                margin-bottom: 6pt;
                color: #666666;
                text-transform: uppercase;
                letter-spacing: 0.5pt;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
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
                color: #C65D45;
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
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            }}

            .abstract-text {{
                text-align: justify;
                font-size: 10pt;
                line-height: 1.75;
                text-indent: 0;
                white-space: pre-wrap;
            }}

            .divider {{
                border-top: 0.5pt solid #e7e2dc;
                margin: 22pt 0;
                page-break-inside: avoid;
            }}

            @page {{
                margin: 0.5in;
                @top {{
                    content: element(pageHeader);
                }}
                @bottom-center {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 9pt;
                    color: #666666;
                    font-family: 'Charter', 'Bitstream Charter', Georgia, 'Times New Roman', serif;
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

    toc_sections = []
    article_num = 1  # Track article numbering for anchors

    for journal_name in sorted(journals.keys()):
        articles = journals[journal_name]

        # Journal header
        toc_sections.append(f"""
            <div class="toc-journal-header">{journal_name}</div>
        """)

        # Article entries under this journal
        for article in articles:
            title = article.get('title', 'Untitled')
            # Truncate long titles
            if len(title) > 80:
                title = title[:77] + "..."

            toc_sections.append(f"""
                <div class="toc-article-entry">
                    <a href="#article-{article_num}" class="toc-article-link">{title}</a>
                    <span class="toc-dots"></span>
                    <span class="toc-page">{article_num}</span>
                </div>
            """)
            article_num += 1

        # Add spacing between journal sections
        if journal_name != list(sorted(journals.keys()))[-1]:
            toc_sections.append('<div class="toc-section-spacer"></div>')

    return f"""
        <div class="toc-header">Table of Contents</div>
        {"".join(toc_sections)}
        <div style="page-break-after: always;"></div>
    """


def _generate_articles_content(journals: Dict[str, List[Dict[str, Any]]]) -> str:
    """Generate articles content HTML."""
    html_parts = []
    article_num = 1  # Track article numbering for anchors

    for journal_name in sorted(journals.keys()):
        articles = journals[journal_name]

        journal_html = f"""
            <div class="journal-section">
                <div class="journal-name">{journal_name}</div>
        """

        for article in articles:
            journal_html += _generate_article_html(article, article_num)
            article_num += 1

        journal_html += "</div>"

        # Add page break between journals (except for the last one)
        if journal_name != list(sorted(journals.keys()))[-1]:
            journal_html += '<div style="page-break-after: always;"></div>'

        html_parts.append(journal_html)

    return "".join(html_parts)


def _generate_article_html(article: Dict[str, Any], article_num: int) -> str:
    """Generate HTML for a single article."""

    title = article.get('title', 'No Title')
    journal = article.get('journal', 'Unknown Journal')
    authors_list = article.get('authors', [])
    pub_date = article.get('pub_date', 'No Date')
    pubmed_id = article.get('pmid')
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

    def _escape_html(value: str) -> str:
        return html.escape(value, quote=True)

    safe_title = _escape_html(str(title))
    safe_journal = _escape_html(str(journal))
    safe_authors = _escape_html(str(authors_display))
    safe_date = _escape_html(str(formatted_date))

    links_html = ""
    if pubmed_id:
        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
        safe_pubmed_url = _escape_html(pubmed_url)
        safe_pubmed_id = _escape_html(str(pubmed_id))
        links_html += f'<a href="{safe_pubmed_url}" class="link">PMID: {safe_pubmed_id}</a>'
    if doi:
        doi_url = f"https://doi.org/{doi}"
        safe_doi_url = _escape_html(doi_url)
        safe_doi = _escape_html(str(doi))
        links_html += f'<a href="{safe_doi_url}" class="link">DOI: {safe_doi}</a>'

    abstract_html = ""
    if abstract and abstract.strip():
        safe_abstract = _escape_html(str(abstract))
        abstract_html = f"""
            <div class="abstract">
                <div class="abstract-label">Abstract</div>
                <div class="abstract-text">{safe_abstract}</div>
            </div>
        """
    else:
        abstract_html = f"""
            <div class="abstract">
                <div class="abstract-label">Abstract</div>
                <div class="abstract-text">No abstract available for this article.</div>
            </div>
        """

    article_html = f"""
            <div id="article-{article_num}" class="article">
                <div class="article-journal">{safe_journal}</div>
                <div class="article-title">{safe_title}</div>
                <div class="article-meta">
                    <div class="authors">{safe_authors}</div>
                    <div class="published">Published: {safe_date}</div>
                    <div class="links">{links_html}</div>
                </div>
                {abstract_html}
            </div>
            <div class="divider"></div>
    """

    return article_html
