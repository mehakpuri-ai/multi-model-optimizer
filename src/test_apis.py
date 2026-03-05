import os
from dotenv import load_dotenv
from groq import Groq
from google import genai

# Load environment variables
load_dotenv()

def test_groq():
    """Test Groq API"""
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Say 'Groq works!'"}],
            max_tokens=10
        )
        print("✅ Groq:", response.choices[0].message.content)
        return True
    except Exception as e:
        print("❌ Groq failed:", str(e))
        return False

def test_google():
    """Test Google (Gemini) API"""
    try:
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3-flash-preview",   # Correct modern Gemini model
            contents="Say 'Google works!'"
        )

        print("✅ Google:", response.text)
        return True

    except Exception as e:
        print("❌ Google failed:", e)
        return False


if __name__ == "__main__":
    print("\n🧪 Testing API Connections...\n")

    results = {
        "Groq": test_groq(),
        "Google": test_google()
    }

    print("\n📊 Results:")
    working = sum(results.values())
    total = len(results)

    print(f"✅ {working}/{total} APIs working")

    if working < total:
        print("\n⚠️ Some APIs failed. Check your keys and try again.")
    else:
        print("\n🎉 All APIs connected! Ready to build.")