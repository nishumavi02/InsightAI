# InsightAI — AI-Powered Business Decision Intelligence Platform

**InsightAI** is an intelligent decision intelligence platform designed to help business leaders (CEOs, Sales, Operations) query structured business data, internal company documents, and historical trends using natural language.

Instead of requiring users to manually run SQL queries, search policy documents, and build spreadsheet forecasts, InsightAI unifies these workflows into a single interactive Streamlit dashboard powered by a hybrid multi-agent AI architecture.

---

## 🏗️ System Architecture

```
                       USER / DASHBOARD (Streamlit)
                                    │
                                    ▼
                      DECISION ROUTER (Rule-Based Intent)
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
     SQL AGENT                  RAG AGENT                   ML AGENT
 (Structured Data)        (Unstructured Docs)          (Predictive Analytics)
         │                          │                          │
   SQLite Database         Document Embeddings            Revenue Model
         │                          │                          │
         └──────────────────────────┼──────────────────────────┘
                                    ▼
                        BUSINESS-FRIENDLY RESPONSE
                                    │
                                    ▼
                      CONVERSATION MEMORY (SQLite)
```
---

## ✨ Core Features & Implementation Progress

### 1. 🔍 SQL Agent (Structured Analytics)
* **Text-to-SQL Pipeline:** Converts natural language questions into database queries automatically.
* **Schema Inspection & Validation:** Dynamically inspects table schemas and restricts query execution strictly to read-only statements (`SELECT`, `WITH`). Destructive commands (`DROP`, `DELETE`, `UPDATE`, `INSERT`) are automatically blocked.
* **Self-Healing Execution:** Performs an automated one-time query regeneration if the initially generated SQL fails.
* **Business Insights:** Translates execution results into plain-language executive summaries.

### 2. 📄 RAG Agent (Unstructured Document Intelligence)
* **Vector Search:** Chunks and embeds internal documents using **Sentence Transformers (`all-MiniLM-L6-v2`)**.
* **Grounded Answer Generation:** Employs cosine similarity thresholds to reject low-confidence retrievals, preventing AI hallucinations when information is missing.

### 3. 📈 ML Forecasting Agent (Predictive Analytics)
* **Revenue Trend Prediction:** Aggregates order data monthly to forecast future revenue trends using a Linear Regression baseline model.
* **Evaluation Metrics:** Evaluates predictions using MAE, RMSE, and $R^2$ metrics to measure model performance.

### 4. 🧠 Decision Router & Memory
* **Query Dispatcher:** Evaluates user input and routes requests to the SQL, RAG, or ML agent.
* **Persistent Chat History:** Logs user questions, answers, and timestamps into a `conversation_history` table in SQLite across application restarts.

### 5. 📊 Interactive Dashboard
* Built with **Streamlit** and **Plotly** to feature real-time KPI cards, interactive chart visualizations, AI executive summaries, and a conversational chat interface.

---

## 🛠️ Tech Stack

* **Frontend & Dashboards:** Streamlit, Plotly
* **Core Language:** Python
* **Database:** SQLite
* **Data Engineering & Processing:** Pandas, NumPy
* **Machine Learning & NLP:** Scikit-learn, Sentence Transformers (`all-MiniLM-L6-v2`)
* **Version Control:** Git, GitHub

---

## 🗄️ Database Schema & Scope

The application runs on an SQLite database (`insightai.db`) containing:
* **`customers`:** ~500 records (demographics, customer details, location)
* **`products`:** ~50 records (product categories, unit pricing, inventory levels)
* **`orders`:** ~5,000 order transactions spanning 12 months
* **`conversation_history`:** Chat logs and query records

---

## 🛡️ Safety & Reliability Features

* **Query Protection:** Blocks destructive database operations before execution.
* **Retrieval Guardrails:** Rejects ungrounded document queries via confidence thresholding.
* **Controlled Routing:** Uses predictable rule-based dispatching for key query types.

---

## 🚀 Future Roadmap

- [ ] Autonomous LLM-based intent router replacing keyword routing.
- [ ] Advanced time-series forecasting algorithms (e.g., ARIMA / Prophet).
- [ ] Dedicated Vector DB integration (FAISS / Pinecone) for large document scale.
- [ ] PostgreSQL migration for production-grade concurrency.
- [ ] FastAPI backend separation and Cloud deployment via Docker.
