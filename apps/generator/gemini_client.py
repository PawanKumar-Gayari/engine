from google import genai
import os


def generate_gemini_content(keyword):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Write a detailed SEO optimized article on: {keyword}

    Include:
    - Title
    - Introduction
    - Headings
    - Conclusion
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",   # ✅ correct model
            contents=prompt
        )

        content = response.text

        if not content:
            raise Exception("Empty response from Gemini")

        return content.strip()

    except Exception as e:
        raise Exception(f"Gemini Error: {str(e)}")