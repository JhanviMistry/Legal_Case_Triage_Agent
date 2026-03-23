# 🧠 Agentic Case Triage AI

An **agentic, explainable legal case triage system** designed for legal advice centres (e.g. Queen Mary Legal Advice Centre). The system automatically validates, classifies, routes, and explains legal enquiries while maintaining **auditability, transparency, and legal-team readiness**.

<img width="1460" height="752" alt="image" src="https://github.com/user-attachments/assets/abbb0265-0019-4c4d-bbd3-7a5150ebb4c8" />

<img width="1414" height="771" alt="image" src="https://github.com/user-attachments/assets/0023d5c4-838b-4ed9-b27f-292c86d1cb22" />



---

## 🚀 Project Overview

This project implements a **multi-agent architecture** that processes incoming legal enquiries and determines:

* Whether the case is **eligible** for triage
* Which **legal domain** it belongs to (e.g. Employment, Housing)
* Where it should be **routed**
* How confident the system is in its decision
* A **human-readable explanation** suitable for clients and legal staff

The system is built with:

* **FastAPI** (backend)
* **React + Vite** (frontend)
* Modular **Agent pattern** for transparency and extensibility

---

## 🧩 Architecture

### Agentic Pipeline

```
User Message
   ↓
PlannerAgent
   ↓
ValidatorAgent
   ↓
ReasonerAgent
   ↓
RouterAgent
   ↓
ExplainerAgent
   ↓
MemoryAgent
   ↓
Final API Response
```

Each agent:

* Has a **single responsibility**
* Mutates a shared `state` object
* Appends explainable steps for audit purposes

---

## 🗂️ Project Structure

```
Case_Triage_Agent/
│
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── triage_engine.py        # Orchestrates agents
│   ├── agents/
│   │   ├── planner.py
│   │   ├── validator.py
│   │   ├── reasoner.py
│   │   ├── router.py
│   │   ├── explainer.py
│   │   └── memory.py
│   └── models.py               # Pydantic schemas
│
├── frontend/
│   ├── index.html
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── services/api.js
│   └── package.json
│
└── README.md
```

---

## ⚙️ Backend Setup (FastAPI)

### 1️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate
```

### 2️⃣ Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

### 3️⃣ Run the backend

From project root:

```bash
uvicorn backend.main:app --reload
```

Backend will run at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

Swagger docs:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🎯 API Usage

### POST `/triage`

#### Request

```json
{
  "message": "I live in London and my employer has not paid my wages"
}
```

#### Response

```json
{
  "case_id": "048407da-5953-4b85-9a23-cf4dfb3ea31b",
  "status": "ACCEPTED",
  "domain": "EMPLOYMENT",
  "route": "Employment Legal Advice",
  "confidence": 0.95,
  "explanation": "The case falls within England and Wales jurisdiction...",
  "steps": [
    "A legal advisor can now review your case",
    "Prepare relevant documents"
  ]
}
```

---

## 🎨 Frontend Setup (React + Vite)

### 1️⃣ Navigate to frontend

```bash
cd frontend
```

### 2️⃣ Install dependencies

```bash
npm install
```

### 3️⃣ Start frontend

```bash
npm run dev
```

Frontend runs at:
👉 [http://localhost:5173](http://localhost:5173)

---

## 🔍 Explainability & Audit Readiness

This system is **designed for legal compliance**:

* Domain and confidence are **explicitly exposed** (not hidden)
* Every decision step is logged in `state['steps']`
* Explanations are client-safe and legally neutral
* MemoryAgent supports future audit & improvement

✔ Suitable for legal clinics
✔ GDPR-conscious architecture
✔ Human-in-the-loop friendly

---

## 🧪 Feature Flags

Enable LLM-based reasoning (optional):

```bash
export USE_LLM_REASONER=true
```

(Default: rule-based reasoning)

---

## 🛣️ Roadmap

* [ ] Frontend redesign (client-friendly UI)
* [ ] Role-based views (client vs legal team)
* [ ] Persistent storage (PostgreSQL)
* [ ] Full audit log export
* [ ] Multilingual support

---

## 👩‍⚖️ Intended Use Disclaimer

This system **does not provide legal advice**. It performs triage only and is designed to assist legal professionals by:

* Filtering ineligible cases
* Reducing admin workload
* Improving response consistency

---

## 👤 Author

**Jhanvi Mistry**
MSc Computer Science

---

If you are a legal professional or developer reviewing this project and would like architectural or compliance details, please get in touch.
