import sys
import json
import hashlib
from colorama import Fore, Style, init

init(autoreset=True)

DATASET_PATH = "dataset.json"
VECTOR_DIM = 384


def simple_hash_embedding(text):
    """Generate a simple deterministic embedding using hash"""
    hash_obj = hashlib.sha256(text.encode())
    hash_bytes = hash_obj.digest()
    embedding = []
    for i in range(VECTOR_DIM):
        embedding.append(float(hash_bytes[i % len(hash_bytes)]) / 255.0)
    return embedding


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = sum(a * a for a in vec1) ** 0.5
    mag2 = sum(b * b for b in vec2) ** 0.5
    if mag1 == 0 or mag2 == 0:
        return 0
    return dot_product / (mag1 * mag2)


def search_local(query, records, top_k=3):
    """Search records locally using cosine similarity"""
    query_vec = simple_hash_embedding(query)
    
    results = []
    for i, rec in enumerate(records):
        text = f"{rec['language']}: {rec['error']}"
        rec_vec = simple_hash_embedding(text)
        similarity = cosine_similarity(query_vec, rec_vec)
        results.append({
            "score": similarity,
            "id": str(i),
            "metadata": {
                "error": rec["error"],
                "solution": rec["solution"],
                "language": rec["language"],
                "tags": rec.get("tags", [])
            }
        })
    
    # Sort by similarity and return top_k
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def display_results(query, results):
    print()
    print(Fore.YELLOW + f'  Query: "{query}"')
    print(Fore.WHITE + "  " + "-" * 50)

    if not results:
        print(Fore.RED + "\n  No results found. Try a different query.")
        return

    for rank, hit in enumerate(results, start=1):
        score = hit.get("score", 0.0)
        meta = hit.get("metadata", {})
        
        error = meta.get("error", "N/A")
        solution = meta.get("solution", "N/A")
        language = meta.get("language", "")
        tags = meta.get("tags", [])

        print()
        print(Fore.YELLOW + f"  #{rank}  {error}")
        print(f"       Language  : " + Fore.CYAN + language)
        print(f"       Similarity: " + Fore.GREEN + f"{score:.2%}")
        if tags:
            print(f"       Tags      : " + Fore.BLUE + "  ".join(f"#{t}" for t in tags[:5]))
        print()
        print(Fore.GREEN + f"       Solution: {solution}")
        print(Fore.WHITE + "  " + "-" * 50)


def main():
    print()
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "  DebugAI — Semantic Error Search (Demo)")
    print(Fore.CYAN + "  Local Vector Search")
    print(Fore.CYAN + "=" * 50)
    print(Fore.WHITE + "\n  Type your error. Type 'exit' to quit.\n")

    # Load dataset
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    
    print(Fore.GREEN + f"[✓] Loaded {len(records)} errors\n")

    while True:
        try:
            user_input = input(Fore.CYAN + "  Search > " + Style.RESET_ALL).strip()
        except (KeyboardInterrupt, EOFError):
            print(Fore.CYAN + "\n\n  Goodbye!\n")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "q"):
            print(Fore.CYAN + "\n  Goodbye!\n")
            break

        results = search_local(user_input, records)
        display_results(user_input, results)


if __name__ == "__main__":
    main()
