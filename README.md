Sure thing — here’s the ready-to-copy README.md in Markdown format:

# Coding Challenge – Message Topics API

## Goal  
Build a small FastAPI service that can analyze hotel guest conversations and extract topics. The challenge focuses on implementing three missing endpoints.

---

## Tasks  
In `app/main.py` you’ll find four endpoints. Only the health check is implemented.  
Please complete the others:

1. **`GET /conversations`** – return all conversations.  
2. **`GET /analytics/topic/{topic}`** – return all conversations about a given topic, plus a simple topic response (e.g. summary or keywords).  
3. **`GET /analytics/hot-topics?number_of_topics=N`** – return the *N hottest topics* with their related conversations.  

Models exist in `app/models.py`. Extend them if needed. You may use any libraries or techniques (AI allowed but not required).  

⏱ Estimated time: ~2 hours. The solution doesn’t have to be perfect—we’ll review and refine it together in the interview.

---

## Setup  
The project uses [uv](https://github.com/astral-sh/uv). Commands are in the `Makefile`.

Run locally (with reloading):  
```bash
make run
```

Run with Docker (no reloading):
```bash
make run-docker
```

Run tests:
```bash
make test
```

Lint & format:
```bash
make lint
make fmt
```

API playground should be available at `http://localhost:8000/docs` after starting the server.

⸻

Notes
- Example conversations are in data/. Feel free to extend or generate new ones.
-  us on clean, working code.
- We’ll use your solution as the basis for discussion, code review, and pair programming in the interview.
