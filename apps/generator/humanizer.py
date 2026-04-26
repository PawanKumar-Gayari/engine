import random
import re


class Humanizer:
    """
    🚀 PRO MAX HUMANIZER (AI → HUMAN TRANSFORMER)

    Features:
    - sentence variation
    - filler injection (controlled)
    - tone shifting (human-like)
    - repetition removal
    - sentence length variation
    - conversational style
    - readability boost
    """

    def __init__(self):

        self.fillers = [
            "In simple terms,",
            "Let's understand this clearly,",
            "Interestingly,",
            "Now here's the important part,",
            "To make it easier,",
            "You might be wondering,"
        ]

        self.human_phrases = [
            "this is important to know",
            "you should remember that",
            "this plays a key role",
            "it helps you understand better"
        ]

        self.replacements = {
            "This article": "In this guide",
            "In conclusion": "To sum up",
            "It is important to note": "You should know",
            "Moreover": "Also",
            "However": "But"
        }

    # =========================
    # 🚀 MAIN
    # =========================
    def humanize(self, content: str) -> str:

        if not content:
            return content

        content = self._clean_text(content)
        content = self._add_variation(content)
        content = self._human_tone(content)
        content = self._fix_repetition(content)
        content = self._sentence_mix(content)

        return content.strip()

    # =========================
    # 🧹 CLEAN
    # =========================
    def _clean_text(self, text):

        text = re.sub(r"\s+", " ", text)
        return text.strip()

    # =========================
    # 🔹 VARIATION
    # =========================
    def _add_variation(self, text):

        sentences = re.split(r'(?<=[.!?]) +', text)
        new = []

        for s in sentences:
            s = s.strip()

            if not s:
                continue

            if random.random() > 0.75:
                s = random.choice(self.fillers) + " " + s

            new.append(s)

        return " ".join(new)

    # =========================
    # 🧠 HUMAN TONE
    # =========================
    def _human_tone(self, text):

        for k, v in self.replacements.items():
            text = text.replace(k, v)

        # add human phrases randomly
        if random.random() > 0.6:
            text += " " + random.choice(self.human_phrases) + "."

        return text

    # =========================
    # 🔁 REMOVE REPETITION
    # =========================
    def _fix_repetition(self, text):

        words = text.split()
        seen = set()
        result = []

        for w in words:
            lw = w.lower()

            # allow common words
            if lw in ["the", "is", "and", "of", "to"]:
                result.append(w)
                continue

            if lw not in seen:
                result.append(w)
                seen.add(lw)

        return " ".join(result)

    # =========================
    # ✂️ SENTENCE MIX
    # =========================
    def _sentence_mix(self, text):

        sentences = re.split(r'(?<=[.!?]) +', text)

        mixed = []

        for s in sentences:

            # break long sentence
            if len(s.split()) > 25:
                parts = s.split(",")
                mixed.extend(parts)
            else:
                mixed.append(s)

        return " ".join(mixed)