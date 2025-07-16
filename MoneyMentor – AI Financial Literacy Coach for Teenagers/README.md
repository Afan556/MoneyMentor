# 💸 MoneyMentor – AI Financial Literacy Coach for Teens

MoneyMentor is a Streamlit-based educational app designed to help teenagers understand financial literacy through interactive chat and decision-based simulation games. It combines Gen Z-friendly AI conversations with realistic financial scenarios to make learning about money fun, relatable, and practical.

## 🚀 Features

- 💬 **Chat with AI Mentor**: Ask anything about saving, investing, budgeting – all answered in Gen Z slang using LLM + Gen Z translator.
- 🎮 **Financial Simulation Game**: Choose between two options in real-world financial situations and receive feedback with explanations.
- 📊 **Score Tracking**: Earn points for every correct decision in the simulation.
- 🧠 **Contextual Responses**: Powered by LangChain and Google Generative AI for personalized, helpful responses.

## 📦 Project Structure

```bash
📁 moneymentor/
│
├── main.py                    # Streamlit frontend
├── chatbot.py                 # LangChain + Gemini Gen Z response logic
├── simulator.py               # Simulation scenario logic & scoring
│
├── data/
│   └── sim_scenarios_fixed.csv  # Scenario data for simulation
│
├── schemaplan.md              # Dataset schema & design explanation
├── datacleaningnotes.md       # Notes on how the data was cleaned
└── README.md                  # You’re reading this
