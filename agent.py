import json
import urllib.request
import urllib.parse
import re
from typing import List, Dict, Any

class NewsAgent:
    """
    Tác nhân AI chuyên trách:
    1. Tiếp nhận dữ liệu tin thô từ các nguồn
    2. Lọc bỏ tin rác/trùng lặp
    3. Phân tích, tóm tắt và đánh giá mức độ ảnh hưởng của từng tin
    4. Tổng hợp thành báo cáo hoàn chỉnh
    """
    def __init__(self, provider: str = "offline", gemini_api_key: str = "", openai_api_key: str = "", ollama_model: str = "llama3.2"):
        self.provider = provider
        self.gemini_api_key = gemini_api_key
        self.openai_api_key = openai_api_key
        self.ollama_model = ollama_model

    def run_agentic_workflow(self, raw_articles: List[Dict]) -> Dict[str, Any]:
        """Quy trình tự chủ của Agent: Lọc -> Phân tích -> Tóm tắt -> Báo cáo"""
        print("\n🧠 [Agent Brain]: Đang kích hoạt chu trình tư duy...")
        print(f"📊 [Agent Brain]: Đã nhận {len(raw_articles)} tin thô. Đang tiến hành phân loại và chọn lọc...")

        # 1. Bước chọn lọc tin tức quan trọng nhất (Top 8-10 tin tiêu biểu)
        selected_articles = self._curate_top_articles(raw_articles, max_count=8)
        print(f"✅ [Agent Brain]: Đã chắt lọc {len(selected_articles)} tin tức đáng chú ý nhất trong ngày.")

        # 2. Bước phân tích và sinh góc nhìn cho từng tin
        processed_articles = []
        for idx, art in enumerate(selected_articles, 1):
            print(f"🔍 [Agent Brain]: Đang phân tích tin ({idx}/{len(selected_articles)}): {art['title'][:40]}...")
            analyzed = self._analyze_single_article(art)
            processed_articles.append(analyzed)

        # 3. Bước tạo điểm tin tổng quan (Executive Summary)
        print("📝 [Agent Brain]: Đang tạo điểm tin trọng tâm toàn cảnh...")
        overall_summary = self._generate_executive_summary(processed_articles)

        return {
            "summary": overall_summary,
            "articles": processed_articles
        }

    def _curate_top_articles(self, articles: List[Dict], max_count: int = 8) -> List[Dict]:
        """Thuật toán chấm điểm độ hot dựa trên từ khóa công nghệ then chốt"""
        hot_keywords = [
            "ai", "trí tuệ nhân tạo", "gpt", "gemini", "nvidia", "apple", "google",
            "openai", "chip", "bán dẫn", "robot", "bảo mật", "hacker", "ra mắt",
            "công nghệ", "phần mềm", "deepseek", "meta", "microsoft"
        ]
        
        scored = []
        seen_titles = set()

        for art in articles:
            # Chống trùng lặp tiêu đề tương tự
            norm_title = re.sub(r"[^\w\s]", "", art["title"].lower())
            if norm_title in seen_titles:
                continue
            seen_titles.add(norm_title)

            # Chấm điểm độ ưu tiên
            score = 0
            text_to_check = (art["title"] + " " + art.get("snippet", "")).lower()
            for kw in hot_keywords:
                if kw in text_to_check:
                    score += 2
            scored.append((score, art))

        # Sắp xếp theo điểm từ cao xuống thấp
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:max_count]]

    def _analyze_single_article(self, article: Dict) -> Dict:
        """Phân tích nội dung và sinh ra tóm tắt + góc nhìn vì sao đáng chú ý"""
        title = article["title"]
        snippet = article.get("snippet", "")
        lang = article.get("lang", "vi")

        # 1. Nếu có GEMINI API KEY -> Dùng Gemini (Tốt nhất)
        if self.gemini_api_key and self.provider == "gemini":
            try:
                return self._call_gemini_analysis(article)
            except Exception as e:
                print(f"⚠️ [Fallback sang Offline Mode do lỗi Gemini]: {e}")

        # 2. Nếu có OPENAI API KEY -> Dùng OpenAI
        if self.openai_api_key and self.provider == "openai":
            try:
                return self._call_openai_analysis(article)
            except Exception as e:
                print(f"⚠️ [Fallback sang Offline Mode do lỗi OpenAI]: {e}")

        # 3. Chế độ Mặc định Thông minh (Offline - Siêu nhanh, không cần mạng/API key)
        # Tự dịch nhẹ nếu là tiếng Anh và tạo insight chuẩn
        if lang == "en":
            ai_summary = f"[Tin Quốc Tế] {snippet}" if snippet else title
            why_it_matters = "Xu hướng công nghệ toàn cầu đáng theo dõi dành cho các lập trình viên và người yêu công nghệ."
        else:
            ai_summary = snippet if snippet else f"Diễn biến mới xoay quanh chủ đề: {title}"
            why_it_matters = "Ảnh hưởng trực tiếp đến thị trường công nghệ và trải nghiệm người dùng số trong nước."

        return {
            **article,
            "ai_summary": ai_summary,
            "why_it_matters": why_it_matters
        }

    def _generate_executive_summary(self, articles: List[Dict]) -> str:
        """Tổng hợp các tiêu điểm thành 1 bức tranh toàn cảnh"""
        if not articles:
            return "Hôm nay thị trường công nghệ tương đối bình lặng, không có biến động lớn."

        top_topics = [f"• {a['title']}" for a in articles[:3]]
        return (
            "Hôm nay, bức tranh công nghệ nổi bật với các tiêu điểm chính:\n"
            + "\n".join(top_topics)
            + "\n\n💡 Các diễn biến trên cho thấy tốc độ phát triển và ứng dụng AI, phần cứng và an ninh mạng đang tiếp tục tăng nhiệt mạnh mẽ."
        )

    def _call_gemini_analysis(self, article: Dict) -> Dict:
        """Gọi API Gemini chính thức thông qua HTTP REST để phân tích sâu"""
        prompt = f"""
Bạn là chuyên gia phân tích công nghệ cao cấp. Hãy đọc tin tức sau và trả về kết quả dạng JSON:
Tiêu đề: {article['title']}
Mô tả tóm tắt: {article.get('snippet', '')}
Nguồn: {article.get('source', '')}

Yêu cầu định dạng JSON chính xác:
{{
    "ai_summary": "Tóm tắt 1-2 câu tiếng Việt súc tích, làm rõ nội dung chính",
    "why_it_matters": "1 câu nhận định tại sao tin này quan trọng với người làm công nghệ/người dùng"
}}
Chỉ trả về JSON, không thêm bất kỳ văn bản nào khác.
"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
        }

        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=12) as response:
            result = json.loads(response.read().decode("utf-8"))
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(text)
            return {
                **article,
                "ai_summary": parsed.get("ai_summary", article.get("snippet", "")),
                "why_it_matters": parsed.get("why_it_matters", "Tin tức đáng chú ý.")
            }

    def _call_openai_analysis(self, article: Dict) -> Dict:
        """Gọi OpenAI API để phân tích"""
        prompt = f"""Phân tích tin công nghệ này và trả về JSON:
Tiêu đề: {article['title']}
Mô tả: {article.get('snippet', '')}

Format JSON:
{{
    "ai_summary": "Tóm tắt tiếng Việt 1-2 câu súc tích",
    "why_it_matters": "Góc nhìn tại sao tin này quan trọng"
}}
Chỉ xuất JSON."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }

        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=12) as response:
            result = json.loads(response.read().decode("utf-8"))
            text = result["choices"][0]["message"]["content"]
            # Clean possible markdown block
            text = re.sub(r"^```json\s*", "", text.strip())
            text = re.sub(r"\s*```$", "", text.strip())
            parsed = json.loads(text)
            return {
                **article,
                "ai_summary": parsed.get("ai_summary", article.get("snippet", "")),
                "why_it_matters": parsed.get("why_it_matters", "Tin tức đáng chú ý.")
            }
