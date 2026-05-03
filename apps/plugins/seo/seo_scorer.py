import re


class SEOScorer:
    """
    🚀 Advanced SEO Scoring Engine
    """

    name = "seo_scorer"
    priority = 20
    phase = "post"

    def run(self, article, keyword="", intent="", context=None):

        content = article.get("content", "")
        title = article.get("title", "")
        meta = article.get("meta_description", "")

        score = 0

        # =========================
        # 🔥 CONTENT LENGTH
        # =========================
        length = len(content)

        if length > 2000:
            score += 25
        elif length > 1200:
            score += 20
        elif length > 800:
            score += 15
        else:
            score += 5

        # =========================
        # 🔥 KEYWORD CHECK
        # =========================
        keyword = keyword.lower()

        if keyword in content.lower():
            score += 20

        if keyword in title.lower():
            score += 10

        if keyword in meta.lower():
            score += 10

        # =========================
        # 🔥 STRUCTURE CHECK
        # =========================
        if "<h2>" in content.lower():
            score += 10

        if content.count("<h2>") >= 3:
            score += 5

        # =========================
        # 🔥 READABILITY
        # =========================
        sentences = content.count(".")
        if sentences > 20:
            score += 10

        # =========================
        # 🔥 REPETITION CHECK
        # =========================
        if re.search(r'\b(\w+)( \1\b)+', content.lower()):
            score -= 10

        # =========================
        # 🔥 META QUALITY
        # =========================
        if 50 <= len(meta) <= 160:
            score += 5

        # =========================
        # 🔥 FINAL SCORE
        # =========================
        score = max(0, min(score, 100))

        article["seo_score"] = score

        # =========================
        # 🔥 RANK PREDICTION
        # =========================
        if score > 80:
            article["rank_prediction"] = "High"
        elif score > 60:
            article["rank_prediction"] = "Medium"
        else:
            article["rank_prediction"] = "Low"

        return article