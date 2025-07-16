
---

## 🧱 `schemaplan.md` – Scenario Dataset Schema Plan

```markdown
# 🧾 Schema Plan – Financial Simulation Scenarios Dataset

## 🎯 Purpose

The dataset powers the simulation module in MoneyMentor, letting users engage with realistic financial decisions.

## 🧱 CSV Schema

| Column Name        | Data Type | Description |
|--------------------|-----------|-------------|
| id                 | Integer   | Unique identifier for each scenario |
| scenario_text      | String    | The situation the user must respond to |
| option_a           | String    | First decision option |
| option_b           | String    | Second decision option |
| correct_option     | String    | "A" or "B" – the better financial decision |
| feedback_correct   | String    | Explanation shown if user picks correctly |
| feedback_incorrect | String    | Guidance shown if user picks wrong |

## 🔄 Sample Entry

```csv
id,scenario_text,option_a,option_b,correct_option,feedback_correct,feedback_incorrect
1,"You get $500 for your birthday.", "Spend it all on clothes", "Save $300 and spend $200", "B", "Good job saving early!", "Spending it all isn't smart!"
