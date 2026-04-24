def detect_intent(keyword: str) -> str:
    k = keyword.lower().strip()

    # =========================
    # 🐶 PET / ANIMAL
    # =========================
    pet_keywords = [
        "dog", "cat", "pet", "puppy", "kitten",
        "dog food", "dog care", "dog training",
        "breed", "animal", "pet care"
    ]

    # =========================
    # 💼 JOB / CAREER
    # =========================
    job_keywords = [
        "job", "vacancy", "recruitment", "bharti", "form",
        "apply online", "salary", "notification",
        "government job", "govt job", "latest job",
        "sarkari", "post", "posts"
    ]

    # =========================
    # 📚 EDUCATION / EXAM
    # =========================
    education_keywords = [
        "exam", "syllabus", "result", "admit card",
        "question paper", "previous year",
        "cut off", "answer key", "pattern",
        "marks", "qualification"
    ]

    # =========================
    # 📖 GUIDE / HOW-TO
    # =========================
    guide_keywords = [
        "how to", "kese", "kaise", "guide",
        "steps", "process", "tips", "tricks",
        "method", "ka tarika", "kaise kare"
    ]

    # =========================
    # 🧠 DETECTION LOGIC (priority based)
    # =========================
    if any(word in k for word in pet_keywords):
        return "pet"

    elif any(word in k for word in job_keywords):
        return "career"

    elif any(word in k for word in education_keywords):
        return "education"

    elif any(word in k for word in guide_keywords):
        return "guide"

    # 🔥 fallback smart detection
    if "202" in k or "2025" in k or "2026" in k:
        return "career"

    return "general"