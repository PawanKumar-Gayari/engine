from openai import OpenAI
import os
import json
import re


def generate_openai_content(keyword):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise Exception("OPENAI_API_KEY not found")

    # =========================
    # 🔥 OPENROUTER CLIENT (FIXED AUTH)
    # =========================
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    # =========================
    # 🧠 STRONG PROMPT
    # =========================
    prompt = f"""
Write a professional SEO article on: {keyword}

STRICT RULES:
- English only (NO Hindi, NO Hinglish)
- No repetition
- No garbage text
- Proper grammar
- Use <h2> headings
- Minimum 900 words

Structure:
<h2>Introduction</h2>
<h2>Overview</h2>
<h2>Preparation Strategy</h2>
<h2>Tips</h2>
<h2>Conclusion</h2>

Return ONLY JSON:
{{
"title": "...",
"content": "...",
"meta_description": "..."
}}
"""

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",  # 🔥 BETTER MODEL
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        raw_output = response.choices[0].message.content.strip()

        # =========================
        # 🔥 SAFE JSON PARSER (STRONG)
        # =========================
        def extract_json(text):
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                return json.loads(text[start:end])
            except Exception:
                return None

        data = extract_json(raw_output)

        if not data:
            raise Exception(f"Invalid JSON → {raw_output[:300]}")

        # =========================
        # 🧹 CLEAN CONTENT
        # =========================
        content = data.get("content", "")

        # remove non-english
        content = re.sub(r'[^\x00-\x7F]+', ' ', content)

        # remove repetition
        content = re.sub(r'\b(\w+)( \1\b)+', r'\1', content)

        # clean spacing
        content = re.sub(r'\s+', ' ', content)

        # =========================
        # 🧠 SAFE TITLE + META
        # =========================
        title = data.get("title", "").strip()

        if len(title) < 10:
            title = f"{keyword.title()} 2026 Complete Guide"

        meta = data.get("meta_description", "").strip()

        if len(meta) < 50:
            meta = f"{keyword} complete guide with preparation tips and strategy."

        return {
            "title": title,
            "content": content.strip(),
            "meta_description": meta[:160]
        }

    except Exception as e:
        raise Exception(f"AI Client Error: {str(e)}")