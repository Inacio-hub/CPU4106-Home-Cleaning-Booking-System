# CPU4106 assessment review and interface revision

## Explicit requirements

Source: CPU4106-20C Group Project Assessment S1/S2, October 2026.

| Brief section | Explicit requirement | Project evidence / limitation |
| --- | --- | --- |
| Section A, Objective and Internship Scenario | Team of 3–5; computing artefact linked to an SDG and business challenge. Frontend, backend, full stack or hardware integration permitted. | Three allocated members; HomeCare full stack booking system; prospective SDG 8 contribution. No measured economic benefit claimed. |
| Key Requirements | Scrum roles, backlog and sprint cycles; documented SDLC; Gantt/milestones; daily stand-up attendance and decisions. | Role allocation and planning documents available. Group reports review and rehearsal completion, but detailed event/contribution records are incomplete. Do not invent them. |
| Deliverables S1 and table Assessment components | Functional artefact 30%; individual article 25%; group viva/presentation 20%. | Python/SQLite application, article and 18-slide presentation. Technical verification does not prove independent authorship. |
| Live Viva and Presentation Details, Presentation Content | 15 minutes plus 5 minutes Q&A; plan, CASE diagrams, implementation and live interface/function tests. | UML use case, context DFD, database design and demonstration plan retained. |
| Visuals and Deliverables; Code Submission | Slides on Moodle and all source on GitHub. | Separate live Render URL and source repository URL supplied. GitHub Pages hosting is not specified in the brief. |
| Section B Portfolio Requirements | Weekly individual reflections approximately 200 ±10% words with practical evidence. | Check each member's own uploaded files and receipts. No uploads are changed by this revision. |
| Assessment Regulations & Important Information | Statement of Authenticity; acknowledgement of assistance; do not present AI-generated work as independently authored. | Accurate acknowledgement retained; personal authenticity statements remain unsigned until personally verified. |

## Marking criteria and conflicts

The 70–100% Group Artefact descriptor emphasises functionality, SDG alignment,
clear Scrum/SDLC practice, complete documentation and collaboration. The article
descriptor calls for analysis and IEEE references; the viva descriptor emphasises
system design, implementation, testing, strong visuals and confident delivery.
Project Management & Documentation explicitly requests complete stand-up records,
Scrum boards/backlogs, Gantt charts and risk management.

The general slide guidance permits 15–20 slides, while the excellent-band viva
descriptor says 15–18: retaining 18 satisfies both. The heading "Live Viva and
Presentation Details ... 25 marks" conflicts with the component table and rubric
which assign viva/presentation 20%; seek lecturer clarification rather than
silently changing the weighting. The brief lists 9 November 2026, while the group
reports a lecturer-confirmed presentation deadline of 2 November. Follow the
confirmed Moodle/lecturer deadline. An attractive homepage alone cannot close
missing project-management evidence or guarantee a grade.

## Design recommendations implemented

Homepage layout is a recommendation, not a prescribed brief template. Reduced
hero text and spacing, balanced appointment information, services/prices nearer
the first screen, concise demo notice and an appropriately qualified SDG 8
explanation. A public homepage precedes sign-in, as the group reports the lecturer
requested. Booking, allocation and staff actions retain server-side role checks.
Assistance information remains available in the footer. No paid services,
invented testimonials, external participants or measured business outcomes added.

## Verification scope

The current local run exercises 27 inherited integration regressions plus 6
hosting-adapter checks: persistence and server-trusted price/identity; validation
boundaries; two-client overlap; cancellation; allocation and status progression;
cleaner visibility; role/ownership denials; HTTPS origin/cookie configuration;
health endpoint and fictional-data notice. See REVIEW_REGRESSION_RESULTS.txt.
These new local checks are separate from the historical Windows 27-case run in
14.064 seconds, exit 0, and its eleven screenshot states.

JavaScript syntax, unique IDs and explicit labels were checked. Calculated CSS
foreground/background contrast is recorded separately from browser/device tests.
Responsive CSS includes a single-column layout below 750px; that rule alone does
not establish physical-device or screen-reader usability. Lighthouse is not
installed in this environment, so no Lighthouse score is claimed. Authenticated
browser walkthroughs and native mobile-device checks must not be described as
completed merely because HTTP regression tests pass.

## Hosting limitation

Render Free uses temporary local storage. SQLite data survives requests while
the instance runs but may reset on sleep, restart or redeploy. Existing historical
evidence and source are retained. No private customer database is uploaded or
deleted by this revision. A deployment restart has the previously disclosed demo
storage limitation. Keep the local app as a viva backup.
