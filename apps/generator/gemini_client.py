from google import genai
import os
from dotenv import load_dotenv

# 🔥 Ensure .env is loaded
load_dotenv()


def generate_gemini_content(keyword: str) -> str:
    """
    Generate SEO optimized article using Gemini API
    """

    # 🔑 Load API key
    api_key = os.getenv("GEMINI_API_KEY")

    print("\n===== GEMINI DEBUG =====")
    print("KEY FOUND:", bool(api_key))
    print("KEY PREVIEW:", api_key[:8] + "..." if api_key else None)
    print("KEYWORD:", keyword)

    if not api_key:
        raise Exception("GEMINI_API_KEY not found in environment")

    try:
        # 🤖 Create client
        client = genai.Client(api_key=api_key)

        # ✍️ Prompt
        prompt = f"""
Write a detailed SEO optimized blog article on: {keyword}

Structure:
- Catchy Title
- Introduction (engaging)
- Multiple Headings (H2/H3)
- Detailed Explanation
- Bullet Points where needed
- Conclusion

Make it human-like and easy to read.
"""

        print("🚀 Calling Gemini API...")

        # 📡 API call
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        # 📄 Extract content safely
        content = getattr(response, "text", None)

        if not content:
            raise Exception("Empty response from Gemini")

        print("✅ Gemini Success\n")

        return content.strip()

    except Exception as e:
        print("❌ GEMINI ERROR:", str(e))
        raise Exception(f"Gemini Error: {str(e)}")