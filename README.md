# Home Cleaning Service Booking System

## 🌐 [OPEN FULL WEBSITE — GITHUB PAGES](https://inacio-hub.github.io/CPU4106-Home-Cleaning-Booking-System/)

**Lecturer:** Click **OPEN FULL WEBSITE** above. Opening `index.html` in GitHub's file list shows source code, not the published website.

**GitHub Pages mode:** Public HomeCare homepage, service prices and fictional customer/admin/cleaner workflows run in your browser. Demo bookings use browser localStorage only: they are not shared across devices or browsers and do not use secure authentication. Use fictional addresses and the published demo password only.

**Original backend:** `app.py`, `deploy.py`, `schema.sql` and Python integration tests remain available for local assessment. GitHub Pages does not run Python or SQLite. To run the original backend locally, follow the Windows instructions below.

CPU4106 Level 4 group project: Inacio Fernandes, Jevito Pereira and Socorrina Borges.

An original complete local web application for customer bookings, administrator allocation and cleaner job progress. Proposed SDG 8 contribution: clearer small-business scheduling and workload records. Economic impact has not been measured.

## Website access

[**OPEN FULL WEBSITE — HomeCare public homepage**](https://inacio-hub.github.io/CPU4106-Home-Cleaning-Booking-System/)

The public GitHub Pages version needs no server login to view its homepage and service prices. Sign in with the fictional demo accounts below to try local browser-only booking and staff workflows. The original database-backed version is still available to run locally.

## Updated Python/SQLite homepage (31 October 2026)

The Python application now opens a public homepage with services, prices and booking steps before sign-in. `app.py` serves `backend-index.html` when present and falls back to `index.html` for older local packages. Download the complete repository to run this version; keep both frontend files. Protected actions still use the Python API and SQLite database. Existing databases are not included or overwritten.

The public homepage was observed through the Opera connector on Inacio's laptop. The earlier manual booking sequence showed requested, assigned, in-progress and completed states. That sequence preceded the homepage change. A new isolated Linux run of `python3 -m unittest test_audit.AuditTests` passed 27 tests in 3.844 seconds. JavaScript syntax and selected-service handoff logic also passed checks using a Node DOM stub, which is not a full browser interaction test. These results are separate from the historical Windows run and its 11 screenshot states.

GitHub Pages remains the separate browser-only preview. It cannot run this Python/SQLite application. Updating source does not verify a Render deployment.

## Run on Windows

1. Install Python 3.10 or later if needed. No external packages are required.
2. Extract the project folder and double-click start_windows.bat, or open a terminal in the folder and run `py app.py`.
3. Open http://127.0.0.1:8765/ in your browser.
4. Stop the server with Ctrl+C. SQLite creates cleaning.db automatically with fictional demo accounts and services. Do not upload that database.

On other platforms run `python3 app.py`.

## Demo accounts

- Customer: customer@example.test
- Administrator: admin@example.test
- Cleaner: cleaner@example.test
- Second test customer: other@example.test

All demo passwords: `DemoPass123!`. These are intentionally public fictional coursework accounts, not credentials for a real service.

## Features and demonstration

Customer: view services, request a future appointment, view own bookings and cancel eligible future bookings. A saved request reserves cleaner capacity and remains requested pending allocation.

Administrator: review requests and allocate the seeded cleaner. Cleaner: view allocated jobs, start work and complete it. Pending and cancelled requests are hidden from the cleaner view.

Use fictional addresses and an available future whole-hour slot. Bookings must fit within 08:00-18:00 and the next 30 days. Overlaps are rejected when no cleaner has capacity. In-progress and completed jobs cannot be cancelled through the demo workflow. Use a separate fresh booking to demonstrate cancellation.

## Source files

- backend-index.html: public homepage and customer/staff frontend for the Python/SQLite system shown in the final viva.
- index.html: separate browser-only GitHub Pages demonstration, using localStorage.
- app.py: Python HTTP server, sessions, role checks, validation and database operations.
- schema.sql: relational schema and constraints.
- test_app.py, test_week4.py, test_audit.py: integration tests and regression coverage.
- start_windows.bat: Windows launcher.
- .gitignore: excludes generated databases, caches and local settings.

## Tests and existing evidence

Run `py test_audit.py` on Windows, or `python3 test_audit.py` elsewhere. It runs the expanded 27-case suite using an isolated temporary database and port 8766. Do not add counts from inherited or repeated suites together.

Historical expanded audit: 18 passing and 9 failing tests before corrections, then all 27 passing. The corrected release subsequently passed all 27 Windows tests in 14.064 seconds with exit code 0. Eleven genuine Windows screenshot states document the booking, allocation, progress and cancellation workflows. Screenshot states are separate from automated test cases. These are recorded prior results, not a new execution during packaging. Detailed logs and screenshots are preserved under evidence/windows/ and in the separately supplied consolidated Windows evidence archive.

## Configuration and limitations

Optional environment variables: CLEANING_DB and CLEANING_PORT. Default database: cleaning.db beside app.py. Default port: 8765. The server binds to 127.0.0.1.

This local coursework prototype uses Python standard-library HTTP handling and SQLite. XAMPP, MySQL and FastAPI are not dependencies. It has one seeded cleaner, in-memory sessions and local business times. Real payments, external messaging, self-service registration, availability editing and production hosting are outside scope. Technical tests do not establish full security, accessibility or representative-user acceptance.

GitHub stores the source and GitHub Pages publishes the browser-only demonstration. The original Python/SQLite application runs locally and is not hosted by GitHub Pages.

## Allocated responsibilities and assistance

Inacio: backend validation, storage, availability and booking-conflict checks. Jevito: customer interface, form, confirmation and validation messages. Socorrina: administrator allocation, cleaner dashboard and job-status workflow. Allocation does not prove independent authorship or testing.

AI substantially supported code, tests, diagrams and documentation. Each member must review and understand the work and confirm their actual contributions. No meetings, feedback or individual commit history are invented.

## Upload to GitHub

Extract this ZIP first. Upload the files INSIDE Home_Cleaning_Project to the repository root, including README.md, app.py, index.html, schema.sql, tests, launcher and .gitignore. Do not upload only the ZIP. Check repository access and provide the actual repository URL according to lecturer instructions. The source repository is public. The browser-only demo is linked at the top of this README.

## Coursework documentation and evidence

See docs/PROJECT_GUIDE.md, docs/PLANNING_AND_REVIEW.md, docs/EVIDENCE_INDEX.md and docs/SUBMISSION_CHECKLIST.md. Upload docs/ and evidence/ alongside the root source files. Historical evidence and proposed activity records are clearly separated.





## Assessment and homepage review

See [ASSESSMENT_REVIEW.md](ASSESSMENT_REVIEW.md) for brief section references,
rubric priorities and limits. The latest source includes a compact public layout, current
service prices and a prospective SDG 8 explanation. GitHub Pages may need publication to be enabled in repository Settings → Pages (Deploy from branch: main, /(root)). Sign-in remains required for
booking and staff workflows. New local checks are recorded in
[REVIEW_REGRESSION_RESULTS.txt](REVIEW_REGRESSION_RESULTS.txt); these do not add
to the historical Windows totals.
