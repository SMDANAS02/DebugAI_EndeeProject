#  DebugAI — AI Error Debugging Assistant using Endee Vector Database

A practical AI developer tool that allows programmers to paste error messages and retrieve the most relevant solutions using **semantic search powered by Endee vector database**.

This project demonstrates how **vector databases + embeddings** can build intelligent debugging assistants.

---

# 📋 Table of Contents

- Features
- System Architecture
- Why Endee?
- Tech Stack
- Quick Start
- Project Structure
- How It Works
- Example Usage
- Author

---

# ✨ Features

🔎 Semantic search for programming errors  
⚡ Fast vector similarity search using **Endee**  
🧠 Error message embedding using **Sentence Transformers**  
📂 Dataset of common programming errors and solutions  
🐳 Docker-based Endee deployment  
💻 Simple command-line interface for searching solutions

---

# 🏗️ System Architecture
User Error Message
│
▼
Sentence Transformer
(all-MiniLM-L6-v2)
│
▼
Vector Embedding
(384 dimension)
│
▼
Endee Vector Database
(HNSW ANN Search)
│
▼
Most Similar Error + Solution

---

# 🔷 Why Endee?

This project uses **Endee vector database** because:

| Feature | Benefit |
|------|------|
| High-performance ANN search | Very fast similarity search |
| HNSW indexing | Efficient vector retrieval |
| Docker deployment | Easy local setup |
| Metadata support | Store error type, language, tags |
| Open source | Fully local and privacy-friendly |

Endee enables building **AI developer tools without external APIs**.

---

# 🛠️ Tech Stack

| Layer | Technology | Purpose |
|------|------|------|
| Programming | Python | Main implementation |
| Vector Database | Endee | Store embeddings |
| Embedding Model | all-MiniLM-L6-v2 | Convert errors to vectors |
| ML Library | Sentence Transformers | Generate embeddings |
| Deployment | Docker | Run Endee server |

---

# ⚡ Quick Start

## 1 Install dependencies
pip install -r requirements.txt


---

## 2 Start Endee Vector Database


docker run -p 8080:8080 endeeio/endee-server


Open Endee dashboard:


http://localhost:8080


---

## 3 Insert embeddings into Endee


python embed_and_upsert.py


This will:

- load dataset
- generate embeddings
- insert vectors into Endee

---

## 4 Search for errors


python search_error.py


Example query:


ModuleNotFoundError: No module named numpy


Output:


Similar Error:
ModuleNotFoundError

Solution:
Install the package using pip install numpy


---

# 📁 Project Structure


DebugAI_EndeeProject
│
├── dataset.json
├── embed_and_upsert.py
├── search_error.py
├── search_error_demo.py
├── requirements.txt
└── README.md


---

# ⚙️ How It Works

### Step 1 — Dataset

The project contains a dataset of programming errors and solutions.

Example:

```json
{
  "error": "ModuleNotFoundError: No module named numpy",
  "solution": "Install the package using pip install numpy",
  "language": "Python"
}
Step 2 — Embedding

Each error message is converted into a 384-dimensional vector embedding using:

sentence-transformers/all-MiniLM-L6-v2
Step 3 — Vector Storage

Embeddings are stored inside Endee vector database.

Example structure:

vector_id
vector_embedding
metadata:
  error
  solution
  language
Step 4 — Semantic Search

When a user enters an error:

Error message is embedded
Endee performs ANN similarity search
Top matching errors are returned
Best solution is displayed
💡 Example Use Cases

Developer debugging assistant
AI coding tools
Programming help systems
IDE debugging plugins

👨‍💻 Author

Anas

GitHub: https://github.com/SMDANAS02

* Acknowledgements

Endee Vector Database
Sentence Transformers
Open-source ML community
