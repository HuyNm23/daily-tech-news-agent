import urllib.request
import xml.etree.ElementTree as ET
import re
import html
from typing import List, Dict, Optional

def clean_html(raw_html: str) -> str:
    """Loại bỏ thẻ HTML và làm sạch văn bản"""
    if not raw_html:
        return ""
    text = html.unescape(raw_html)
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean

def find_first_node(parent: ET.Element, tags: List[str]) -> Optional[ET.Element]:
    """Tìm node đầu tiên tồn tại trong danh sách tag (tránh lỗi bool(Element) trong Python)"""
    for tag in tags:
        node = parent.find(tag)
        if node is not None:
            return node
    return None

def fetch_rss_feed(source_info: Dict) -> List[Dict]:
    """
    Thu thập tin tức từ 1 nguồn RSS.
    Sử dụng thư viện chuẩn của Python để đạt hiệu năng cao, siêu nhẹ, không tốn RAM.
    """
    name = source_info.get("name", "Unknown Source")
    url = source_info.get("url")
    limit = source_info.get("limit", 5)
    lang = source_info.get("lang", "vi")

    articles = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()

        # Phân tích cây XML RSS
        root = ET.fromstring(xml_data)

        # Hỗ trợ cả RSS 2.0 (channel/item) và Atom feed (entry)
        items = root.findall(".//item")
        if not items:
            items = root.findall(".//{http://www.w3.org/2005/Atom}entry")

        for item in items[:limit]:
            # Lấy Title
            title_node = find_first_node(item, ["title", "{http://www.w3.org/2005/Atom}title"])
            title = title_node.text if title_node is not None and title_node.text else "Không có tiêu đề"
            title = clean_html(title)

            # Lấy Link
            link_node = find_first_node(item, ["link", "{http://www.w3.org/2005/Atom}link"])
            link = ""
            if link_node is not None:
                link = link_node.text or link_node.get("href", "")

            # Lấy Mô tả / Tóm tắt ban đầu
            desc_node = find_first_node(item, [
                "description", 
                "summary", 
                "{http://www.w3.org/2005/Atom}summary", 
                "{http://www.w3.org/2005/Atom}content"
            ])
            raw_desc = desc_node.text if desc_node is not None and desc_node.text else ""
            clean_desc = clean_html(raw_desc)

            # Lấy Ngày đăng
            pub_date_node = find_first_node(item, [
                "pubDate", 
                "published", 
                "{http://www.w3.org/2005/Atom}published", 
                "{http://www.w3.org/2005/Atom}updated"
            ])
            pub_date = pub_date_node.text if pub_date_node is not None and pub_date_node.text else "Hôm nay"

            if title and link:
                articles.append({
                    "source": name,
                    "title": title,
                    "link": link.strip(),
                    "snippet": clean_desc[:300] + "..." if len(clean_desc) > 300 else clean_desc,
                    "published": pub_date.strip(),
                    "lang": lang
                })

    except Exception as e:
        print(f"⚠️ [Lỗi khi cào tin từ {name}]: {e}")

    return articles

def fetch_all_sources(sources: List[Dict]) -> List[Dict]:
    """Cào tin tức từ tất cả các nguồn trong danh sách cấu hình"""
    all_articles = []
    for src in sources:
        print(f"📡 Đang quét tin tức từ: {src['name']}...")
        items = fetch_rss_feed(src)
        print(f"   -> Đã lấy được {len(items)} bài viết mới nhất.")
        all_articles.extend(items)
    return all_articles
