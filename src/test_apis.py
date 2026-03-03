import os
from dotenv import load_dotenv

from groq import Groq
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_groq():
    """Test Groq API"""
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')
        response = model.generate_content("Say 'Google works!'")
        print("✅ Google:", response.text)
        return True
    except Exception as e:
        print("❌ Google failed:", str(e))
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
        print("\n⚠️  Some APIs failed. Check your keys and try again.")
    else:
        print("\n🎉 All APIs connected! Ready to build.")