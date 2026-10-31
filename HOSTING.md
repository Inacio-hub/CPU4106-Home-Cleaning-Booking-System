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

render.yaml defines these settings. Creating the service still requires the
owner's connected Render account. A deployment file is not a deployed website.
Record the actual successful deployment URL before updating presentation links.

## Important demonstration limits

This remains a classroom prototype using Python's standard-library HTTP server,
not a production service. Accounts are intentionally public and shared. Only
fictional data should be entered. SQL records persist between requests while
this instance runs, but free Render local storage resets on sleep, restart or
redeploy. The service can take about a minute to wake after 15 minutes idle.
Open it before the viva. Durable hosting would require a separate agreed change.

## Links after verified deployment

Add an **Open live coursework website** link near the top of README.md and put
the same real HTTPS URL on slide 18. Retain a separate source-code repository
link. The repository's github.com address will continue to open source code;
the live website has its own address.

## Evidence

Historical 27-test Windows results and 11 screenshot states describe the tested
local release at commit 155aff203e75da5f15865dcf640f878cb544bb86. Hosted-adapter
tests are separate new verification, not additional historical Windows cases.
Do not describe hosted browser behaviour as verified until deployment is tested.
