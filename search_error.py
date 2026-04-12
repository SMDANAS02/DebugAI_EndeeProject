import sys
import os
import json
import requests
import msgpack
from sentence_transformers import SentenceTransformer
from colorama import Fore, Style, init

init(autoreset=True)

ENDEE_BASE_URL = os.getenv("ENDEE_URL", "http://localhost:8080")
INDEX_NAME = "debug_errors"
MODEL_NAME = "all-MiniLM-L6-v2"
DATASET_PATH = "dataset.json"
DEFAULT_TOP_K = 3

_model = None
_metadata_cache = {}


def load_metadata_cache():
    """Load metadata from dataset.json into memory"""
    global _metadata_cache
    if not _metadata_cache:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for i, rec in enumerate(data):
            _metadata_cache[str(i)] = {
                "error": rec["error"],
                "solution": rec["solution"],
                "language": rec["language"],
                "tags": rec.get("tags", [])
            }
    return _metadata_cache


def get_model():
    global _model
    if _model is None:
        print(Fore.CYAN + "[~] Loading model...")
        _model = SentenceTransformer(MODEL_NAME)
        print(Fore.GREEN + "[✓] Model ready\n")
    return _model


def search(query, top_k=DEFAULT_TOP_K):
    model = get_model()
    query_vector = model.encode(query)
    if hasattr(query_vector, 'tolist'):
        query_vector = query_vector.tolist()
    payload = {
        "vector": query_vector,
        "k": top_k
    }
    try:
        r = requests.post(
            f"{ENDEE_BASE_URL}/api/v1/index/{INDEX_NAME}/search",
            json=payload,
            timeout=10
        )
        r.raise_for_status()
        
        # Handle MessagePack response
        if r.headers.get('Content-Type') == 'application/msgpack':
            data = msgpack.unpackb(r.content, raw=False)
            results = []
            metadata_cache = load_metadata_cache()
            
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, (list, tuple)) and len(item) >= 2:
                        distance, vector_id = item[0], item[1]
                        
                        # Get metadata from cache
                        metadata = metadata_cache.get(str(vector_id), {})
                        
                        results.append({
                            "score": distance,
                            "id": vector_id,
                            "metadata": metadata
                        })
            return results
        else:
            return r.json().get("results", [])
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "\n[✗] Cannot reach Endee. Is Docker running?")
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"\n[✗] Search error: {e}")
        return []


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
    print(Fore.CYAN + "  DebugAI — Semantic Error Search")
    print(Fore.CYAN + "  Powered by Endee Vector DB")
    print(Fore.CYAN + "=" * 50)
    print(Fore.WHITE + "\n  Type your error. Type 'exit' to quit.\n")

    get_model()
    load_metadata_cache()

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

        results = search(user_input)
        display_results(user_input, results)


if __name__ == "__main__":
    main()
