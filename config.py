# ==============================================================================
# CẤU HÌNH CHO DAILY TECH NEWS AGENT
# ==============================================================================
import os
from pathlib import Path

# Tải biến môi trường từ .env (hỗ trợ cả khi chưa cài python-dotenv)
BASE_DIR = Path(__file__).resolve().parent
env_file = BASE_DIR / ".env"
try:
    from dotenv import load_dotenv
    load_dotenv(env_file)
except ImportError:
    # Bộ đọc .env đơn giản tự chế bằng Python thuần nếu chưa cài python-dotenv
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip())

# 1. Cấu hình AI Provider (gemini / openai / ollama / offline)
# Nếu không có API Key, Agent sẽ tự động fallback về chế độ 'offline' thông minh
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# 2. Cấu hình Telegram (Tùy chọn - để gửi tin về điện thoại)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# 3. Danh sách các nguồn tin tức công nghệ (RSS feeds)
# Sử dụng RSS siêu nhẹ, cập nhật tức thì, không lo bị chặn IP
NEWS_SOURCES = [
    {
        "name": "VnExpress Số Hóa (Công Nghệ)",
        "url": "https://vnexpress.net/rss/so-hoa.rss",
        "lang": "vi",
        "limit": 5
    },
    {
        "name": "Báo Tuổi Trẻ (Khoa Học - Công Nghệ)",
        "url": "https://tuoitre.vn/rss/khoa-hoc.rss",
        "lang": "vi",
        "limit": 5
    },
    {
        "name": "Hacker News (Top Tech)",
        "url": "https://news.ycombinator.com/rss",
        "lang": "en",
        "limit": 5
    },
    {
        "name": "TechCrunch (Khởi nghiệp & AI)",
        "url": "https://techcrunch.com/feed/",
        "lang": "en",
        "limit": 5
    }
]

# 4. Thư mục lưu báo cáo kết quả
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
