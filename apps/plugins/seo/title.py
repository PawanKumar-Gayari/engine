from apps.plugins.base.base_plugin import BasePlugin


class TitlePlugin(BasePlugin):

    name = "seo_title"

    def apply(self, article):

        raw_title = article.get("title", "")

        # 🔥 CLEAN DUMMY / EXTRA TEXT
        clean_title = (
            raw_title
            .replace("[DUMMY]", "")
            .replace("- Test Article", "")
            .strip()
        )

        # 🔥 AVOID DOUBLE SEO (already optimized)
        if "Complete Guide" in clean_title:
            article["title"] = clean_title
            return article

        # 🔥 FINAL SEO TITLE
        article["title"] = f"{clean_title} - Complete Guide 2026 | Eligibility, Syllabus, Exam Date"

        return article