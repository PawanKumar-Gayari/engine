import requests
import os
import time
import random
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


# =========================
# ⚙️ CONFIG
# =========================
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = [
    "meta-llama/llama-3-8b-instruct",
    "mistralai/mistral-7b-instruct",
    "openchat/openchat-3.5"
]

MAX_RETRIES = 3


# =========================
# 🧠 PROMPT BUILDER (UPGRADED)
# =========================
def build_prompt(keyword, intent, stage="draft", base_content=""):

    base_rules = """
- Write in Hinglish (Hindi + English mix)
- Human tone (no robotic)
- SEO optimized
- Use HTML tags (<h2>, <h3>, <ul>, <table>)
- No repetition
"""

    # 🔥 STAGE BASED PROMPTS
    if stage == "rewrite":
        return f"""
Improve and rewrite the following content:

{base_content}

Make it:
- More human
- More detailed
- Better structured
- SEO optimized

Return HTML only.
"""

    elif stage == "seo":
        return f"""
Optimize this content for SEO:

{base_content}

Add:
- better headings
- keywords
- readability improvement

Return HTML only.
"""

    # =========================
    # DEFAULT (DRAFT)
    # =========================
    if intent in ["career", "job"]:
        return f"""
Write a HIGH QUALITY job article on: {keyword}

Include:
- Overview Table
- Eligibility
- Dates
- Salary
- Apply Steps
- FAQs

{base_rules}
"""

    elif intent == "education":
        return f"""
Write an educational article on: {keyword}

Include:
- Syllabus
- Exam Pattern
- Tips
- FAQs

{base_rules}
"""

    return f"""
Write a HIGH QUALITY SEO article on: {keyword}

Include:
- Introduction
- H2 sections
- Bullet points
- FAQs
- Conclusion

{base_rules}
"""


# =========================
# 🚀 MAIN FUNCTION (FIXED)
# =========================
def generate_openrouter_content(
    keyword,
    intent="general",
    stage="draft",
    base_content="",
    model=None
):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise Exception("OPENROUTER_API_KEY missing")

    prompt = build_prompt(keyword, intent, stage, base_content)

    last_error = None

    models_to_try = [model] if model else MODELS

    for mdl in models_to_try:

        for attempt in range(1, MAX_RETRIES + 1):

            try:
                logger.info(f"[OPENROUTER] {stage} | {mdl} | Attempt {attempt}")

                response = requests.post(
                    OPENROUTER_URL,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": mdl,
                        "messages": [
                            {"role": "system", "content": "You are an expert SEO writer."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 2500
                    },
                    timeout=40
                )

                if response.status_code != 200:
                    raise Exception(response.text)

                data = response.json()

                content = data["choices"][0]["message"]["content"]

                content = _clean_content(content)

                if not content or len(content) < 300:
                    raise Exception("Weak response")

                logger.info(f"[SUCCESS] {mdl}")

                return content

            except Exception as e:
                last_error = e

                logger.warning(
                    f"[FAIL] {mdl} | Attempt {attempt} | {e}"
                )

                time.sleep((2 ** attempt) + random.uniform(0, 1))

    logger.error("[OPENROUTER] ALL FAILED")

    raise Exception(f"OpenRouter failed: {last_error}")


# =========================
# 🧹 CLEANER
# =========================
def _clean_content(content):

    if not content:
        return ""

    content = content.replace("```html", "").replace("```", "")
    content = content.strip()

    return content