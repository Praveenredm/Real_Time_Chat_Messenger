# Real-Time Chat Application

A modern, real-time chat application built with **FastAPI** (Backend) and **Vanilla JavaScript** (Frontend).
It supports user authentication (JWT), real-time messaging (WebSocket), and data persistence (SQLite).

## Features
-   **Authentication**: Secure Login and Signup using JWT (JSON Web Tokens).
-   **Real-time Messaging**: Instant message delivery using WebSockets.
-   **Multi-User Chat**: Chat with other users in real-time.
-   **User Identification**: Messages displaying the sender's username.
-   **Optimistic UI**: Immediate feedback when sending messages.
-   **Responsive Design**: Clean and modern UI using CSS Flexbox.

## Tech Stack
-   **Backend**: Python, FastAPI, SQLAlchemy, SQLite, PyJWT, Passlib.
-   **Frontend**: HTML5, CSS3, JavaScript (Fetch API, WebSocket).
-   **Database**: SQLite (Zero configuration required).

## Project Structure
```
.
├── backend/
│   ├── app/
│   │   ├── models/       # Database models (User)
│   │   ├── routers/      # API routes (Auth, Chat)
│   │   ├── core/         # Security configs
│   │   ├── websocket/    # Connection manager
│   │   ├── db.py         # Database connection
│   │   └── main.py       # App entry point
│   ├── create_tables.py  # Script to initialize DB
│   └── requirements.txt  # Python dependencies
│
└── chat-frontend/
    ├── index.html        # Main UI
    ├── style.css         # Styling
    └── app.js            # Frontend Logic
```

## Setup Instructions

### Prerequisites
-   Python 3.8+ installed.

### 1. Backend Setup
Navigate to the `backend` folder:
```bash
cd backend
```

Install dependencies:
```bash
pip install fastapi uvicorn sqlalchemy python-dotenv pyjwt passlib[bcrypt]
```

Initialize the database (creates `chat.db` file):
```bash
python create_tables.py
```

Start the server:
```bash
uvicorn app.main:app --reload
```
*The server will start at `http://127.0.0.1:8000`.*

### 2. Frontend Setup
Simply open the `chat-frontend/index.html` file in your web browser.

**Optional (Recommended)**:
To avoid any potential CORS issues, you can run a simple HTTP server:
```bash
cd chat-frontend
python -m http.server 8080
```
Then open `http://localhost:8080` in your browser.

## Usage Guide

1.  **Register**: Open the app and sign up with a username, email, and password.
2.  **Login**: Log in with your credentials.
3.  **Chat**: start sending messages!
4.  **Test with Multiple Users**:
    -   Open the app in your main browser (User 1).
    -   Open the app in an **Incognito Window** (User 2).
    -   Log in as different users in each window.
    -   Chat and see messages appear instantly!

## Troubleshooting

-   **CORS Error**: If you see a CORS error in the console, verify the backend is running. If opening the HTML file directly doesn't work, try the `python -m http.server` method mentioned above.
-   **Database Error**: If you see "no such table", make sure you ran `python create_tables.py`.
-   **Duplicate Messages**: If you see double messages, refresh the page. The app logic handles self-message deduplication.
