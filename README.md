
# 📊 Agentic Analytics Chatbot

### Dynamic SQL + DuckDB + Ollama (Open-Source LLM)

---

## 🧩 Problem Statement

A hair care product company tracks its customer journey from:

> Registration → Form Completion → Order Placement

The company provided 30 days of aggregated funnel data containing:

* User demographics (gender, age bucket)
* Acquisition channels (UTM source, campaign, medium)
* Platform (web/app)
* Geography (city)
* Hair loss stage
* Order lag buckets (D0, D1, D7, D15, D30+)
* Revenue data

The goal was to build an **intelligent agentic chatbot** that can:

* Answer any analytical question about the dataset
* Dynamically generate SQL
* Maintain conversation context
* Handle follow-up questions
* Gracefully handle errors
* Use open-source LLMs (Ollama)

---

## 🎯 Objective

Build an **Agentic AI-powered analytics chatbot** that:

* Understands natural language analytical questions
* Generates SQL dynamically (not template-based)
* Executes queries safely
* Performs aggregations & comparisons
* Computes business metrics (conversion rates)
* Maintains conversational memory
* Handles invalid queries robustly

---

## 🏗 System Architecture

```
User Question
      ↓
Ollama LLM (Reasoning + SQL Generation)
      ↓
SQL Guard (SELECT-only enforcement)
      ↓
DuckDB Execution Engine
      ↓
Error Handling + Auto-Refinement
      ↓
Result Formatting
      ↓
Streamlit Chat UI
```

---

## 🧠 Agentic Design Pattern

The system follows a structured agent loop:

### 1️⃣ Reason

The LLM:

* Understands user intent
* Creates an analysis plan
* Generates SQL
* Specifies how to interpret results

### 2️⃣ Act

The generated SQL is executed in DuckDB.

### 3️⃣ Reflect

If execution fails:

* The error message is passed back to the LLM
* The SQL is refined automatically
* Retry occurs (up to 3 attempts)

### 4️⃣ Respond

Results are:

* Formatted
* Interpreted
* Displayed clearly

---

## 🧮 Key Business Metrics Implemented

### D0 Conversion Rate

```
SUM(d0_orders) / SUM(d0_form_filled)
```

### Dplus Conversion Rate

```
SUM(dplus_orders) / SUM(dplus_form_filled)
```

### Form Completion Rate

```
SUM(total_form_filled) / SUM(total_form_start)
```

All divisions use `NULLIF` to prevent divide-by-zero errors.

---

## 🧠 Context Awareness

The chatbot maintains lightweight conversational memory:

* Stores resolved top entities (e.g., top city)
* Handles follow-ups like:

  > “What about platform-wise for that top city?”

The system rewrites such questions internally before SQL generation.

---

## 🔄 Dynamic SQL Generation

The chatbot:

* Does NOT use predefined query templates
* Generates SQL on-the-fly
* Handles:

  * Grouping
  * Aggregation
  * Date filtering
  * Interval logic
  * Ranking
  * Comparisons
  * Trend analysis

Example:

> “Which city has the highest D0 conversion rate in the last 15 days?”

Generates dynamic SQL using:

* MAX(date_parsed)
* INTERVAL '15 days'
* ORDER BY conversion DESC
* LIMIT 1

---

## ⚙️ Technology Stack

| Component    | Technology           |
| ------------ | -------------------- |
| LLM          | Ollama (llama3.2:3b) |
| Query Engine | DuckDB               |
| UI           | Streamlit            |
| Data Format  | JSON                 |
| Language     | Python               |

---

## 🤖 Why Ollama?

* Fully open-source
* Runs locally
* No external API dependency
* Strong reasoning for SQL generation
* Fast inference with llama3.2:3b

Model Used:

```
llama3.2:3b
```

Chosen for:

* Low latency
* Reliable structured output
* Balanced reasoning capability

---

## 📂 Project Structure

```
Assignment-Analytics-Agent/
│
├── app.py
├── cli_chat.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── data/
│   └── d0_dplus_daily_summary.json
│
├── schemas/
│   └── d0_dplus_daily_summary.schema
│
└── src/
    ├── agent.py
    ├── config.py
    ├── data_loader.py
    ├── formatting.py
    ├── llm_ollama.py
    ├── prompts.py
    ├── sql_guard.py
```

---

## 🔐 Robustness & Safety

* SELECT-only SQL enforcement
* Automatic SQL retry mechanism
* Error reflection loop
* Prevents unsafe operations
* Handles ambiguous questions
* Protects against divide-by-zero
* Structured JSON contract with LLM

---

## 📊 Supported Analytical Queries

### Revenue

* Daily average revenue
* Week-over-week revenue change
* Revenue trend comparison

### Conversion

* Best performing city
* Stage-wise performance
* UTM source comparison
* Platform comparison

### Funnel

* Form completion rate
* Conversion lag analysis
* No-form orders

### Time Analysis

* Last N days
* Weekly aggregation
* Trend comparison

---

## 🧪 Example Questions

```
Which city has the highest D0 conversion rate in the last 15 days?

What about platform-wise for that top city?

Is there week-over-week improvement in D0 orders?

Which stage performs best for Dplus conversion?
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install Ollama

```bash
ollama pull llama3.2:3b
```

### 4️⃣ Run Application

```bash
python -m streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

## 📈 Evaluation Criteria Covered

| Requirement                 | Status |
| --------------------------- | ------ |
| Accuracy                    | ✅      |
| Dynamic SQL generation      | ✅      |
| Agentic reasoning loop      | ✅      |
| Context awareness           | ✅      |
| Robust error handling       | ✅      |
| Open-source LLM integration | ✅      |
| Clean modular code          | ✅      |
| Scalable architecture       | ✅      |

---

## 🚀 Extensibility

The system can be extended to:

* Add visualization layer
* Support additional datasets
* Integrate vector-based document retrieval
* Deploy via containerization
* Add authentication & role-based controls

---

## 🏁 Conclusion

This project demonstrates an end-to-end implementation of an **Agentic AI analytics system** that translates natural language into executable SQL, reasons over structured business data, maintains conversational context, and performs dynamic analysis — entirely using open-source tools.

It is designed to be:

* Modular
* Explainable
* Scalable
* Production-ready in architecture
