from .utils import is_ai_enabled
from .ai_router import generate_ai_content
from .intent import detect_intent
from .formatter import format_article

from apps.generator.model_router import ModelRouter
from apps.generator.humanizer import Humanizer

import re
import logging

logger = logging.getLogger(__name__)


# =========================
# 🚀 MAIN GENERATOR (UPGRADED)
# =========================
def generate_article(keyword, style="blog", model=None, base_content=None):

    logger.info("========== GENERATOR START ==========")

    keyword = (keyword or "").strip()

    if not keyword:
        return _dummy_article(keyword, error="Empty keyword")

    ai_status = is_ai_enabled()
    intent = detect_intent(keyword)

    logger.info(f"KEYWORD: {keyword}")
    logger.info(f"AI ENABLED: {ai_status}")
    logger.info(f"INTENT: {intent}")

    router = ModelRouter()
    humanizer = Humanizer()

    if ai_status:
        try:
            # =========================
            # 🔥 MULTI-MODEL ROUTING
            # =========================
            if not model:
                model = router.get_model("draft")

            raw_content = generate_ai_content(
                keyword,
                intent=intent,
                stage="draft",
                base_content=base_content or "",
            )

            if not raw_content or len(raw_content) < 300:
                raise Exception("Weak AI response")

            # =========================
            # 🧹 FORMAT
            # =========================
            clean_content = format_article(raw_content)

            # =========================
            # 🧠 HUMANIZATION (NEW)
            # =========================
            try:
                clean_content = humanizer.humanize(clean_content)
            except Exception as e:
                logger.warning(f"Humanizer failed: {e}")

            # =========================
            # 🔁 REMOVE DUPLICATION
            # =========================
            clean_content = _remove_title_from_content(clean_content, keyword)

            # =========================
            # 🏗 BUILD FINAL ARTICLE
            # =========================
            final_content = _build_full_article(
                keyword=keyword,
                content=clean_content,
                intent=intent
            )

            title = _generate_title(keyword, intent)
            slug = _generate_slug(keyword)
            meta = _generate_meta_description(keyword, intent)

            return {
                "title": title,
                "content": final_content,
                "meta_description": meta,
                "slug": slug,
                "source": "AI",
                "intent": intent,
                "model": model
            }

        except Exception as e:
            logger.error(f"❌ AI ERROR: {e}")
            return _dummy_article(keyword, error=str(e))

    return _dummy_article(keyword)


# =========================
# 🔥 FULL ARTICLE BUILDER
# =========================
def _build_full_article(keyword, content, intent):

    title = _generate_title(keyword, intent)
    intro = _extract_intro(content)

    return f"""
<h1>{title}</h1>

<section>
<h2>Introduction</h2>
<p>{intro}</p>
</section>

<section>
<h2>Overview</h2>
<table>
<tr><th>Topic</th><td>{keyword}</td></tr>
<tr><th>Category</th><td>{intent}</td></tr>
<tr><th>Year</th><td>2026</td></tr>
</table>
</section>

<section>
<h2>Detailed Explanation</h2>
{content}
</section>

<section>
<h2>Key Highlights</h2>
<ul>
<li>Updated for 2026</li>
<li>Easy to understand</li>
<li>Exam focused content</li>
</ul>
</section>

<section>
<h2>FAQs</h2>
<h3>What is {keyword}?</h3>
<p>{keyword} is explained above in a structured and simplified way.</p>

<h3>Why is {keyword} important?</h3>
<p>This topic is useful for exams, career growth, and practical knowledge.</p>
</section>

<section>
<h2>Conclusion</h2>
<p>This guide provides complete understanding of {keyword}. Use it for preparation and revision.</p>
</section>
"""


# =========================
# 🔁 REMOVE DUPLICATE TITLE
# =========================
def _remove_title_from_content(content, keyword):

    pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    lines = content.split("\n")
    filtered = []

    for line in lines:
        if pattern.search(line) and len(line.strip()) < 80:
            continue
        filtered.append(line)

    return "\n".join(filtered)


# =========================
# 🧠 INTRO EXTRACTOR
# =========================
def _extract_intro(content):

    text = re.sub(r"<[^>]+>", "", content)
    sentences = text.split(".")
    intro = ".".join(sentences[:3])

    return intro.strip()


# =========================
# 🔗 SLUG
# =========================
def _generate_slug(keyword):

    slug = keyword.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)

    return slug.strip("-")


# =========================
# 🧠 META
# =========================
def _generate_meta_description(keyword, intent):

    if intent == "education":
        return f"{keyword} 2026 syllabus, exam pattern और preparation tips हिंदी में जानें।"

    elif intent == "career":
        return f"{keyword} recruitment 2026 – eligibility, salary, selection process पूरी जानकारी।"

    elif intent == "guide":
        return f"{keyword} कैसे करें? Step-by-step guide 2026 में जानें।"

    return f"{keyword} के बारे में पूरी जानकारी 2026 में विस्तार से पढ़ें।"


# =========================
# 🧠 TITLE
# =========================
def _generate_title(keyword, intent):

    keyword = keyword.strip().title()

    if intent == "career":
        return f"{keyword} Recruitment 2026 | Eligibility, Salary, Apply Online"

    elif intent == "education":
        return f"{keyword} 2026 | Syllabus, Exam Pattern, Preparation Tips"

    elif intent == "guide":
        return f"How To {keyword} (2026 Guide) | Step-by-Step Process"

    return f"{keyword} - Complete Guide 2026"


# =========================
# 🧪 FALLBACK
# =========================
def _dummy_article(keyword, error=None):

    title = f"{keyword} - Complete Guide (Fallback)"

    return {
        "title": title,
        "content": f"""
<h1>{title}</h1>
<p>Fallback content generated.</p>
<p>Error: {error}</p>
""",
        "meta_description": f"{keyword} जानकारी (Fallback)",
        "slug": _generate_slug(keyword),
        "source": "DUMMY",
        "error": error
    }