# Assignment: Build a Data Analytics Chatbot

## Objective

Build an intelligent chatbot that can answer analytical questions from the provided aggregated data of a hair care product company's registration-to-order funnel.

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
- Parse natural language questions
- Perform aggregations, comparisons, and trend analysis
- Return clear, formatted answers with relevant numbers

### 2. Example Questions to Support

The chatbot should be able to answer questions like (but not limited to):

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

- Use Python and SQL as the primary languages
- Load and process the JSON data efficiently
- Implement proper error handling
- Structure code in a modular, maintainable way

### 5. Bonus Features (Optional)

- Support follow-up questions with context
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
2. **Coverage** - Ability to handle diverse question types
3. **Robustness** - Graceful handling of edge cases
4. **Code Quality** - Clean, documented, modular code
5. **User Experience** - Clear, well-formatted responses
