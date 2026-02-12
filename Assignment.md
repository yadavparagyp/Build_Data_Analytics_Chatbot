# Assignment: Build a Data Analytics Chatbot

## Objective

Build an intelligent Agentic chatbot that can answer analytical questions from the provided aggregated data of a hair care product company's registration-to-order funnel.

## Context

You are provided with 30 days of aggregated data (`data/d0_dplus_daily_summary/d0_dplus_daily_summary.json`) that tracks the customer journey from form registration to order placement. The data includes various dimensions like city, platform, UTM parameters, gender, age bucket, and hair loss stage.

### Data Schema

Refer to `schemas/d0_dplus_daily_summary.schema` for the complete schema. Key columns include:

**Dimensions:**
- `date` - The reporting date
- `gender` - Male/Female
- `platform` - web/app
- `city` - Indian cities (Mumbai, Delhi, Bangalore, etc.)
- `stage` - Hair loss stage (Stage 1-5, Unknown)
- `age_bucket` - Age groups (18-25, 26-35, 36-45, 46-55, 55+)
- `first_form_utm_medium`, `first_form_utm_campaign`, `first_form_utm_source` - UTM parameters at form submission
- `order_utm_medium`, `order_utm_campaign`, `order_utm_source` - UTM parameters at order placement

**Metrics:**
- `total_form_start` - Total people who initiated form fillup
- `d0_form_start` - People who signed up and initiated form on the same day
- `total_form_filled` - Total people who completed the form
- `d0_form_filled` - People who completed form on signup day
- `dplus_form_filled` - People who completed form but signed up before
- `d0_orders` - Orders placed on the same day as signup
- `dplus_orders` - Orders from people who signed up earlier
- `d1_orders`, `d7_orders`, `d15_orders`, `d21_orders`, `d30_orders`, `d30plus_orders` - Orders by signup lag
- `NF_orders` - No-form orders (direct purchases without form)
- `d0_revenue` - Revenue from D0 orders (in INR)

### Key Business Metrics to Understand

1. **D0 Conversion Rate** = `Total D0 Orders / Total D0 Form Filled` (People who ordered on the same day they filled the form)
2. **Dplus Conversion Rate** = `Total Dplus Orders / Total Dplus Form Filled` (People who ordered after the day they filled the form)
3. **Form Completion Rate** = `total_form_filled / total_form_start`

## Requirements

### 1. Core Functionality

The chatbot should:
- Parse **any** natural language analytical question about the data
- Dynamically understand user intent and generate appropriate queries
- Perform aggregations, comparisons, trend analysis, and any other analytical operations supported by the data
- Return clear, formatted answers with relevant numbers
- Handle questions that go beyond the provided examples—the system should generalize, not memorize
- **Maintain conversation context** and answer follow-up questions based on previous interactions (e.g., "What about for Mumbai?" after asking about Delhi's conversion rate)

### 2. Query Handling

**Important**: The chatbot must be capable of answering **any analytical question** that can be derived from the available data, not just the examples listed below. The examples are provided only to illustrate the types of analysis expected. Since you are implementing an Agentic AI with dynamic SQL generation, the system should generalize to handle novel queries that were not explicitly anticipated during development.

The chatbot should be able to answer questions like:

**Revenue Analysis:**
1. What was the daily average revenue for the last week?
2. Is there any noticeable change in the current week's revenue compared to the last two weeks?
3. If revenue change is more than 5%, find out if there was a noticeable difference in any of the utm_source

**Conversion Analysis:**
4. Which stage has the highest D0 conversion rate?
5. Which utm_source drives the most D0 orders?
6. Which city has the highest D0 conversion rate?
7. Which city has the lowest D0 conversion rate in the last 15 days?

**Funnel Analysis:**
8. What is the form completion rate by platform?
9. Which age bucket has the best conversion?
10. How does weekend performance compare to weekdays?

**Trend Analysis:**
11. Is there a week-over-week improvement in D0 orders?
12. Which campaign showed the most growth this week?

### 3. Handling Limitations

The chatbot should gracefully handle:
- Questions that cannot be answered from the available data
- Ambiguous questions (ask for clarification)
- Invalid date ranges
- Missing or null values in the data

### 4. Technical Requirements

- **Agentic AI Architecture**: Implement the chatbot using an Agentic AI approach where the agent can:
  - Reason about the user's question
  - Plan the steps needed to answer the query
  - Execute actions (data retrieval, calculations)
  - Reflect on results and refine if needed

- **Dynamic SQL Generation**: The agent should dynamically generate SQL queries based on natural language input rather than using hardcoded query templates. The system should:
  - Understand the data schema
  - Generate appropriate SQL queries on-the-fly
  - Handle complex aggregations and filters dynamically

- **Open Source LLM Integration**: Use open source cloud-based models for the AI backbone:
  - **Ollama Cloud**: Models like Llama, Mistral, or similar
  - **Hugging Face Inference API**: Models available through Hugging Face's hosted inference endpoints
  - Document which model(s) you chose and why

- Use Python and SQL as the primary languages
- Load and process the JSON data efficiently (consider using SQLite or DuckDB for SQL queries)
- Implement proper error handling
- Structure code in a modular, maintainable way

### 5. Bonus Features (Optional)

- Generate simple visualizations (charts/graphs)
- Export answers to a report format
- Suggest related questions based on the current query

## Deliverables

1. Working chatbot code
2. A simple UI interface for interacting with the chatbot
3. README with setup instructions
4. Sample conversation demonstrating various question types

## Reference Files

- Data: `data/d0_dplus_daily_summary/d0_dplus_daily_summary.json`
- Schema: `schemas/d0_dplus_daily_summary.schema`

## Evaluation Criteria

1. **Accuracy** - Correct answers with proper calculations
2. **Generalization** - Ability to handle **any** analytical query derivable from the data, not just predefined examples
3. **Context Awareness** - Ability to maintain conversation history and correctly interpret follow-up questions
4. **Robustness** - Graceful handling of edge cases, ambiguous queries, and unsupported questions
5. **Code Quality** - Clean, documented, modular code
6. **User Experience** - Clear, well-formatted responses
7. **Agentic Design** - Effective implementation of agentic AI patterns (planning, reasoning, tool use)
8. **SQL Generation** - Quality and correctness of dynamically generated SQL queries for novel questions
9. **LLM Integration** - Proper integration with open source models (Ollama/Hugging Face)
