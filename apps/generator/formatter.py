import re


def format_article(raw_content: str) -> str:
    """
    🚀 HUMAN BLOG FORMATTER (FINAL)

    Output:
    - Clean readable blog
    - Proper headings
    - Bullet points fixed
    - No HTML junk
    """

    if not raw_content:
        return ""

    # =========================
    # 🔥 STEP 1: CLEAN HTML
    # =========================
    content = re.sub(r"<[^>]+>", "", raw_content)

    # =========================
    # 🔥 STEP 2: NORMALIZE TEXT
    # =========================
    content = content.replace("**", "")
    content = content.replace("\t", " ")
    content = re.sub(r"[ ]{2,}", " ", content)

    # =========================
    # 🔥 STEP 3: FIX BULLETS
    # =========================
    content = content.replace("+ ", "\n• ")
    content = content.replace("- ", "\n• ")

    # =========================
    # 🔥 STEP 4: REMOVE DUPLICATES
    # =========================
    content = _remove_duplicates(content)

    # =========================
    # 🔥 STEP 5: BUILD STRUCTURE
    # =========================
    final = _build_article(content)

    return final.strip()


# =========================
# 🔁 REMOVE DUPLICATE LINES
# =========================
def _remove_duplicates(text):

    seen = set()
    result = []

    for line in text.split("\n"):
        clean = line.strip().lower()

        if len(clean) > 25:
            if clean in seen:
                continue
            seen.add(clean)

        result.append(line)

    return "\n".join(result)


# =========================
# 🧠 MAIN STRUCTURE ENGINE
# =========================
def _build_article(content):

    lines = content.split("\n")

    final = []
    buffer = []

    def flush():
        if buffer:
            paragraph = " ".join(buffer).strip()
            if paragraph:
                final.append(paragraph + "\n")
            buffer.clear()

    for line in lines:
        line = line.strip()

        if not line:
            flush()
            continue

        # 🔥 HEADINGS AUTO DETECT
        lower = line.lower()

        if lower in [
            "introduction",
            "syllabus",
            "exam pattern",
            "important topics",
            "preparation tips",
            "additional tips",
            "conclusion",
            "overview"
        ]:
            flush()
            final.append("\n" + line.upper() + "\n")

        elif line.startswith("•"):
            flush()
            final.append(line)

        else:
            buffer.append(line)

    flush()

    return "\n".join(final)