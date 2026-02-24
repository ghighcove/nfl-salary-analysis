#!/usr/bin/env python3
"""
NFL article pipeline index generator.

Generates article/index.html from article_status.json and opens it in the browser.
Run this file to view the article pipeline status.
"""

import json
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

# Add shared tools to path (sibling directory to this repo)
ROOT = Path(__file__).parent.parent
SHARED = ROOT.parent / "_shared_tools"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from article_status_generator import ArticleStatusGenerator


PROJECT_CONFIG = {
    "display_name": "NFL Analytics",
    "category": "Sports Analytics",
    "color": "#1B4F72",
}

STATUS_BADGE = {
    "published": '<span style="background:#1e4d2b;color:#3fb950;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">Published</span>',
    "ready":     '<span style="background:#1c3a5e;color:#58a6ff;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">Ready</span>',
    "draft":     '<span style="background:#2d2d0e;color:#d29922;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">Draft</span>',
    "archived":  '<span style="background:#2d2d2d;color:#8b949e;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">Archived</span>',
}


def generate_index(open_browser: bool = True) -> Path:
    """Generate article/index.html and optionally open it."""
    # Run status generator
    gen = ArticleStatusGenerator(
        project_root=ROOT,
        display_name=PROJECT_CONFIG["display_name"],
        category=PROJECT_CONFIG["category"],
    )
    data = gen.generate(write=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    articles = data.get("articles", [])
    summary = data.get("summary", {})
    color = PROJECT_CONFIG["color"]

    # Build article rows
    rows_html = ""
    for a in articles:
        badge = STATUS_BADGE.get(a["status"], STATUS_BADGE["draft"])
        platforms = ", ".join(a.get("platforms_published", [])) or "—"
        pub_date = ""
        if a.get("publish_dates"):
            pub_date = next(iter(a["publish_dates"].values()), "")
        elif a.get("date"):
            pub_date = a["date"]

        preview_link = ""
        if a.get("preview_html"):
            preview_link = f' &nbsp;<a href="{a["preview_html"]}" style="color:{color}">Preview</a>'

        rows_html += f"""
        <tr>
          <td><strong>{a['title']}</strong>{preview_link}
            <div style="font-size:11px;color:#8b949e;margin-top:2px">{a.get('subtitle','')[:80]}</div>
          </td>
          <td style="color:#8b949e;font-size:12px">{a.get('category','')}</td>
          <td>{platforms}</td>
          <td style="color:#8b949e;font-size:12px">{pub_date or '—'}</td>
          <td>{badge}</td>
        </tr>"""

    if not rows_html:
        rows_html = '<tr><td colspan="5" style="color:#8b949e;font-style:italic;text-align:center;padding:20px">No articles found in article/drafts/</td></tr>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{PROJECT_CONFIG['display_name']} — Article Pipeline</title>
<style>
  :root {{
    --bg: #0d1117; --bg2: #161b22; --border: #30363d;
    --text: #c9d1d9; --muted: #8b949e; --accent: {color};
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         background: var(--bg); color: var(--text); font-size: 14px; padding-bottom: 40px; }}
  header {{ background: var(--bg2); border-bottom: 1px solid var(--border);
            padding: 20px 30px; display: flex; justify-content: space-between; align-items: center; }}
  header h1 {{ font-size: 22px; color: var(--accent); }}
  header .ts {{ font-size: 12px; color: var(--muted); }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 24px 20px; }}
  .summary {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
  .stat {{ background: var(--bg2); border: 1px solid var(--border); border-radius: 8px;
           padding: 14px 20px; min-width: 100px; }}
  .stat .n {{ font-size: 28px; font-weight: 700; color: var(--accent); }}
  .stat .lbl {{ font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: .4px; margin-top: 2px; }}
  table {{ width: 100%; border-collapse: collapse; background: var(--bg2);
           border-radius: 8px; overflow: hidden; border: 1px solid var(--border); }}
  th {{ background: #1c2128; color: var(--muted); padding: 10px 14px; text-align: left;
        font-size: 11px; text-transform: uppercase; letter-spacing: .4px; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid var(--border); font-size: 13px; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #1c2128; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<header>
  <div>
    <h1>{PROJECT_CONFIG['display_name']}</h1>
    <div style="color:var(--muted);font-size:13px;margin-top:4px">Article Pipeline</div>
  </div>
  <div class="ts">Updated: {now}</div>
</header>

<div class="container">
  <div class="summary">
    <div class="stat"><div class="n">{summary.get('total', 0)}</div><div class="lbl">Total</div></div>
    <div class="stat"><div class="n" style="color:#3fb950">{summary.get('published', 0)}</div><div class="lbl">Published</div></div>
    <div class="stat"><div class="n" style="color:#58a6ff">{summary.get('ready', 0)}</div><div class="lbl">Ready</div></div>
    <div class="stat"><div class="n" style="color:#d29922">{summary.get('draft', 0)}</div><div class="lbl">Draft</div></div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Title</th>
        <th>Category</th>
        <th>Platform(s)</th>
        <th>Date</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>
</body>
</html>"""

    out = ROOT / "article" / "index.html"
    out.write_text(html, encoding="utf-8")

    if open_browser:
        webbrowser.open(out.as_uri())

    return out


if __name__ == "__main__":
    path = generate_index(open_browser=True)
    print(f"Generated: {path}")
