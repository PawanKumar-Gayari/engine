import requests
import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# 🧠 PROMPT BUILDER
# =========================
def build_prompt(keyword: str, intent: str) -> str:

    # 🐶 PET / ANIMAL
    if intent == "pet":
        return f"""
Write a detailed, practical guide on: {keyword}

Focus:
- Pet care (dog/cat)
- Daily routine
- Food and diet
- Training tips
- Health care
- Common mistakes

Rules:
- NO fake products
- Real-world advice
- Simple Hinglish language
- Helpful for beginners

Structure:
- Title
- Introduction
- H2 headings
- Bullet points
- FAQs
- Conclusion
"""

    # 💼 JOB / CAREER
    elif intent == "career":
        return f"""
Write a detailed job article on: {keyword}

Include:
- Eligibility
- Age limit
- Salary
- Selection process
- Exam pattern
- Important dates
- Preparation tips

Make it structured and factual.
"""

    # 📚 EDUCATION
    elif intent == "education":
        return f"""
Write an educational article on: {keyword}

Include:
- Syllabus
- Exam pattern
- Important topics
- Preparation strategy
- Tips for scoring high

Keep it clear and structured.
"""

    # 📖 GENERAL / GUIDE
    else:
        return f"""
Write a HIGH QUALITY SEO optimized article on: {keyword}

Rules:
- Understand the topic properly
- Do NOT invent fake things
- Keep content real and useful
- Human-like tone

Structure:
- Title
- Introduction
- H2 headings
- Bullet points
- FAQs
- Conclusion

Minimum 800 words.
"""


# =========================
# 🚀 MAIN FUNCTION
# =========================
def generate_openrouter_content(keyword: str, intent: str = "general") -> str:

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise Exception("OPENROUTER_API_KEY not found")

    url = "https://openrouter.ai/api/v1/chat/completions"

    # 🔥 dynamic prompt
    prompt = build_prompt(keyword, intent)

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",

        "messages": [
            {
                "role": "system",
                "content": "You are a professional SEO blog writer who writes accurate and helpful content."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        "temperature": 0.7,
        "max_tokens": 1200
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

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