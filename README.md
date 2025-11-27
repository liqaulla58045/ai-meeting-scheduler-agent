# 📅 AI Meeting Scheduler Agent

An AI-inspired **Meeting Scheduler** that understands natural language requests
and automatically creates meeting entries, detects conflicts, supports recurring events,
and shows an interactive calendar view.

Built for **Rooman AI Internship Challenge**.

---

## 🚀 Overview

This agent allows users to type instructions like:

> "Schedule a 30-minute sync with Rahul tomorrow at 3 PM about project status every week until next month"

The system will:

- Parse the natural language request (locally, no external API needed)
- Extract:
  - title
  - date and time
  - duration
  - participants
  - recurrence pattern (daily / weekly / monthly / none)
- Check for **time conflicts** with existing meetings
- Save the meeting into a **local SQLite database**
- Show meetings in:
  - A **list view** (Manage tab)
  - A **calendar-like view by date** (Calendar tab)

There is also a **simulated Google Calendar integration stub** to show how real APIs could be plugged in later.

---

## ✨ Features

### 1. Natural Language Meeting Scheduling

- Write free-text like:
  - “Schedule a standup with team tomorrow at 10 AM for 15 minutes”
  - “Set a weekly meeting with Rahul every Monday at 4 PM about AI project”
- The agent extracts:
  - **Title** (topic / purpose)
  - **Start & end time**
  - **Duration**
  - **Participants** (after “with …”)
  - **Recurrence** (daily / weekly / monthly / none)

### 2. Recurring Meetings

- Supports simple recurrence types:
  - `none` (one-time)
  - `daily`
  - `weekly`
  - `monthly`
- Optional end date using phrases like:
  - “until next month”
- Recurrence info is stored in DB and displayed in UI.

### 3. Conflict Detection

- If a new meeting overlaps with an existing one:
  - The scheduler **rejects** it and shows a clear error:
    > “Time slot conflicts with an existing meeting.”
- Conflict detection also works on **edit** (when changing time).

### 4. Calendar View

- `📅 Calendar View` tab:
  - Groups meetings by date
  - Lets the user pick a day and see all meetings for that date
  - Shows title, time, participants, and recurrence

### 5. Manage Meetings (Edit / Delete / Export)

- `📋 Manage Meetings` tab:
  - List of all meetings (with recurrence info)
  - **Edit**:
    - Update title / participants
    - Time conflict checks are applied
  - **Delete**:
    - Remove a meeting safely
  - **Export**:
    - Export all meetings to **CSV**
    - Simple text export for PDF-like usage (download as `.txt`)

### 6. Modern Streamlit UI

- Futuristic styling:
  - Animated Lottie loader
  - Gradient light theme
  - Custom CSS for buttons & cards
- Tabs:
  - **Schedule Meeting**
  - **Calendar View**
  - **Manage Meetings**
- Visual feedback:
  - Success / error messages
  - Balloons + emoji rain on successful recurring scheduling

### 7. Simulated Google Calendar Integration

- A stub function `create_google_calendar_event(...)`:
  - Returns a **fake event ID & link**
  - No real API calls (safe for demo without credentials)
- This shows how one could integrate:
  - Google Calendar
  - Outlook Calendar
  - etc.

---

## ⚠️ Limitations

- **No live LLM API:**  
  To keep deployment free and quota-safe, the current version uses a **rule-based local parser** (regex + heuristics) instead of calling an external OpenAI / LLM API.  
  - It works well for typical phrases, but:
    - Very complex or ambiguous sentences may not be perfectly parsed.

- **Simple Date/Time Parsing:**
  - Supports common words like `today`, `tomorrow`, and explicit times like `3 PM`, `11:30 am`, `16:00`.
  - Very natural vague phrases like “later in the evening” are not fully handled.

- **Recurrence is metadata only:**
  - Recurring meetings are stored with recurrence info and shown in UI.
  - Individual repeated instances are not yet expanded into separate rows for each week/day.

- **Single-user, local DB:**
  - Uses a single SQLite database (`meetings.db`).
  - No authentication / multi-tenant separation yet.

- **Google Calendar is simulated:**
  - No real Google API keys or OAuth setup.
  - The stub only returns a fake URL for demonstration.

---

## 🧱 Tech Stack

- **Language:** Python 3
- **Frontend/UI:** Streamlit
- **NLP Parsing:** Local rule-based parsing (`regex` + `dateutil`)  
  (Designed so it can later be swapped with OpenAI / any LLM)
- **Database:** SQLite via SQLAlchemy
- **Time Zone:** Asia/Kolkata (IST)
- **Extras:**
  - `streamlit-extras` (UI enhancements & animations)
  - `streamlit-lottie` for Lottie animations
  - `pandas` for table export / calendar view

---

## 🛠 Setup & Run Instructions (Local)

### 1. Clone the Repository

```bash
git clone <your-repo-url>.git
cd ai-meeting-scheduler-agent
