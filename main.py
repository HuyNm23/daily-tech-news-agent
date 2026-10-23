#!/usr/bin/env python3
# ==============================================================================
# DAILY TECH NEWS AGENT - MAIN ORCHESTRATOR
# ==============================================================================
import sys
import os
from datetime import datetime
from pathlib import Path

# Đảm bảo in UTF-8 mượt mà trên console Windows (tránh lỗi font / emoji cp1258)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thêm thư mục hiện tại vào sys.path để import dễ dàng
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

import config
from tools.news_fetcher import fetch_all_sources
from tools.notifier import export_markdown_report, export_html_report, send_telegram_alert
from agent import NewsAgent

def print_banner():
    print("""
================================================================
🚀 DAILY TECH NEWS AGENT - TRỢ LÝ SĂN TIN CÔNG NGHỆ TỰ ĐỘNG 🚀
================================================================
    """)

def main():
    print_banner()
    
    # 1. Khởi tạo Agent
    print(f"⚙️ Khởi động Agent với chế độ AI: [{config.AI_PROVIDER.upper()}]")
    agent = NewsAgent(
        provider=config.AI_PROVIDER,
        gemini_api_key=config.GEMINI_API_KEY,
        openai_api_key=config.OPENAI_API_KEY,
        ollama_model=config.OLLAMA_MODEL
    )

    # 2. Bước 1: Tool cào dữ liệu từ các nguồn RSS
    print("\n[BƯỚC 1/3]: Thu thập tin tức từ các nguồn uy tín...")
    raw_articles = fetch_all_sources(config.NEWS_SOURCES)
    
    if not raw_articles:
        print("❌ Không thu thập được tin tức nào. Vui lòng kiểm tra lại kết nối mạng!")
        return

    print(f"🎉 Thu thập thành công {len(raw_articles)} bài viết từ các nguồn.")

    # 3. Bước 2: Agent tư duy, lọc, phân tích và tóm tắt
    print("\n[BƯỚC 2/3]: Agent tiến hành tư duy, chọn lọc và tổng hợp...")
    report_data = agent.run_agentic_workflow(raw_articles)

    # 4. Bước 3: Xuất báo cáo (Markdown + Giao diện Web HTML đẹp mắt)
    print("\n[BƯỚC 3/3]: Đang xuất bản báo cáo tổng hợp...")
    date_slug = datetime.now().strftime("%Y-%m-%d_%H%M")
    
    md_file = config.REPORTS_DIR / f"news_report_{date_slug}.md"
    html_file = config.REPORTS_DIR / f"news_report_{date_slug}.html"
    
    export_markdown_report(report_data, md_file)
    export_html_report(report_data, html_file)

    print("\n" + "="*60)
    print("✅ ĐÃ HOÀN TẤT NHIỆM VỤ! KẾT QUẢ ĐÃ ĐƯỢC TẠO TẠI:")
    print(f"📄 File Markdown : {md_file}")
    print(f"🌐 File HTML Web : {html_file}")
    print("="*60)

    # 5. Gửi thông báo Telegram (nếu có cấu hình)
    if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID:
        print("📲 Đang gửi thông báo tóm tắt qua Telegram...")
        telegram_msg = f"📰 *BẢN TIN CÔNG NGHỆ HÔM NAY*\n\n{report_data['summary']}\n\n👉 Chi tiết đã lưu tại máy tính của bạn!"
        if send_telegram_alert(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID, telegram_msg):
            print("✅ Đã gửi tin nhắn Telegram thành công!")

    # 6. Mở trực tiếp file HTML trên trình duyệt để người dùng xem ngay
    print(f"\n💡 Bạn có thể mở file '{html_file.name}' bằng trình duyệt để xem giao diện cực đẹp!")

if __name__ == "__main__":
    main()
