# Home Cleaning Service Booking System

CPU4106 Level 4 group project: Inacio Fernandes, Jevito Pereira and Socorrina Borges.

A complete local web application for customer bookings, administrator allocation and cleaner job progress. Proposed SDG 8 contribution: clearer small-business scheduling and workload records. Economic impact has not been measured.

## Open the live website

[**Open HomeCare: live cleaning booking website**](https://cpu4106-home-cleaning-demo.onrender.com/)

The website is hosted on Render and runs the Python/SQLite backend. The home
page and database health endpoint were verified in a browser on 31 October
2026. This check does not claim a new full hosted booking walkthrough.

The link opens a public homepage with service prices. Choose Book a cleaning or Sign in to access booking and staff workflows.

Use only fictional information. Accounts are shared, and temporary free
hosting storage can reset after sleep, restart or deployment. The first visit
after inactivity may take about a minute. See [HOSTING.md](HOSTING.md).

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

- index.html: full frontend, including CSS and JavaScript.
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

GitHub stores the source. Use the live Render link above to open the website, or run the original application locally as a backup. GitHub Pages does not run this Python/SQLite backend.

## Allocated responsibilities and assistance

Inacio: backend validation, storage, availability and booking-conflict checks. Jevito: customer interface, form, confirmation and validation messages. Socorrina: administrator allocation, cleaner dashboard and job-status workflow. Allocation does not prove independent authorship or testing.

AI substantially supported code, tests, diagrams and documentation. Each member must review and understand the work and confirm their actual contributions. No meetings, feedback or individual commit history are invented.

## Upload to GitHub

Extract this ZIP first. Upload the files INSIDE Home_Cleaning_Project to the repository root, including README.md, app.py, index.html, schema.sql, tests, launcher and .gitignore. Do not upload only the ZIP. Check repository access and provide the actual repository URL according to lecturer instructions. The source repository is public. The hosted coursework demo is available through the separate live Render URL above.

## Coursework documentation and evidence

See docs/PROJECT_GUIDE.md, docs/PLANNING_AND_REVIEW.md, docs/EVIDENCE_INDEX.md and docs/SUBMISSION_CHECKLIST.md. Upload docs/ and evidence/ alongside the root source files. Historical evidence and proposed activity records are clearly separated.





## Assessment and homepage review

See [ASSESSMENT_REVIEW.md](ASSESSMENT_REVIEW.md) for brief section references,
rubric priorities and limits. The homepage has a compact public layout, current
service prices and a prospective SDG 8 explanation. Sign-in remains required for
booking and staff workflows. New local checks are recorded in
[REVIEW_REGRESSION_RESULTS.txt](REVIEW_REGRESSION_RESULTS.txt); these do not add
to the historical Windows totals.
