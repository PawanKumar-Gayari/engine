import re


class Verifier:
    """
    🔍 Content Quality Verifier
    """

    def evaluate(self, article, keyword):

        content = article.get("content", "").lower()
        title = article.get("title", "").lower()

        score = 0
        issues = []

        # length check
        if len(content) > 1500:
            score += 30
        elif len(content) > 800:
            score += 20
        else:
            issues.append("Content too short")

        # keyword check
        if keyword.lower() in content:
            score += 20
        else:
            issues.append("Keyword missing")

        if keyword.lower() in title:
            score += 10

        # structure check
        if "<h2>" in content:
            score += 20
        else:
            issues.append("No headings")

        # repetition check
        if re.search(r'\b(\w+)( \1\b)+', content):
            issues.append("Repetition detected")

        # readability
        if content.count(".") > 15:
            score += 10

        return {
            "score": min(score, 100),
            "issues": issues
        }