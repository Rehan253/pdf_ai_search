import os
import json
from datetime import datetime
from search_engine import SearchEngine


def save_results_to_json(query, results, output_dir="data/results"):
    """
    Save the search query and its results to a JSON file.
    File name will include timestamp.
    """
    os.makedirs(output_dir, exist_ok=True)

    data = {
        "query": query,
        "results": [
            {
                "score": res["distance"],
                "filename": res["metadata"]["filename"],
                "page": res["metadata"]["page"],
            }
            for res in results
        ],
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"search_results_{timestamp}.json"
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n[INFO] Results saved to: {output_path}\n")


def main():
    print("\n===============================")
    print("   AI PDF Semantic Search")
    print("===============================\n")

    engine = SearchEngine()

    while True:
        query = input("\nEnter your question (or type 'exit' to quit):\n>> ")

        if query.lower().strip() == "exit":
            print("Goodbye!")
            break

        if not query.strip():
            print("[WARN] Empty query, please type something.")
            continue

        results = engine.search(query, k=5)

        print("\n=== TOP RESULTS ===\n")

        if not results:
            print("No results found.")
            continue

        for res in results:
            print(f"Score: {res['distance']:.4f}")
            print(f"File: {res['metadata']['filename']}")
            print(f"Page: {res['metadata']['page']}")
            print("-----------------------------")

        # NEW: Ask user if they want to save results
        choice = input("\nDo you want to save these results to JSON? (y/n): ").strip().lower()
        if choice == "y":
            save_results_to_json(query, results)


if __name__ == "__main__":
    main()
