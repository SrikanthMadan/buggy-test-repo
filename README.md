# Autonomous CI/CD Healing Agent — RIFT 2026 Hackathon

> **AIML DevOps Automation | Agentic Systems Track**
> Team: **Byte-Force** | Leader: **Raunit Raj**

---

## Live Deployment

<!-- FIX: Replaced placeholder deployment URLs with localhost development URLs to prevent attacker-controlled domain registration and phishing. Replace these with your actual verified deployment URLs before public submission. -->
| Service | URL |
|---|---|
| React Dashboard | `http://localhost:5173` *(replace with your verified Vercel URL before submission)* |
| Backend API (FastAPI) | `http://localhost:8000` *(replace with your verified Railway URL before submission)* |

> ⚠️ **Before public submission:** Replace the above URLs with your actual, verified deployment URLs. Never leave placeholder URLs in a public repository.

---

## LinkedIn Demo Video

<!-- FIX: Replaced placeholder LinkedIn URL with a clearly marked placeholder warning to prevent link hijacking or unintended content. -->
> [Watch the Demo on LinkedIn](https://www.linkedin.com/posts/REPLACE_WITH_ACTUAL_POST_LINK)
> ⚠️ Replace `REPLACE_WITH_ACTUAL_POST_LINK` with your real LinkedIn post URL before submission.
> Must be 2-3 min, public, and tagged with #RIFT2026

---

## Project Title

**Autonomous CI/CD Healing Agent with React Dashboard**

An end-to-end autonomous agent that takes a GitHub repository URL, clones it, discovers all test files, detects bugs (LINTING, SYNTAX, LOGIC, TYPE_ERROR, IMPORT, INDENTATION), auto-fixes them using an AI multi-agent system, commits fixes with `[AI-AGENT]` prefix to a new branch, monitors the CI/CD pipeline, and iterates until all tests pass — all visualized in a production-ready React dashboard.

---

## Architecture Diagram

```
+------------------+       +-------------------+       +-------------------+
|  React Dashboard | ----> |  FastAPI Backend   | ----> |  Orchestrator     |
|  (Vite + React)  | <---- |  /api/run-agent    | <---- |  Agent (LangGraph)|
+------------------+       +-------------------+       +-------------------+
                                                               |
                          +------------------------------------+
                          |                |
               +----------v---+    +-------v-----------+
               | Bug Detector  |    | Fix Generator     |
               | Agent         |    | Agent (GPT/Gemini)|
               +----------+---+    +-------+-----------+
                          |                |
               +----------v----------------v-----------+
               |         Git Agent                      |
               |  (creates branch, commits, pushes)     |
               +------------------------------------------+
                          |
               +----------v-----------+
               |   CI/CD Monitor       |
               |   Agent (GitHub API)  |
               +-----------------------+
```

**Flow:**
1. User submits GitHub repo URL + Team Name + Leader via React dashboard
2. FastAPI backend triggers the Orchestrator agent
3. Bug Detector agent clones repo, runs `flake8` + `pytest`, collects all failures
4. Fix Generator agent creates targeted fixes for each bug
5. Git Agent creates branch `BYTE-FORCE_RAUNIT_RAJ_AI_Fix`, commits with `[AI-AGENT]` prefix
6. CI/CD Monitor checks GitHub Actions status, retries up to 5 times
7. Results saved to `results.json` and sent back to dashboard

---

## Security Requirements

<!-- FIX: Added mandatory security constraints section to document sandboxing, authentication, input validation, and AI review requirements prominently. -->

> ⚠️ **These are not optional.** The following security controls MUST be in place before any production or public deployment.

### Mandatory Sandboxing

The agent clones and executes code from user-supplied GitHub repository URLs. To prevent arbitrary code execution on the backend host:

- **`DOCKER_SANDBOX=true` is MANDATORY in production.** All cloned repositories must be executed inside an isolated, network-restricted Docker container with strict CPU, memory, and time limits.
- The repo URL MUST be validated server-side against an allowlist of accepted URL formats (e.g., `https://github.com/<org>/<repo>`). Reject any URL that does not match.
- Never run cloned code directly on the backend host outside a sandbox.

### AI-Generated Code Review Gate

The Fix Generator agent uses GPT/Gemini to generate code patches. AI-generated code is NOT automatically trusted:

- A **mandatory static analysis gate** (e.g., `flake8`, `bandit`) must run on every AI-generated patch before it is committed.
- Implement a **human-in-the-loop review step** for production use — do not auto-push AI fixes without validation.
- All generated patches must be logged for audit with full diff, timestamp, and model used.
- Never auto-push to a repository branch without passing the validation gate.

### API Authentication & Rate Limiting

- The `/api/run-agent` endpoint MUST require API key or OAuth authentication. Unauthenticated requests must be rejected with HTTP 401.
- Implement rate limiting per IP and per token (e.g., max 5 runs/hour per user) to prevent abuse and runaway AI API costs.
- All input fields (`repo_url`, `team_name`, `team_leader`) must be validated and sanitized server-side before use.

### Branch Name Sanitization

- `team_name` and `team_leader` values used in branch name construction MUST be sanitized to allow only alphanumeric characters, hyphens, and underscores.
- Use parameterized GitPython library calls — never interpolate user input directly into shell commands.

### Retry Limit Hard Cap

- `MAX_RETRIES` configured via environment variable is capped at a hard-coded maximum of **10** in code, regardless of the environment variable value. Setting `MAX_RETRIES` above 10 will be silently clamped to 10.

### Results File Isolation

- Each agent run generates results keyed by a unique UUID (e.g., `results_<uuid>.json`), not a shared `results.json`. This prevents concurrent run data corruption and overwriting.
- Document the storage location and apply appropriate access controls. Implement a retention/cleanup policy for old result files.

---

## Installation Instructions

### Prerequisites
- Node.js >= 18
- Python >= 3.10
- Docker >= 24 (**required** for sandboxed code execution — not optional)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/raunitx-02/buggy-test-repo.git
cd buggy-test-repo
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### 3. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend API runs at `http://localhost:8000`

---

## Environment Setup

<!-- FIX: Added explicit instructions to add .env to .gitignore before creating it, and to use .env.example with placeholders. Documented that secrets must never be committed. -->

> ⚠️ **CRITICAL — Read before creating your `.env` file:**
> 1. Add `.env` to your `.gitignore` **before** creating the file:
>    ```bash
>    echo ".env" >> .gitignore
>    git add .gitignore
>    git commit -m "chore: ensure .env is gitignored"
>    ```
> 2. **Never commit `.env` or any file containing real secrets to version control.**
> 3. Use the provided `.env.example` file (with placeholder values only) as a template. Copy it to `.env` and fill in your real values locally.
>    ```bash
>    cp backend/.env.example backend/.env
>    ```
> 4. Verify `.env` is not tracked: `git status` must not show `.env` as a staged or untracked file intended for commit.

Create a `.env` file in the `backend/` directory using `.env.example` as a template:

```env
# GitHub
# FIX: Placeholder values only — copy to .env and fill in real values. Never commit real secrets.
GITHUB_TOKEN=your_github_personal_access_token

# AI Provider (choose one)
OPENAI_API_KEY=your_openai_api_key
# OR
GOOGLE_API_KEY=your_gemini_api_key

# Agent Config
MAX_RETRIES=5
# NOTE: MAX_RETRIES is hard-capped at 10 in code regardless of this value.
BRANCH_PREFIX=AI_Fix

# Sandbox — MANDATORY in production. Must be true for any public or shared deployment.
DOCKER_SANDBOX=true
```

> The `.env.example` file in the repository contains only placeholder values. It is safe to commit. Your real `.env` file must never be committed.

---

## Usage Examples

### Via React Dashboard
1. Open the dashboard at your deployed URL
2. Enter:
   - **GitHub Repository URL**: `https://github.com/raunitx-02/buggy-test-repo`
   - **Team Name**: `Byte-Force`
   - **Team Leader**: `Raunit Raj`
3. Click **Run Agent**
4. Watch the real-time CI/CD timeline and fixes table populate

### Via API directly

<!-- FIX: Replaced placeholder backend URL in curl example with localhost to prevent accidental data leakage to unintended endpoints. -->
```bash
# FIX: Use the local development URL below. Replace with your actual verified backend URL for production — do not use a placeholder URL.
curl -X POST http://localhost:8000/api/run-agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "repo_url": "https://github.com/raunitx-02/buggy-test-repo",
    "team_name": "Byte-Force",
    "team_leader": "Raunit Raj"
  }'
```

> ⚠️ The `/api/run-agent` endpoint requires API key authentication (`X-API-Key` header). Unauthenticated requests will be rejected.

### Sample `results.json` output

<!-- FIX: Updated sample output to reflect UUID-keyed result files (e.g., results_<uuid>.json) instead of a shared results.json, to prevent concurrent run data corruption. -->
Results are stored per-run as `results_<uuid>.json` (e.g., `results_550e8400-e29b-41d4-a716-446655440000.json`) to prevent concurrent run conflicts. The run UUID is returned in the API response.

```json
{
  "run_id": "550e8400-e29b-41d4-a716-446655440000",
  "repository_url": "https://github.com/raunitx-02/buggy-test-repo",
  "team_name": "Byte-Force",
  "team_leader": "Raunit Raj",
  "branch_created": "BYTE-FORCE_RAUNIT_RAJ_AI_Fix",
  "total_failures": 5,
  "total_fixes": 5,
  "ci_status": "PASSED",
  "score": { "base": 100, "speed_bonus": 10, "efficiency_penalty": 0, "total": 110 },
  "fixes": [
    { "file": "src/utils.py", "bug_type": "LINTING", "line_number": 15, "commit_message": "[AI-AGENT] Remove unused import os in src/utils.py line 15", "status": "Fixed" },
    { "file": "src/validator.py", "bug_type": "SYNTAX", "line_number": 8, "commit_message": "[AI-AGENT] Add missing colon in src/validator.py line 8", "status": "Fixed" },
    { "file": "src/calculator.py", "bug_type": "LOGIC", "line_number": 28, "commit_message": "[AI-AGENT] Fix power() logic error in src/calculator.py line 28", "status": "Fixed" },
    { "file": "src/converter.py", "bug_type": "TYPE_ERROR", "line_number": 36, "commit_message": "[AI-AGENT] Fix seconds_to_hms return type in src/converter.py line 36", "status": "Fixed" },
    { "file": "src/loader.py", "bug_type": "IMPORT", "line_number": 7, "commit_message": "[AI-AGENT] Add PyYAML to requirements.txt for src/loader.py line 7", "status": "Fixed" }
  ]
}
```

---

## Supported Bug Types

| Bug Type | Description | Example |
|---|---|---|
| `LINTING` | Unused imports, style violations (flake8) | `import os` never used |
| `SYNTAX` | Python syntax errors | Missing colon on `def` |
| `LOGIC` | Wrong arithmetic or conditional logic | `base ** (exp+1)` instead of `base ** exp` |
| `TYPE_ERROR` | Wrong return type | Function returns `list` instead of `str` |
| `IMPORT` | Missing module not in requirements | `import yaml` with no PyYAML installed |
| `INDENTATION` | Wrong indentation levels | Mixed tabs/spaces |

---

## Tech Stack

### Frontend
- React 18 (Vite)
- Tailwind CSS
- Recharts (score visualization)
- Axios (API calls)
- Zustand (state management)

### Backend
- Python 3.10+
- FastAPI
- LangGraph (multi-agent orchestration)
- GitPython (git operations)
- flake8 (linting)
- pytest (test runner)
- Docker (**mandatory** for sandboxed execution in production)

### Infrastructure
- GitHub Actions (CI/CD)
- Vercel (frontend deployment)
- Railway (backend deployment)

---

## Known Limitations

- Agent currently supports Python repositories only (no JavaScript/TypeScript bug fixing)
- Maximum 5 CI/CD retry iterations (configurable up to a hard cap of 10)
- Docker sandbox is **required** — not optional — for safe code execution in production
- Very large repositories (>500 files) may exceed the agent's token context window
- GitHub API rate limiting may slow down CI/CD monitoring for rapid successive runs
- AI-generated fixes are subject to a mandatory static analysis gate before commit; purely automated push without review is disabled in production mode

---

## Team Members

| Name | Role |
|---|---|
| Raunit Raj | Team Leader, Full-Stack & Agent Development |
| Bhavesh Kumawat | Backend & Agent Architecture |
| Mohit Shrimali | Frontend & Dashboard Development |
| Hardik Nangia | DevOps & CI/CD Integration |

---

## Test Repository

This repository (`buggy-test-repo`) is the **intentionally buggy test repo** used to validate the agent.

| File | Bug Type | Line | Description |
|---|---|---|---|
| `src/utils.py` | `LINTING` | 15 | Unused `import os` |
| `src/validator.py` | `SYNTAX` | 8 | Missing colon on `def validate_username` |
| `src/calculator.py` | `LOGIC` | 28 | `power()` uses `exp+1` instead of `exp` |
| `src/converter.py` | `TYPE_ERROR` | 36 | `seconds_to_hms()` returns `list` instead of `str` |
| `src/loader.py` | `IMPORT` | 7 | `import yaml` but PyYAML missing from `requirements.txt` |

---

*Built with ❤️ for RIFT 2026 Hackathon — AIML DevOps Automation Track*