from .utils import is_ai_enabled
from .ai_router import generate_ai_content
from .intent import detect_intent


def generate_article(keyword, style="blog"):

    print("\n========== GENERATOR DEBUG ==========")

    keyword = (keyword or "").strip()
    print("KEYWORD:", keyword)

    if not keyword:
        return _dummy_article(keyword, error="Empty keyword")

    ai_status = is_ai_enabled()
    print("AI ENABLED:", ai_status)

    # 🧠 Detect intent
    intent = detect_intent(keyword)
    print("🧠 DETECTED INTENT:", intent)

    # =========================
    # 🤖 AI MODE
    # =========================
    if ai_status:
        try:
            print("🚀 USING AI ROUTER...")

            content = generate_ai_content(keyword, intent=intent)

            if not content or len(content) < 200:
                raise Exception("Weak or empty AI response")

            print("✅ AI SUCCESS")

            return {
                # 🔥 SEO title centralized (no duplication)
                "title": _generate_title(keyword, intent),
                "content": content.strip(),
                "source": "AI",
                "intent": intent
            }

        except Exception as e:
            print("❌ AI ERROR:", str(e))

            # 🔁 smart fallback (still usable)
            return _dummy_article(
                keyword,
                error=f"AI Failed → {str(e)}"
            )

    # =========================
    # 🧪 DUMMY MODE
    # =========================
    print("⚠️ USING DUMMY MODE")
    return _dummy_article(keyword)


# =========================
# 🧠 TITLE GENERATOR (SEO SAFE)
# =========================
def _generate_title(keyword, intent):

    keyword = keyword.strip().title()

    if intent == "career":
        return f"{keyword} Recruitment 2026 | Eligibility, Salary, Apply Online"

    elif intent == "education":
        return f"{keyword} 2026 | Syllabus, Exam Pattern, Preparation Tips"

    elif intent == "pet":
        return f"{keyword} Care Guide 2026 | Food, Training, Health Tips"

    elif intent == "guide":
        return f"How To {keyword} (2026 Guide) | Step-by-Step Process"

    else:
        return f"{keyword} - Complete Guide 2026"


# =========================
# 🧪 DUMMY GENERATOR (SMART)
# =========================
def _dummy_article(keyword, error=None):

    title = f"{keyword} - Complete Guide (Test Mode)"

    content = f"""
🚨 THIS IS DUMMY CONTENT 🚨

Keyword: {keyword}

⚠️ AI system failed or disabled.

-------------------------------------

📌 Introduction:
This is a fallback article for {keyword}.

📌 Why this happened:
{error or "AI disabled"}

📌 What you can do:
- Check API key
- Check AI provider
- Check server logs

📌 Conclusion:
Fix AI system to generate real content.

-------------------------------------

🔧 SYSTEM INFO:
Mode: DUMMY
"""

    return {
        "title": title,
        "content": content.strip(),
        "source": "DUMMY",
        "error": error
    }