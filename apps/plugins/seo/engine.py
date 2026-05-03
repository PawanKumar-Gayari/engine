def run_seo_plugin(article, keyword: str = "", intent: str = "", context=None):
    """
    🔥 Smart SEO Engine (Advanced AI Version)
    - keyword optimization
    - heading structure
    - basic density control
    - plugin runner integration
    - meta context enrichment
    """

    from apps.plugins.seo.runner import apply_seo_plugins
    import re
    import logging

    logger = logging.getLogger(__name__)
    context = context or {}

    try:
        # =========================
        # 📦 Normalize Input
        # =========================
        if isinstance(article, dict):
            content = article.get("content", "")
        else:
            content = str(article)

        if not content:
            return article

        # =========================
        # 🧠 Context Enrichment
        # =========================
        keyword = keyword.lower().strip()
        context.update({
            "keyword": keyword,
            "intent": intent,
        })

        # =========================
        # 🔥 1. KEYWORD INSERTION (SMART)
        # =========================
        if keyword and keyword not in content.lower():
            content = f"{keyword.title()} - {content}"

        # =========================
        # 🔥 2. BASIC KEYWORD DENSITY CONTROL
        # =========================
        if keyword:
            words = content.split()
            total_words = len(words)
            keyword_count = content.lower().count(keyword)

            desired_density = 0.01  # 1%
            current_density = keyword_count / max(total_words, 1)

            if current_density < desired_density:
                content += f"\n\n{keyword}"

        # =========================
        # 🔥 3. HEADING STRUCTURE FIX
        # =========================
        if keyword:
            if not content.strip().startswith("#"):
                content = f"# {keyword.title()}\n\n" + content

        # =========================
        # 🔥 4. FAQ AUTO ADD (INTENT BASED)
        # =========================
        if intent in ["informational", "question"]:
            faq_section = f"""

## FAQs

**What is {keyword}?**  
{keyword.title()} is explained in simple terms above.

**Why is {keyword} important?**  
It helps users understand the topic better.
"""
            content += faq_section

        # =========================
        # 🔥 5. APPLY SEO PLUGINS (PIPELINE)
        # =========================
        content = apply_seo_plugins(content, context)

        # =========================
        # 📊 SEO SCORE (BASIC)
        # =========================
        score = 0
        if keyword in content.lower():
            score += 40
        if "#" in content:
            score += 20
        if "faq" in content.lower():
            score += 20
        if len(content.split()) > 300:
            score += 20

        # =========================
        # 📤 Return Safe Format
        # =========================
        if isinstance(article, dict):
            article["content"] = content
            article["seo_processed"] = True
            article["seo_keyword"] = keyword
            article["seo_intent"] = intent
            article["seo_score"] = score
            return article

        return content

    except Exception as e:
        logger.error(f"❌ SEO Engine Failed: {e}")

        if isinstance(article, dict):
            article["seo_error"] = str(e)
            return article

        return article