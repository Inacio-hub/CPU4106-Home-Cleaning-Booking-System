# Live coursework demo deployment

The complete app needs a Python host. GitHub contains the source; GitHub Pages
cannot execute the Python backend. The original app.py, schema and frontend
remain unchanged. deploy.py adds a hosted launcher with HTTPS-origin handling,
Secure session cookies behind HTTPS, a health endpoint, and a visible demo notice.

## Render configuration

- Repository: https://github.com/Inacio-hub/CPU4106-Home-Cleaning-Booking-System
- Branch: main; runtime: Python; plan: Free.
- Build: `python -m py_compile app.py deploy.py`
- Start: `python deploy.py`
- Health check: `/healthz`
- Python version: 3.13.5.
- CLEANING_DB: `/tmp/cpu4106-demo.sqlite3`
- Render supplies PORT and RENDER_EXTERNAL_URL automatically.
- No real customer database, credentials or private information is uploaded.

## Verified live URL

https://cpu4106-home-cleaning-demo.onrender.com/

The owner deployed the Free service from the Blueprint. The supplied Render
screen shows Live at source commit 8bae1d7cef1908bd95c1f491c0b81ebdf88e6ca3.
On 31 October 2026, the browser displayed the HomeCare sign-in page and visible
demo warning. /healthz returned {"status": "ok", "mode": "coursework-demo"}.
No complete new hosted role workflow is claimed by this availability check.

## Important demonstration limits

This remains a classroom prototype using Python's standard-library HTTP server,
not a production service. Accounts are intentionally public and shared. Only
fictional data should be entered. SQL records persist between requests while
this instance runs, but free Render local storage resets on sleep, restart or
redeploy. The service can take about a minute to wake after 15 minutes idle.
Open it before the viva. Durable hosting would require a separate agreed change.

## Website and source links

README.md provides the live website link. Slide 18 provides separate clickable
links for the live website and GitHub source. The github.com repository address
continues to open code; the onrender.com address opens the running website.

## Evidence

Historical 27-test Windows results and 11 screenshot states describe the tested
local release at commit 155aff203e75da5f15865dcf640f878cb544bb86. Hosted-adapter
tests are separate new verification, not additional historical Windows cases.
The live availability check covers the homepage and health endpoint only; historical local test and screenshot totals remain separate.

