# 🚀 Endee Internship 2026 – Submission Repository

<div align="center">

![Endee](https://img.shields.io/badge/Endee-Vector_Database-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge\&logo=python)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

### **AI Error Solution Finder**

*An AI system that detects programming errors and suggests solutions using vector embeddings.*

</div>

---

# 👨‍💻 Candidate Information

| Field               | Details                                 |
| ------------------- | --------------------------------------- |
| **Name**            | Mohamed Anas                            |
| **Institution**     | V S B engineering college               |
| **Email**           |smohamedanas02@gmail.com                 |
| **GitHub**          |https://github.com/SMDANAS02             |
| **Submission Date** | April 2026                              |
| **Project**         | AI Error Solution Finder                |

---

# 🎯 Project Overview

This project builds an **AI-powered system that analyzes programming errors and suggests solutions automatically**.

Instead of searching errors manually on Google or StackOverflow, the system uses **vector embeddings and semantic search** to find similar errors from a database.

Example dataset:

```json
{
  "error": "ModuleNotFoundError: No module named numpy",
  "solution": "Install the package using pip install numpy",
  "language": "Python"
}
```

The system converts error messages into **vector embeddings** and stores them in a **vector database**.
When a new error is given, the system finds **similar errors and their solutions**.

---

# 🌟 Key Features

### 🔍 Semantic Error Search

* Finds **similar errors even if the text is different**
* Uses **vector embeddings**
* Supports multiple programming languages

Example:

```
Query: "numpy module missing"
Result: "ModuleNotFoundError: No module named numpy"
```

---

### 🤖 AI Based Solution Suggestion

Steps:

```
User Error
     ↓
Embedding Model
     ↓
Vector Database Search
     ↓
Retrieve Similar Errors
     ↓
Return Best Solution
```

---

# 🏗️ System Architecture

```
User Input Error
       ↓
Embedding Model
(sentence-transformers)
       ↓
Vector Database
(Endee / FAISS)
       ↓
Similarity Search
       ↓
Retrieve Solution
```

---

# ⚙️ Technology Stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Embeddings      | sentence-transformers |
| Vector Database | Endee                 |
| Backend         | Python                |
| Dataset         | JSON                  |
| AI Model        | all-MiniLM-L6-v2      |

---

# 📊 Workflow

### Step 1 — Dataset Creation

Dataset contains **error and solution pairs**.

Example:

```
Error → Solution
```

---

### Step 2 — Embedding Generation

Error messages are converted into **384 dimensional vectors** using:

```
sentence-transformers/all-MiniLM-L6-v2
```

---

### Step 3 — Vector Storage

Embeddings are stored inside **Endee Vector Database**.

---

### Step 4 — Query Search

When a user enters an error:

1. Convert query to embedding
2. Perform similarity search
3. Return closest matching error
4. Show solution

---

# 🚀 Quick Start

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/project-name.git
cd project-name
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Project

```bash
python main.py
```

---

# 📂 Project Structure

```
project/
│
├── data/
│   └── errors.json
│
├── embeddings/
│   └── generate_embeddings.py
│
├── search/
│   └── search_error.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 📈 Example Usage

Input:

```
Error: ModuleNotFoundError: numpy
```

Output:

```
Solution: Install the package using

pip install numpy
```

---

# 🎯 Future Improvements

* Support more programming languages
* Web interface for error search
* Add LLM explanation for solutions
* Larger error dataset

---

# 📞 Contact

**Name:** Mohamed Anas S
**Email:** smohamedanas02@gmail.com
**GitHub:** https://github.com/SMDANAS02

---

✅ **Project Status: Completed**

---

