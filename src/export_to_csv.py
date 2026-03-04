import json
import csv
import glob

def export_to_csv():
    """Export results to CSV for easy analysis"""
    
    # Find latest results
    result_files = glob.glob("data/results_*.json")
    if not result_files:
        print("No results files found!")
        return
    
    latest_file = max(result_files)
    
    # Load results
    with open(latest_file, 'r') as f:
        results = json.load(f)
    
    # Export to CSV
    csv_file = latest_file.replace('.json', '.csv')
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✅ Exported to: {csv_file}")
    print(f"   Open in Excel/Google Sheets for analysis")

if __name__ == "__main__":
    export_to_csv()