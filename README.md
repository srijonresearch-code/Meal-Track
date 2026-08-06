# 🍱 MealTrack

A shared house meal cost splitter built with Python and Streamlit.

## The Problem

When you live with others, someone buys groceries and everyone eats. At the end of the month it's a headache figuring out who spent how much, how many meals each person had, and who owes who what. MealTrack handles all of that automatically.

## Features

- 📦 Track grocery purchases per member
- 🍽️ Log daily meals per person (up to 3 per day)
- 📊 Auto-calculates meal rate and who needs to pay or get paid
- 🗓️ Month-wise records — data is saved separately for each month
- 👤 Admin-protected member management
- 🗑️ Delete individual entries from bazar or meal logs

## How It Works

**Meal Rate** = Total Bazar Amount ÷ Total Meals

**Due Amount** = What a member spent on bazar − (Meal Rate × Their meals)
→ Positive means they're owed money back

**Pay Amount** = (Meal Rate × Their meals) − What they spent on bazar
→ Positive means they owe money

## Tech Stack

- **Python**
- **Streamlit** — UI and forms
- **Pandas** — data handling and calculations
- **CSV** — local file storage

## Project Structure

```
mealtrack/
│
├── app.py               # Main application
├── members.csv          # Member list
├── bazarJanuary2026.csv # Monthly bazar logs (auto-created)
├── mealJanuary2026.csv  # Monthly meal logs (auto-created)
└── ...
```

## Running Locally

```bash
pip install streamlit pandas
streamlit run app.py
```

## What I Learned

This was a self-directed project — no tutorials, just building. Key things I leveled up on:

- `df.loc` vs chained indexing and avoiding `SettingWithCopyWarning`
- Streamlit forms, `st.rerun()`, and multi-column layouts
- Per-row delete logic with pandas
- CSV read/write and handling `FileNotFoundError` gracefully

---

Built by [Srijon](https://github.com/your-username) · 2026
