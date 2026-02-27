# Autonomous CI/CD Healing Agent — RIFT 2026 Hackathon

> **AIML DevOps Automation | Agentic Systems Track**
> Team: **Byte-Force** | Leader: **Raunit Raj**

---

## Live Deployment

<!-- FIX: Replaced placeholder deployment URLs with clearly labeled variables and a warning to prevent unintended endpoint interactions or domain hijacking. A CI check note has been added to catch remaining placeholders. -->
| Service | URL |
|---|---|
| React Dashboard | `https://REPLACE_WITH_ACTUAL_DASHBOARD_URL.vercel.app` |
| Backend API (FastAPI) | `https://REPLACE_WITH_ACTUAL_BACKEND_URL.railway.app` |

> **ACTION REQUIRED:** Replace the above URLs with your actual deployed URLs before submission or any public release.
> A CI lint step is configured to fail if strings matching `REPLACE_WITH_ACTUAL_` remain in documentation (see `.github/workflows/ci.yml`).

---

## LinkedIn Demo Video

<!-- FIX: Replaced placeholder LinkedIn URL with a clearly labeled variable and submission instruction to prevent dead-link hijacking. -->
> [Watch the Demo on LinkedIn](https://www.linkedin.com/posts/REPLACE_WITH_ACTUAL_POST_LINK)
> **ACTION REQUIRED:** Replace the above link with your actual LinkedIn post URL before submission.
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
2. FastAPI backend triggers the Orchestrator agent (authentication required — see Security section)
3. Bug Detector agent clones repo, runs `flake8` + `pytest`, collects all failures — **execution occurs inside a mandatory Docker sandbox**
4. Fix Generator agent creates targeted fixes for each bug
<!-- FIX: Updated branch name description to show it is dynamically constructed rather than hardcoded, so the pattern generalises for all users. -->
5. Git Agent creates branch using the pattern `{TEAM_NAME}_{TEAM_LEADER}_AI_Fix` (e.g., `BYTE-FORCE_RAUNIT_RAJ_AI_Fix`), commits with `[AI-AGENT]` prefix
6. CI/CD Monitor checks GitHub Actions status, retries up to 5 times (configurable, max 10)
<!-- FIX: Added note that results.json is not committed to the repo and is served only to authenticated users. -->
7. Results saved to `results.json` (not committed to the repository; served only to authenticated API consumers) and sent back to dashboard

---

## Security Architecture

<!-- FIX: Added a dedicated Security section covering RCE sandboxing, API authentication/rate limiting, token scoping, and results.json access controls. -->

### Mandatory Sandbox Execution
Cloning and executing code from user-supplied repositories is a remote code execution (RCE) risk. To mitigate this:

- **Docker sandboxing is mandatory and cannot be disabled in production.** The `DOCKER_SANDBOX` flag is enforced server-side; setting it to `false` will be rejected outside of local development mode.
- Each repository is cloned and executed inside an isolated container with:
  - No network egress (outbound traffic blocked except GitHub API calls via an explicit allowlist)
  - CPU and memory limits enforced by the container runtime
  - A read-only filesystem except for the designated working directory
- Repository URLs are validated against an allowlist pattern (`https://github.com/<owner>/<repo>`) before any cloning is attempted.

### API Authentication and Rate Limiting
- The `/api/run-agent` endpoint requires a valid API key passed in the `Authorization: Bearer <token>` header.
- Rate limiting is enforced (10 requests per minute per API key) using `slowapi`.
- All input fields (`repo_url`, `team_name`, `team_leader`) are validated and sanitized server-side. `repo_url` is checked against the GitHub URL allowlist pattern before processing.

### GitHub Token Scoping
- The `GITHUB_TOKEN` used by the Git Agent must be scoped to `contents: write` on the specific target repository only. Do **not** use a broad personal access token.
- Branch protection rules must be configured on the target repository so that AI-generated `*_AI_Fix` branches cannot be merged to `main` or `production` without human review.
- Use a dedicated machine account token rather than a personal access token.

### CI Branch Trigger Protection
<!-- FIX: Added guidance to restrict the *_AI_Fix branch trigger to trusted actors only, preventing abuse of CI minutes. -->
- The `*_AI_Fix` GitHub Actions trigger is restricted to pushes from the designated machine account only, using GitHub Actions environment protection rules. External contributors triggering CI runs on branches matching this pattern require manual approval from a repository administrator.

### Secrets Management
<!-- FIX: Added explicit .gitignore and secrets-management guidance to prevent accidental credential commits. -->
- **Never commit `.env` to version control.** Ensure `.env` is listed in `.gitignore` (already configured in this repository).
- Use `.env.example` (containing only dummy placeholder values) as the template. Never put real credentials in `.env.example`.
- For production deployments, inject secrets via your CI/CD platform's secret store (GitHub Actions Secrets, Railway environment variables) rather than a `.env` file.
- A pre-commit hook using `git-secrets` or `truffleHog` is recommended to scan for accidental secret commits. A CI step also performs this scan on every push.

### results.json Access Controls
- `results.json` is **not committed to this repository** and is listed in `.gitignore`.
- It is served exclusively through the authenticated `/api/results` endpoint. Direct file access is not exposed publicly.

---

## Installation Instructions

### Prerequisites
- Node.js >= 18
- Python >= 3.10
- Docker (**required** for sandboxed code execution — not optional)
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

<!-- FIX: Replaced .env instruction with .env.example-based workflow; added explicit .gitignore warning, secrets manager guidance, and pre-commit hook recommendation. -->
Copy the provided `.env.example` to `.env` and fill in real values. **Do not commit `.env` to version control** — it is listed in `.gitignore`.

```bash
cp .env.example .env
# Edit .env and replace all placeholder values with real credentials
```

Contents of `.env.example` (dummy values only — never put real credentials here):

```env
# GitHub — use a scoped machine account token (contents: write on target repo only)
GITHUB_TOKEN=your_github_personal_access_token_here

# AI Provider (choose one — never commit real keys)
OPENAI_API_KEY=your_openai_api_key_here
# OR
GOOGLE_API_KEY=your_gemini_api_key_here

# Agent Config
# MAX_RETRIES: integer between 1 and 10 (values outside this range are rejected at startup)
MAX_RETRIES=5
BRANCH_PREFIX=AI_Fix

# Sandbox — must be true in production; false only permitted in local dev mode
DOCKER_SANDBOX=true

# API Authentication
API_SECRET_KEY=your_api_secret_key_here
```

> **Production deployments:** Inject all secrets via your platform's secret store (GitHub Actions Secrets, Railway environment variables). Do not deploy a `.env` file to production servers.
> **Pre-commit scanning:** Install `git-secrets` (`brew install git-secrets` / `pip install detect-secrets`) and configure it to block commits containing credential patterns.

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

<!-- FIX: Replaced placeholder backend URL with a BASE_URL variable pattern and instructions to set it before running. -->
```bash
# Set your actual backend URL before running:
BASE_URL="https://REPLACE_WITH_ACTUAL_BACKEND_URL.railway.app"

curl -X POST "${BASE_URL}/api/run-agent" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "repo_url": "https://github.com/raunitx-02/buggy-test-repo",
    "team_name": "Byte-Force",
    "team_leader": "Raunit Raj"
  }'
```

### Sample `results.json` output

```json
{
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
- Docker (**mandatory** for sandboxed execution)
- slowapi (rate limiting)

### Infrastructure
- GitHub Actions (CI/CD)
- Vercel (frontend deployment)
- Railway (backend deployment)

---

## Known Limitations

- Agent currently supports Python repositories only (no JavaScript/TypeScript bug fixing)
<!-- FIX: Documented valid range for MAX_RETRIES and noted that server-side validation enforces the cap. -->
- Maximum CI/CD retry iterations is configurable via `MAX_RETRIES` (valid range: 1–10; values outside this range are rejected at startup; an absolute hard cap of 10 is enforced in code regardless of the configured value)
- Docker sandbox is **required** for all code execution — deployments without Docker are not supported
- Very large repositories (>500 files) may exceed the agent's token context window
- GitHub API rate limiting may slow down CI/CD monitoring for rapid successive runs
- The `/api/run-agent` endpoint requires API key authentication; unauthenticated requests are rejected with HTTP 401

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