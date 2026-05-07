# 🛠️ IndieStack DevOps
**A production-ready backend for indie games.**

This project provides a "one-click" infrastructure for developers to handle player data, persistence, and scaling without needing to be a server expert.

## Tech Stack
- **Engine:** Docker & Docker Compose
- **Backend:** Python (Flask)
- **Database:** PostgreSQL
- **Caching:** Redis (Coming Soon)

## How to use
1. Install Docker.
2. Run `docker compose up --build`.
3. Your game can now POST to `http://localhost:5000/update_stats`.