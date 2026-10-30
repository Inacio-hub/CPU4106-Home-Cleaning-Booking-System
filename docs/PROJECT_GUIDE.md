# Project guide

## Scope and SDG
A local booking system for a proposed small cleaning business, with customers, administrators and cleaners. SDG 8 is supported as a potential contribution to scheduling productivity and organised enterprise records; measured economic impact is not claimed.

## Architecture and data
HTML/CSS/JavaScript calls a Python standard-library HTTP API using JSON. SQLite stores Users, Services, CleanerAvailability and Bookings. Sessions identify users and roles. Foreign keys protect relationships. Prices use integer pence. Parameterised SQL separates input from query syntax. BEGIN IMMEDIATE protects the capacity check and insertion.

## Core acceptance criteria
- Valid known-service requests use future whole-hour times within 30 days, fit business hours 08:00-18:00, and have a text address of 8-250 characters.
- Server-derived customer identity, service price and duration override untrusted submitted values.
- Ownership and role checks prevent unauthorised record access and actions.
- Requested bookings reserve capacity; conflicting or concurrent requests cannot overbook the seeded cleaner.
- Administrator allocation produces assigned. Cleaner start produces in_progress, then completion produces completed.
- Customer cancellation is limited to eligible owned future bookings and releases capacity. Requested/cancelled jobs are hidden from the cleaner view.

## API examples
GET /api/services lists services. POST /api/login establishes a session. GET /api/bookings returns permitted records. POST /api/bookings creates a request. POST /api/bookings/{id}/assign, /cancel and /status implement role-controlled actions. Valid creation returns 201; invalid input 400, missing authentication 401, denied permission 403, invalid paths 404 and capacity/state conflicts 409. See source and tests for exact request fields and case-specific behaviour.

## SDLC evidence
Requirements: requirements_backlog.csv and acceptance criteria above. Design: context.svg, f3_use_case.svg and schema.sql. Implementation: app.py and index.html. Verification: 27-case audit and dated evidence folders. Evaluation: limitations and outstanding human-review records. Diagrams are retained Week 3 models; the final viva shows an adapted editable UML version, including separate Start job and Complete job use cases.

## Allocated responsibilities
Inacio Fernandes: backend validation, storage, availability and booking-conflict checks. Jevito Pereira: customer form, confirmation and validation messages. Socorrina Borges: administrator allocation, cleaner dashboard and status workflow. These allocations do not establish independent implementation or testing.

## Limits
One seeded cleaner, local times, no real payments, external messaging, self-service registration or availability editor. No production readiness or complete security/accessibility certification. Genuine contribution, discussion and user-review findings must be recorded by the members, not inferred from templates.
