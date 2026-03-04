import json
import glob
from collections import defaultdict

def analyze_latest_results():
    """Analyze the most recent test results"""
    
    # Find latest results file
    result_files = glob.glob("data/results_*.json")
    if not result_files:
        print("No results files found!")
        return
    
    latest_file = max(result_files)
    print(f"📊 Analyzing: {latest_file}\n")
    
    # Load results
    with open(latest_file, 'r') as f:
        results = json.load(f)
    
    # Organize by category and model
    by_category = defaultdict(lambda: defaultdict(list))
    
    for r in results:
        if r["success"]:
            by_category[r["category"]][r["model"]].append(r)
    
    # Analyze each category
    print("="*70)
    print("CATEGORY ANALYSIS")
    print("="*70)
    
    for category, models in by_category.items():
        print(f"\n📂 {category.upper()}:")
        print(f"{'Model':<20} {'Avg Latency':<15} {'Avg Cost':<15} {'Queries'}")
        print("-"*70)
        
        for model_name, model_results in models.items():
            avg_latency = sum(r["latency_seconds"] for r in model_results) / len(model_results)
            avg_cost = sum(r["estimated_cost"] for r in model_results) / len(model_results)
            
            print(f"{model_name:<20} {avg_latency:<15.3f} ${avg_cost:<14.6f} {len(model_results)}")
        
        # Find best for this category
        best_speed = min(models.items(), 
                        key=lambda x: sum(r["latency_seconds"] for r in x[1])/len(x[1]))
        best_cost = min(models.items(),
                       key=lambda x: sum(r["estimated_cost"] for r in x[1])/len(x[1]))
        
        print(f"\n  🏆 Fastest: {best_speed[0]}")
        print(f"  💰 Cheapest: {best_cost[0]}")
    
    # Overall recommendations
    print("\n" + "="*70)
    print("💡 INITIAL ROUTING INSIGHTS")
    print("="*70)
    
    print("""
Based on the data:

1. SIMPLE_QA queries:
   → Use cheapest, fastest model (likely Groq Llama)
   → High speed matters more than quality for factual answers

2. REASONING queries:
   → May need more capable models (GPT-4o, larger Llama)
   → Balance cost vs accuracy

3. CREATIVE queries:
   → Quality matters most
   → May justify higher cost models

4. CODE queries:
   → Accuracy critical
   → Test which model has fewer syntax errors

5. ANALYSIS queries:
   → Depth matters
   → May need larger models

Next steps:
- Manual quality review of outputs
- Build quality scoring system
- Create routing rules based on prompt type
""")

if __name__ == "__main__":
    analyze_latest_results()