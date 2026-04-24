def detect_intent(keyword: str) -> str:
    k = keyword.lower()

    if any(word in k for word in ["dog", "cat", "pet", "puppy"]):
        return "pet"

    elif any(word in k for word in ["job", "vacancy", "recruitment", "salary"]):
        return "career"

    elif any(word in k for word in ["exam", "syllabus", "result", "admit card"]):
        return "education"

    elif any(word in k for word in ["how to", "kese", "kaise", "guide"]):
        return "guide"

    else:
        return "general"