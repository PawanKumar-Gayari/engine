import requests
import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# 🧠 PROMPT BUILDER (PRO)
# =========================
def build_prompt(keyword: str, intent: str) -> str:

    # =========================
    # 💼 JOB / CAREER (ADVANCED)
    # =========================
    if intent in ["career", "job"]:
        return f"""
You are an expert Hindi-English (Hinglish) SEO content writer.

Write a HIGHLY STRUCTURED government job article on: {keyword}

STRICT FORMAT (FOLLOW EXACTLY):

1. SEO Introduction (keyword in first 100 words)

2. ⚡ Latest Update Box (use HTML styled box with bullets)

3. Overview Table (HTML table)

4. Vacancy Details (table format)

5. Important Dates (table)

6. Eligibility Criteria
   - Educational Qualification (table)
   - Age Limit (table)

7. Application Fee (table)

8. Selection Process (step table)

9. Exam Pattern (table + subjects)

10. Physical Test (PET/PST tables if applicable)

11. Salary Structure (table + allowances)

12. Apply Online Steps (step-by-step)

13. Required Documents (list)

14. Preparation Strategy (practical tips)

15. FAQs (Q1–Q10 using <details><summary> format)

16. Conclusion

RULES:
- Use proper HTML: <h2>, <h3>, <table>, <ul>, <strong>
- Use Hinglish (Hindi + English mix)
- Make it REALISTIC (no fake data)
- Use alert boxes (yellow/red/blue inline style)
- Make article 1500+ words
- SEO optimized

OUTPUT: Clean HTML article only
"""

    # =========================
    # 🐶 PET / GUIDE
    # =========================
    elif intent == "pet":
        return f"""
Write a detailed, practical guide on: {keyword}

Include:
- Daily routine
- Food & diet
- Training
- Health care
- Common mistakes

Rules:
- No fake info
- Beginner friendly
- Hinglish tone

Structure:
- Title
- Intro
- H2 sections
- Bullet points
- FAQs
- Conclusion
"""

    # =========================
    # 📚 EDUCATION
    # =========================
    elif intent == "education":
        return f"""
Write a structured educational article on: {keyword}

Include:
- Syllabus
- Exam pattern
- Important topics
- Preparation tips

Make it clear and structured.
"""

    # =========================
    # 📖 GENERAL (UPGRADED SEO)
    # =========================
    else:
        return f"""
Write a HIGH QUALITY SEO optimized article on: {keyword}

Rules:
- Human-like writing
- No fake info
- Practical content

Structure:
- Title
- Introduction
- H2 headings
- Bullet points
- FAQs
- Conclusion

Minimum 1200 words.
"""


# =========================
# 🚀 MAIN FUNCTION
# =========================
def generate_openrouter_content(keyword: str, intent: str = "general") -> str:

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise Exception("OPENROUTER_API_KEY not found")

    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = build_prompt(keyword, intent)

    payload = {
        # 🔥 Stable + Best free models
        "model": "meta-llama/llama-3-8b-instruct",

        "messages": [
            {
                "role": "system",
                "content": "You are a professional SEO blog writer who writes structured, accurate and high-quality content."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        "temperature": 0.7,
        "max_tokens": 2000
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)

    # ❌ HTTP ERROR
    if response.status_code != 200:
        raise Exception(f"OpenRouter HTTP Error: {response.status_code} - {response.text}")

    data = response.json()

    # ❌ API ERROR
    if "error" in data:
        raise Exception(f"OpenRouter Error: {data['error']['message']}")

    try:
        content = data["choices"][0]["message"]["content"]
    except Exception:
        raise Exception("Invalid response format from OpenRouter")

    if not content:
        raise Exception("Empty response from OpenRouter")

    return content.strip()