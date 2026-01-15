import weasyprint
from datetime import datetime
from typing import List, Dict, Any
from app.config import settings


def generate_brief_pdf(articles: List[Dict[str, Any]], profile_name: str = "MedBrief Summary") -> bytes:
    """
    Generate PDF from articles list.

    Args:
        articles: List of article dictionaries with keys:
                 title, authors, journal, pub_date, pubmed_id, doi, abstract
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

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{profile_name}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                margin: 50px;
                color: #1f2937;
                background: #ffffff;
            }}

            .header {{
                text-align: center;
                margin-bottom: 40px;
                border-bottom: 3px solid #e07a5f;
                padding-bottom: 25px;
                background: linear-gradient(135deg, #fef7f5 0%, #ffffff 100%);
                padding: 30px;
                border-radius: 8px;
                margin-left: -30px;
                margin-right: -30px;
                margin-bottom: 50px;
            }}

            .header h1 {{
                font-size: 28pt;
                margin: 0;
                font-weight: 600;
                color: #1f2937;
                letter-spacing: -0.5px;
            }}

            .generated-date {{
                font-size: 10pt;
                color: #6b7280;
                margin-top: 8px;
                font-weight: 500;
            }}

            .journal-section {{
                margin-bottom: 45px;
                page-break-inside: avoid;
                background: #fafafa;
                padding: 25px;
                border-radius: 6px;
                border-left: 4px solid #e07a5f;
            }}

            .journal-name {{
                font-size: 16pt;
                font-weight: 600;
                margin-bottom: 15px;
                color: #e07a5f;
                border-bottom: 2px solid #f3f4f6;
                padding-bottom: 8px;
                letter-spacing: -0.2px;
            }}

            .article-title {{
                font-size: 14pt;
                font-weight: 600;
                margin-bottom: 12px;
                line-height: 1.3;
                color: #1f2937;
            }}

            .article-meta {{
                margin-bottom: 15px;
                font-size: 10.5pt;
                line-height: 1.4;
            }}

            .authors {{
                margin-bottom: 6px;
                color: #374151;
            }}

            .published {{
                margin-bottom: 6px;
                color: #6b7280;
                font-weight: 500;
            }}

            .links {{
                margin-bottom: 15px;
            }}

            .link {{
                margin-right: 20px;
                color: #059669;
                text-decoration: none;
                font-weight: 500;
                font-size: 10pt;
                padding: 4px 8px;
                background: #ecfdf5;
                border-radius: 4px;
                border: 1px solid #d1fae5;
            }}

            .link:hover {{
                background: #d1fae5;
            }}

            .abstract {{
                text-align: justify;
                margin-top: 15px;
                line-height: 1.6;
                color: #374151;
                background: #ffffff;
                padding: 15px;
                border-radius: 4px;
                border: 1px solid #f3f4f6;
            }}

            .abstract-title {{
                font-weight: 600;
                margin-bottom: 8px;
                color: #1f2937;
                font-size: 11pt;
            }}

            @page {{
                margin: 1in;
                @bottom-right {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 9pt;
                    color: #9ca3af;
                    font-weight: 500;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>MedBrief - Summary</h1>
            <div class="generated-date">Generated: {datetime.now().strftime('%B %d, %Y')}</div>
        </div>
    """

    current_journal = None

    for article in articles:
        journal = article.get('journal', 'Unknown Journal')

        # Add journal section header if this is a new journal
        if journal != current_journal:
            if current_journal is not None:
                html += "</div>"  # Close previous journal section

            html += f"""
        <div class="journal-section">
            <div class="journal-name">{journal}</div>
            """
            current_journal = journal

        # Add article content
        html += _generate_article_html(article)

    # Close the last journal section
    if current_journal is not None:
        html += "</div>"

    html += """
    </body>
    </html>
    """

    return html


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

    html = f"""
            <div class="article-title">{title}</div>
            <div class="article-meta">
                <div class="authors">{authors_display}</div>
                <div class="published">Published: {formatted_date}</div>
                <div class="links">
    """

    # Add PMID link
    if pubmed_id:
        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
        html += f'<a href="{pubmed_url}" class="link" target="_blank">PMID: {pubmed_id}</a>'

    # Add DOI link
    if doi:
        doi_url = f"https://doi.org/{doi}"
        html += f'<a href="{doi_url}" class="link" target="_blank">DOI: {doi}</a>'

    html += """
                </div>
            </div>
    """

    # Add abstract section only if abstract exists
    if abstract and abstract.strip():
        html += f"""
            <div class="abstract">
                <div class="abstract-title">Abstract:</div>
                <div>{abstract}</div>
            </div>
        """
    else:
        html += """
            <div class="abstract">
                <div class="abstract-title">Abstract:</div>
                <div>No abstract available for this article.</div>
            </div>
        """

    return html