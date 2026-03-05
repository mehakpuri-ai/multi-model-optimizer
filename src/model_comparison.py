import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from google import genai

# Load environment variables
load_dotenv()

# Model configurations
MODELS = {
    "llama-3.1-8b-instant": {
        "provider": "groq",
        "cost_input": 0.00,
        "cost_output": 0.00,
    },
    "gemini-3-flash-preview": {
        "provider": "google",
        "cost_input": 0.125,
        "cost_output": 0.375,
    },
}


class ModelTester:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.google_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.results = []

    def estimate_tokens(self, text):
        return len(text) // 4

    def calculate_cost(self, model_name, input_text, output_text):
        config = MODELS[model_name]

        input_tokens = self.estimate_tokens(input_text)
        output_tokens = self.estimate_tokens(output_text)

        cost = (
            (input_tokens / 1_000_000) * config["cost_input"]
            + (output_tokens / 1_000_000) * config["cost_output"]
        )

        return cost

    def query_groq(self, model_name, prompt):
        try:
            start = time.time()

            response = self.groq_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )

            latency = time.time() - start
            output = response.choices[0].message.content
            cost = self.calculate_cost(model_name, prompt, output)

            return {
                "success": True,
                "output": output,
                "latency": latency,
                "cost": cost
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "latency": 0,
                "cost": 0
            }

    def query_google(self, model_name, prompt):
        try:
            start = time.time()

            response = self.google_client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            latency = time.time() - start
            output = response.text
            cost = self.calculate_cost(model_name, prompt, output)

            return {
                "success": True,
                "output": output,
                "latency": latency,
                "cost": cost
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "latency": 0,
                "cost": 0
            }

    def test_prompt(self, prompt, category):
        print(f"\n📝 Testing: '{prompt[:50]}...'")

        for model_name, config in MODELS.items():
            print(f"  ⏳ {model_name}...", end=" ")

            if config["provider"] == "groq":
                result = self.query_groq(model_name, prompt)

            elif config["provider"] == "google":
                result = self.query_google(model_name, prompt)

            self.results.append({
                "timestamp": datetime.now().isoformat(),
                "model": model_name,
                "provider": config["provider"],
                "category": category,
                "prompt": prompt,
                "success": result["success"],
                "output": result.get("output", ""),
                "error": result.get("error", ""),
                "latency_seconds": round(result["latency"], 3),
                "estimated_cost": round(result["cost"], 6)
            })

            if result["success"]:
                print(f"✅ {result['latency']:.2f}s, ${result['cost']:.6f}")
            else:
                print(f"❌ {result.get('error','Failed')[:40]}")

            time.sleep(0.5)

    def run_tests(self, prompts_file="data/test_prompts.json"):
        print("🚀 Starting model comparison tests...\n")

        with open(prompts_file, "r") as f:
            prompts_data = json.load(f)

        for category, prompts in prompts_data.items():

            print("\n" + "=" * 60)
            print(f"📂 Category: {category.upper()}")
            print("=" * 60)

            for prompt in prompts:
                self.test_prompt(prompt, category)

        self.save_results()
        self.print_summary()

    def save_results(self):
        output_file = f"data/results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n💾 Results saved to: {output_file}")

    def print_summary(self):
        print("\n" + "=" * 60)
        print("📊 SUMMARY STATISTICS")
        print("=" * 60)

        stats = {}

        for model_name in MODELS.keys():

            model_results = [r for r in self.results if r["model"] == model_name]
            successful = [r for r in model_results if r["success"]]

            if successful:

                avg_latency = sum(r["latency_seconds"] for r in successful) / len(successful)
                total_cost = sum(r["estimated_cost"] for r in successful)
                success_rate = len(successful) / len(model_results) * 100

                stats[model_name] = {
                    "avg_latency": avg_latency,
                    "total_cost": total_cost,
                    "success_rate": success_rate,
                    "total_queries": len(model_results)
                }

        for model_name, data in stats.items():

            print(f"\n{model_name}")
            print(f"  Queries: {data['total_queries']}")
            print(f"  Success Rate: {data['success_rate']:.1f}%")
            print(f"  Avg Latency: {data['avg_latency']:.3f}s")
            print(f"  Total Cost: ${data['total_cost']:.6f}")

        fastest = min(stats.items(), key=lambda x: x[1]["avg_latency"])
        cheapest = min(stats.items(), key=lambda x: x[1]["total_cost"])

        print("\n🏆 BEST MODELS")
        print(f"Fastest: {fastest[0]} ({fastest[1]['avg_latency']:.3f}s)")
        print(f"Cheapest: {cheapest[0]} (${cheapest[1]['total_cost']:.6f})")


if __name__ == "__main__":
    tester = ModelTester()
    tester.run_tests()