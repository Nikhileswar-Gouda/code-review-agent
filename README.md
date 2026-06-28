

# 🤖 Autonomous Code Review & Bug Fix Agent

> Powered by **Claude AI (Anthropic)** — the most advanced AI + **Genetic Algorithms**



![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)




![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)




![Claude AI](https://img.shields.io/badge/Claude_AI-Anthropic-blueviolet?style=flat-square)




![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)




![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)



---

## 📌 Overview

An AI-powered autonomous agent that **automatically detects bugs** in Python code, **evolves the best fix** using a custom Genetic Algorithm, validates the fixes, and generates a **detailed PDF report** — all inside a beautiful Streamlit web UI.

> 💡 Unlike other tools that just detect bugs — this agent **evolves and improves fixes** across multiple generations using natural selection!

---

## ✨ Features

- 🐛 **Intelligent Bug Detection** — Powered by Anthropic's Claude AI
- 🧬 **Genetic Algorithm Fix Evolution** — Evolves the best fix over multiple generations
- 🧠 **Smart Memory System** — Learns and recalls similar fixes from past sessions
- ✅ **Fix Validator** — Validates syntax and scores quality of each fix
- 📄 **PDF Report Generator** — Auto-generates a detailed downloadable report
- 🌐 **Beautiful Streamlit UI** — Clean, interactive, and easy to use
- ⚡ **Real-time Analysis** — Instant bug detection and fix evolution

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.x | Core language |
| Streamlit | Interactive web UI |
| Claude AI (Anthropic) | Bug detection & fix generation |
| Genetic Algorithm | Fix evolution (custom, no library) |
| fpdf2 | PDF report generation |
| JSON | Local memory storage |

---

## 📁 Project Structure

```
code-review-agent/
├── app.py            # Main Streamlit application
├── detector.py       # Bug detection using Claude AI
├── ga_engine.py      # Genetic Algorithm engine
├── validator.py      # Fix syntax validator
├── memory.py         # Local JSON memory system
├── report.py         # PDF report generator
├── requirements.txt  # Dependencies
└── README.md         # Documentation
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Nikhileswar-Gouda/code-review-agent.git
cd code-review-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your FREE Anthropic API Key
- Go to [console.anthropic.com](https://console.anthropic.com)
- Sign up and create a free API key

### 4. Run the app

```bash
python -m streamlit run app.py
```

### 5. Open in browser
- Go to http://localhost:8501
- Paste your Anthropic API Key in the sidebar

---

## 🚀 How to Use

1. **Code Input tab** — Paste your Python code or load a sample
2. **Click Start Analysis** — Claude AI detects all bugs instantly
3. **Bug Detection tab** — View bugs with severity levels
4. **Fix Evolution tab** — Click Evolve Fixes to run Genetic Algorithm
5. **Results & Report tab** — Download your PDF report

---

## 🧬 How the Genetic Algorithm Works

```
Step 1: Bug detected by Claude AI
Step 2: Generate 4 fix candidates
Step 3: Score each candidate
Step 4: Keep top 2 elite fixes
Step 5: Crossover — combine top 2
Step 6: Mutate — improve using Claude AI
Step 7: Repeat for 3 generations
Step 8: Return highest scoring fix
```

---

## 📊 Sample Bugs Detected

| Bug Type | Severity | Description |
|----------|----------|-------------|
| Division by Zero | 🔴 High | Dividing by zero crashes the program |
| File Not Closed | 🟡 Medium | File handle left open after use |
| Infinite Recursion | 🔴 High | No base case in recursive function |
| Index Out of Range | 🔴 High | Accessing invalid list index |
| Type Error (str + int) | 🔴 High | Mixing incompatible data types |
| Missing Return Statement | 🟡 Medium | Function returns None unintentionally |

---

## 📦 Requirements

```
streamlit
anthropic
fpdf2
```

---

## 👨‍💻 Author

**Nikhileswar Gouda**
Built as part of internship project using **Claude AI + Genetic Algorithms**
GitHub: [@Nikhileswar-Gouda](https://github.com/Nikhileswar-Gouda)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

⭐ Star this repo if you found it helpful!
