from openai import OpenAI
import os


def generate_openai_content(keyword):

    api_key = os.getenv("OPENAI_API_KEY")

    # 🔐 SAFETY CHECK
    if not api_key:
        raise Exception("OPENAI_API_KEY not found in environment")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Write a detailed SEO optimized article on: {keyword}

    Include:
    - Title
    - Introduction
    - Headings
    - Conclusion
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content

        if not content:
            raise Exception("Empty response from OpenAI")

        return content.strip()

    except Exception as e:
        # 🔥 Proper error pass
        raise Exception(f"OpenAI Error: {str(e)}")