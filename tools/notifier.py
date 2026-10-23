import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

def export_markdown_report(report_data: Dict[str, Any], output_path: Path) -> Path:
    """Xuất báo cáo dưới dạng Markdown chuẩn GitHub để đọc trong VS Code"""
    date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    content = f"""# 📰 Bản Tin Công Nghệ Hàng Ngày (Daily Tech Digest)
*Được tổng hợp và phân tích tự động bởi AI Agent vào lúc: **{date_str}***

---

## 🎯 Điểm Tin Nổi Bật (Executive Summary)
{report_data.get('summary', 'Chưa có tóm tắt chung.')}

---

## 🚀 Chi Tiết Các Tin Tức Quan Trọng

"""
    for idx, item in enumerate(report_data.get("articles", []), 1):
        content += f"""### {idx}. {item.get('title')}
- **Nguồn:** {item.get('source')} | [🔗 Đọc bài gốc]({item.get('link')})
- **Tóm tắt nhanh:** {item.get('ai_summary', item.get('snippet'))}
- **💡 Góc nhìn / Vì sao đáng chú ý:** {item.get('why_it_matters', 'Tin tức đáng chú ý trong ngày.')}

"""

    content += """---
*🤖 Báo cáo này được tạo tự động bởi **Antigravity Tech News Agent**.*
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


def export_html_report(report_data: Dict[str, Any], output_path: Path) -> Path:
    """Xuất báo cáo dưới dạng giao diện HTML hiện đại (Dark Mode), mở trực tiếp bằng trình duyệt"""
    date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    cards_html = ""
    for idx, item in enumerate(report_data.get("articles", []), 1):
        cards_html += f"""
        <div class="card">
            <div class="card-header">
                <span class="source-tag">{item.get('source')}</span>
                <span class="date">{item.get('published', '')}</span>
            </div>
            <h3 class="card-title">
                <a href="{item.get('link')}" target="_blank">{item.get('title')}</a>
            </h3>
            <p class="summary">{item.get('ai_summary', item.get('snippet'))}</p>
            <div class="insight">
                <strong>💡 Góc nhìn AI:</strong> {item.get('why_it_matters', 'Tin tức đáng quan tâm')}
            </div>
        </div>
        """

    html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Tech News Digest - {date_str}</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.2);
            --border: #334155;
            --insight-bg: rgba(56, 189, 248, 0.08);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 30px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
        }}
        h1 {{
            font-size: 2.2rem;
            color: var(--text-primary);
            margin-bottom: 8px;
        }}
        .badge {{
            display: inline-block;
            background: var(--accent-glow);
            color: var(--accent);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        .executive-summary {{
            background: var(--card-bg);
            border-left: 4px solid var(--accent);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .executive-summary h2 {{
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: var(--accent);
        }}
        .news-grid {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .source-tag {{
            background: #334155;
            color: #e2e8f0;
            padding: 2px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .date {{
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}
        .card-title a {{
            color: var(--text-primary);
            text-decoration: none;
            font-size: 1.2rem;
            font-weight: 600;
            transition: color 0.2s;
        }}
        .card-title a:hover {{
            color: var(--accent);
        }}
        .summary {{
            color: var(--text-secondary);
            margin: 12px 0;
            font-size: 0.95rem;
        }}
        .insight {{
            background: var(--insight-bg);
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 0.9rem;
            color: #bae6fd;
            border-left: 3px solid var(--accent);
        }}
        footer {{
            text-align: center;
            margin-top: 50px;
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <span class="badge">🤖 AI Agent Automation</span>
            <h1>Bản Tin Công Nghệ Hàng Ngày</h1>
            <p style="color: var(--text-secondary);">Cập nhật tự động lúc {date_str}</p>
        </header>

        <section class="executive-summary">
            <h2>🎯 Điểm Tin Trọng Tâm</h2>
            <p>{report_data.get('summary', 'Tổng hợp tự động tin công nghệ hôm nay.')}</p>
        </section>

        <section class="news-grid">
            {cards_html}
        </section>

        <footer>
            Tự động tạo bởi <strong>Daily Tech News Agent</strong> 🚀
        </footer>
    </div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    return output_path


def send_telegram_alert(token: str, chat_id: str, text: str) -> bool:
    """Gửi thông báo tóm tắt về Telegram của người dùng (nếu có cấu hình)"""
    if not token or not chat_id:
        return False
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text[:4000], # Giới hạn ký tự của Telegram
        "parse_mode": "Markdown"
    }
    
    try:
        data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
    except Exception as e:
        print(f"⚠️ [Không thể gửi tin qua Telegram]: {e}")
        return False
