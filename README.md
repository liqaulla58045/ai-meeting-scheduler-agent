<<<<<<< HEAD
# 📅 AI Meeting Scheduler Agent

An AI-powered Meeting Scheduler that understands natural language requests
and automatically creates meeting entries, detects conflicts, and stores schedules.

Built for **Rooman AI Internship Challenge**.

---

## 🚀 Overview

This agent allows users to type instructions like:

> "Schedule a 30-minute sync with Rahul tomorrow at 3 PM about project status"

The system will:
- Use AI (OpenAI) to extract date, time, participants, duration, and title
- Check for conflicts with already scheduled meetings
- Save the meeting in a local database (SQLite)
- (Optionally) simulate integration with Google Calendar

---

## ✨ Features

- ✅ Natural Language Understanding (NLP) using OpenAI
- ✅ Automatic extraction of meeting:
  - Title
  - Start/End time
  - Duration
  - Participants
- ✅ Conflict detection (no overlapping meetings)
- ✅ Meeting history & list view
- ✅ Simple, clean Streamlit UI
- ✅ Ready for extension to Google Calendar API

---

## ⚠️ Limitations

- Requires an **OpenAI API key** for NLP parsing.
- Currently uses a **local SQLite DB** (not multi-user distributed).
- Google Calendar integration is simulated (stub) and can be implemented fully later.
- Does not include authentication / multi-account support yet.

---

## 🧱 Tech Stack

- **Frontend/UI:** Streamlit
- **Language:** Python 3
- **AI/NLP:** OpenAI API (`gpt-4.1-mini`)
- **Database:** SQLite using SQLAlchemy
- **Time zone:** Asia/Kolkata (IST)
- **(Optional) External API:** Google Calendar (stub present)

---

## 🛠 Setup & Run Instructions (Local)

### 1. Clone the Repository

```bash
git clone <your-repo-url>.git
cd meeting-scheduler-agent
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set OpenAI API Key

Create a `.env` file or export in terminal:

```bash
export OPENAI_API_KEY="your_api_key_here"
# On Windows (PowerShell):
# $env:OPENAI_API_KEY="your_api_key_here"
```

### 5. Run the App

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

---

## 🌐 Deploying Demo (Streamlit Cloud)

1. Push this project to a **public GitHub repo**.
2. Go to **Streamlit Cloud**, create a new app.
3. Select your repo & `app.py` as the entrypoint.
4. In Streamlit Cloud, go to:
   - **Settings → Secrets**
   - Add: `OPENAI_API_KEY = "your_api_key_here"`
5. Deploy – use the generated URL as your **Working Demo Link**.

---

## 🔭 Potential Improvements

- Full **Google Calendar integration** (create & sync events)
- User **authentication** (multiple users with isolated calendars)
- Voice input (speech-to-text) for meeting requests
- Email notifications to participants
- Integration with MS Outlook / Teams
- Add **priority tags** (High / Medium / Low)
- Analytics: how many meetings per week, free-time suggestion, etc.

---

## 🧩 Architecture Summary

1. **UI Layer (Streamlit)**  
   - Collects natural language meeting requests  
   - Displays proposed meeting details  
   - Shows all scheduled meetings

2. **AI/NLP Layer (OpenAI)**  
   - Converts text → structured JSON (title, start, duration, participants)

3. **Scheduler Logic**  
   - Detects time conflicts  
   - Stores meeting if no conflict

4. **Database (SQLite)**  
   - Persists meetings  
   - Enables listing & querying

5. **External Integration (Future)**  
   - Google Calendar or Outlook can be added through the `calendar_integration.py` module

---

## 🎥 2–3 Minute Demo Script (Suggested)

1. **Intro (20–30 sec)**  
   - Who you are  
   - Which agent you chose: *AI Meeting Scheduler Agent*

2. **Problem (20–30 sec)**  
   - Manual meeting scheduling is slow; conflicts, back-and-forth, etc.

3. **Live Demo (1–1.5 min)**  
   - Type: `"Schedule a 30-minute sync with Rahul tomorrow at 3 PM about project status"`  
   - Show AI extracting details  
   - Confirm & show it added to the list  
   - Try another meeting at same time and show **conflict handling**

4. **Architecture (30–40 sec)**  
   - Briefly show the diagram (UI → AI/NLP → Scheduler → DB → (Optional) Calendar)

5. **Closing (10–20 sec)**  
   - Mention extensibility: Google Calendar, email, multi-user, etc.  
   - Say you’d love to continue this in the internship.
=======
# ai-meeting-scheduler-agent
>>>>>>> e207ea40e83945ceae334f0bf23c76e190f308df
