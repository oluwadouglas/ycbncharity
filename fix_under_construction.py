import os
import re
from pathlib import Path

# Paths
TEMPLATE_DIR = Path('templates/charity')
HTML_ROOT = Path('.')  # Now points to the root of ycbf

# Flexible regex for <section class="space ..."> (allow extra classes/attrs/whitespace)
SECTION_RE = re.compile(r'<section[^>]*class="[^"]*space[^"]*"[^>]*>[\s\S]*?</section>', re.IGNORECASE)

# Patterns for static asset references in src, href, data-bg-src, style, srcset, both single and double quotes
ASSET_PATTERNS = [
    # src, href, data-bg-src, srcset attributes
    r'(?P<attr>src|href|data-bg-src|srcset)=(?P<q>["\"])assets/(?P<path>[^"\'>) ]+)(?P<endq>["\"])',
    # url('assets/...') or url("assets/..."), or url(assets/...)
    r'url\((?P<q>["\"])??assets/(?P<path>[^"\')]+)(?P<endq>["\"])??\)',
]

# Helper to convert static and url references
def convert_static_and_urls(html, page_name):
    # Convert all asset references
    html = re.sub(ASSET_PATTERNS[0], static_replacer_attr, html)
    html = re.sub(ASSET_PATTERNS[1], static_replacer_url, html)
    # Only convert links that do NOT require arguments (e.g., not blog-details.html)
    html = re.sub(
        r'href="([a-zA-Z0-9\-]+)\.html"',
        lambda m: (
            f"href='{{% url 'charity:{m.group(1).replace('-', '_')}' %}}'"
            if m.group(1) not in ['blog-details', 'donation-details', 'event-details', 'shop-details', 'team-details']
            else m.group(0)
        ),
        html
    )
    return html

def static_replacer_attr(match):
    attr = match.group('attr')
    q = match.group('q')
    path = match.group('path')
    endq = match.group('endq')
    return f"{attr}={q}{{% static 'assets/{path}' %}}{endq}"

def static_replacer_url(match):
    q = match.group('q') or ''
    path = match.group('path')
    endq = match.group('endq') or ''
    return f"url({q}{{% static 'assets/{path}' %}}{endq})"

def main():
    for tpl_file in TEMPLATE_DIR.glob('*.html'):
        with open(tpl_file, 'r', encoding='utf-8') as f:
            tpl_content = f.read()
        page_name = tpl_file.stem.replace('_', '-')
        html_file = HTML_ROOT / f'{page_name}.html'  # look in ycbf root for original HTML
        # Remove any <section class="space ..."> in template
        tpl_content_cleaned, n = SECTION_RE.subn('', tpl_content)
        replaced = False
        # If corresponding HTML file exists, copy its <section class="space ..."> into template
        if html_file.exists():
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            html_sections = SECTION_RE.findall(html_content)
            if html_sections:
                new_sections = '\n'.join([convert_static_and_urls(s, page_name) for s in html_sections])
                # Insert after breadcumb if present, else at start of content block
                breadcumb_match = re.search(r'(</div>\s*</div>\s*</div>)', tpl_content_cleaned)
                if breadcumb_match:
                    insert_at = breadcumb_match.end()
                    new_tpl_content = tpl_content_cleaned[:insert_at] + '\n' + new_sections + tpl_content_cleaned[insert_at:]
                else:
                    # Insert at start of content block
                    content_block = re.search(r'(\{% block content %\})', tpl_content_cleaned)
                    if content_block:
                        insert_at = content_block.end()
                        new_tpl_content = tpl_content_cleaned[:insert_at] + '\n' + new_sections + tpl_content_cleaned[insert_at:]
                    else:
                        new_tpl_content = new_sections + tpl_content_cleaned
                replaced = True
                with open(tpl_file, 'w', encoding='utf-8') as f:
                    f.write(new_tpl_content)
                print(f'Copied and inserted all sections from {html_file} into {tpl_file}')
        if not replaced:
            # If nothing to insert, just write cleaned content
            with open(tpl_file, 'w', encoding='utf-8') as f:
                f.write(tpl_content_cleaned)
            if n > 0:
                print(f'Removed section from {tpl_file}')

if __name__ == '__main__':
    main()
