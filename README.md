# 📅 AI Meeting Scheduler Agent

An AI-powered Meeting Scheduler that understands natural language requests and automatically creates meeting entries, detects conflicts, and stores schedules.

Built for **Rooman AI Internship Challenge**.

---

## 🚀 Overview

This agent allows users to type instructions like:

> **"Schedule a 30-minute sync with Rahul tomorrow at 3 PM about project status"**

The system will automatically:
- Extract **meeting details** such as date, time, participants, duration, and title
- **Check for conflicts** and avoid overlapping schedules
- **Store meetings** in a persistent **SQLite database**
- Provide a **simple and clean dashboard** to view all scheduled meetings

This project works **fully offline** using a **rule-based NLP engine**, meaning:
- No OpenAI API required
- No running costs
- Works without internet (after initial installation)

---

## ✨ Features

- 🧠 **Offline Natural Language Processing** (regex + rule-based extraction)
- 🕒 Extracts:
  - Meeting Title / Agenda
  - Start & End Time
  - Duration (minutes / hour format)
  - Participants (names or emails)
- 🔁 **Conflict detection** to prevent double booking
- 📋 **Meeting history dashboard**
- 💾 Persistent storage using **SQLite**
- 🖥 **Streamlit UI** with clean UX
- 🔌 Modular structure for future extensions

---

## ⚙️ Limitations

| Item | Current Status |
|-------|-----------------------|
| Language flexibility | Works best with structured meeting text |
| Multi-user support | Single-user system |
| Calendar API | Stub provided but not fully integrated |
| Notifications | Not included yet |

---

## 🧱 Tech Stack

| Component | Technology |
|-----------|------------|
| UI Framework | Streamlit |
| Backend | Python 3 |
| NLP Engine | Offline regex parser |
| Database | SQLite + SQLAlchemy |
| Timezone | Asia/Kolkata |
| Deployment | Streamlit Cloud |

---

## 🛠 Setup & Run Instructions (Local)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd meeting-scheduler-agent
