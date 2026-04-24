from apps.plugins.base.base_plugin import BasePlugin


class MetaPlugin(BasePlugin):

    name = "seo_meta"

    def apply(self, article):

        keyword = article.get("title", "")

        article["meta_description"] = f"Learn everything about {keyword}, including eligibility, syllabus, exam dates and preparation tips."

        return article