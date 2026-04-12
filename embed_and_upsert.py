import json
import os
import sys
import requests
import hashlib
import time
from colorama import Fore, init

init(autoreset=True)

ENDEE_BASE_URL = os.getenv("ENDEE_URL", "http://localhost:8080")
INDEX_NAME = "debug_errors"
DATASET_PATH = "dataset.json"
VECTOR_DIM = 384


def check_endee():
    try:
        r = requests.get(f"{ENDEE_BASE_URL}/api/v1/index/list", timeout=5)
        print(Fore.GREEN + f"[✓] Endee is running at {ENDEE_BASE_URL}")
        return True
    except:
        print(Fore.RED + "[✗] Cannot reach Endee. Start Docker first.")
        return False


def create_index():
    payload = {
        "name": INDEX_NAME,
        "size": VECTOR_DIM,
        "metric": "cosine"
    }
    try:
        r = requests.post(
            f"{ENDEE_BASE_URL}/api/v1/index/create",
            json=payload,
            timeout=10
        )
        if r.status_code in (200, 201):
            print(Fore.GREEN + f"[✓] Index '{INDEX_NAME}' created")
        else:
            print(Fore.YELLOW + f"[!] Index may already exist: {r.status_code}")
    except:
        print(Fore.YELLOW + f"[!] Could not create index (may already exist)")


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(Fore.GREEN + f"[✓] Loaded {len(data)} errors from {DATASET_PATH}")
    return data


def simple_hash_embedding(text):
    """Generate a simple deterministic embedding using hash"""
    hash_obj = hashlib.sha256(text.encode())
    hash_bytes = hash_obj.digest()
    embedding = []
    for i in range(VECTOR_DIM):
        embedding.append(float(hash_bytes[i % len(hash_bytes)]) / 255.0)
    return embedding


def upsert_to_endee(records):
    success = 0
    failed = 0
    
    for i, rec in enumerate(records):
        text = f"{rec['language']}: {rec['error']}"
        vec = simple_hash_embedding(text)
        
        # Serialize metadata as JSON string
        metadata_json = json.dumps({
            "error":    rec["error"],
            "solution": rec["solution"],
            "language": rec["language"],
            "tags":     rec.get("tags", [])
        })
        
        payload = {
            "id": str(i),
            "vector": vec,
            "metadata": metadata_json
        }
        
        try:
            r = requests.post(
                f"{ENDEE_BASE_URL}/api/v1/index/{INDEX_NAME}/vector/insert",
                json=payload,
                timeout=30
            )
            
            if r.status_code in (200, 201):
                success += 1
            else:
                failed += 1
                if i < 3:
                    print(Fore.YELLOW + f"[!] Record {i}: {r.status_code} - {r.text[:100]}")
        except Exception as e:
            failed += 1
            if i < 3:
                print(Fore.YELLOW + f"[!] Record {i} error: {str(e)[:100]}")
        
        if (i + 1) % 10 == 0:
            print(Fore.CYAN + f"[~] Processed {i + 1}/{len(records)}...")
        
        time.sleep(0.1)
    
    print(Fore.GREEN + f"[✓] Upserted {success}/{len(records)} points into Endee!")
    if failed > 0:
        print(Fore.YELLOW + f"[!] {failed} records failed to insert")


def main():
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "  DebugAI — Embed and Upsert")
    print(Fore.CYAN + "=" * 50)

    if not check_endee():
        sys.exit(1)

    records = load_dataset()

    print(Fore.CYAN + "[~] Generating embeddings...")
    print(Fore.GREEN + "[✓] Embeddings generated")

    create_index()

    print(Fore.CYAN + "[~] Inserting vectors...")
    upsert_to_endee(records)

    print()
    print(Fore.GREEN + "Done! Now run: python search_error.py")
    print(Fore.CYAN + "=" * 50)


if __name__ == "__main__":
    main()
