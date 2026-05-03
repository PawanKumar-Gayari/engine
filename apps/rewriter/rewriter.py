from apps.generator.ai_client import generate_openai_content


class Rewriter:
    """
    🔁 AI Rewrite Engine
    """

    def improve(self, article, keyword, issues):

        # 🔥 smart rewrite prompt
        improved = generate_openai_content(
            f"{keyword} detailed guide with proper structure and no repetition"
        )

        return improved