1 Final playback (validated)
Outcome, scope, governance


ID
Item
Locked position
CTX-001
Outcome
Build a reusable scenario tool + decision-support pack showing the year-on-year shift in workforce age/experience/capability profile.
CTX-002
Baseline
Use the latest approved P&A headcount report as the starting population.
CTX-003
Scope
P&A sub-function only, approximately 1,100 people.
CTX-004
Population
Include all employees, including Early Careers cohorts such as apprentices and graduates.
CTX-005
Experience proxy
Use age bands + service length + job family + grade.
CTX-006
Deadline
End May 2026.
GOV-001
Source system
Workforce data sourced from Workday AP reports.
GOV-002
Storage
Initial output stored in the access-controlled P&A Business Operations library.
GOV-003
Classification
Treat outputs as restricted management information until credible and approved for wider sharing.
GOV-004
Sign-off standard for wider sharing
Method credibility + data credibility are required. Narrative will always contain subjectivity, so method becomes the decisive factor.
Analytical method and presentation posture


ID
Item
Locked position
CTX-009
Primary tipping-point method
Weighted Experience Index (WEI) decline is the preferred primary measure.
CTX-010
Secondary presentation lenses
Simple crossover and capability-risk views may be used for simplified presentation and proof-of-concept discussion.
CTX-013
Preferred WEI design
Reference-profile method: compare future workforce states against the current “as is” profile.
CTX-014
Minimum fallback
If reference-profile is not fully supportable, use an expert-weighted WEI with transparent assumptions.
CTX-011
Reusability expectation
A small set of pre-set scenarios is enough for “done”; full free-form modelling is not required initially.
CTX-012
Minimum output standard
Minimum accepted package is a decision-support pack.
Decision rights / ownership


ID
Decision area
Owner
DEP-006
Baseline workforce definition
Requester / customer owner
DEP-007
Attrition assumption
Requester / customer owner
DEP-008
Early Careers intake assumption
Requester / customer owner
DEP-009
Capability-risk interpretation
Engineering director owner
DEP-010
Wider-sharing approval
Engineering director owner
2) Final requirement set
Functional requirements


ID
Requirement
Priority
FR-001
Load a baseline workforce population from the latest approved P&A headcount report.
Must
FR-002
Model the workforce forward year by year using ageing, inflow, outflow, and retirement rules.
Must
FR-003
Include all employee populations, including Early Careers cohorts.
Must
FR-004
Support separate treatment of apprentices and graduates where needed.
Could
FR-005
Apply annual Early Careers intake using configurable assumptions and explicit age-band definitions.
Must
FR-006
Apply annual attrition using the most recent full-year attrition profile.
Must
FR-007
Track workforce composition by age band, service length, job family, and grade over time.
Must
FR-008
Calculate a Weighted Experience Index to show change in aggregate experience/capability profile over time.
Must
FR-009
Provide secondary views for simple cohort crossover and capability-risk interpretation.
Should
FR-010
Produce visual outputs that make trend, cohort shift, and tipping point easy to interpret.
Must
FR-011
Allow authorised users to adjust a defined set of assumptions and rerun pre-set scenarios without redesigning the model.
Must
FR-012
Support alternative scenario presets such as high-attrition / high-intake cases.
Should
FR-013
Support alternative retirement-age assumptions.
Should
FR-014
Support alternative projection horizons.
Should
FR-015
Support alternative grade progression / promotion assumptions.
Should
FR-016
Support separate job-family behaviour where required.
Could
FR-017
Use the current workforce profile as the reference baseline for the preferred WEI method.
Must
FR-018
If the reference-profile method is not yet supportable, allow an expert-weighted WEI fallback.
Should
FR-019
Implement a proxy retirement rule based on thresholds and assumptions, rather than requiring a fixed hard retirement age.
Must
Non-functional requirements
I’ve tightened these so they are testable rather than just aspirational.


ID
Requirement
Metric
Threshold
Test
NFR-001
Output must be suitable for a restricted management-information setting.
Access scope
Restricted audience only until approval
Verify storage location and audience permissions before circulation
NFR-002
The model must be transparent and challengeable.
Assumption visibility
All active scenario drivers visible in one place
Confirm assumptions register exists and matches model inputs
NFR-003
The approach must avoid premature platform lock-in.
Design coupling
Method can be described independently of implementation tool
Review method note without reference to specific platform features
NFR-004
Person-level data exposure must be minimised in outputs.
Granularity of published outputs
Leadership outputs aggregated; no unnecessary person-level display
Review final pack for aggregate presentation only
NFR-005
Senior stakeholders must be able to understand and challenge the logic.
Explainability
WEI method and scenario logic summarised in concise form
Review with non-technical stakeholder and confirm interpretability
NFR-006
The design must support later creation of a sanitised simplified version if approved.
Abstraction readiness
Business logic separable from organisation-specific labels
Review whether labels/terms can be abstracted without changing method
NFR-007
Claims in the pack must remain proportionate to evidence.
Claim strength
No conclusion presented as causal if only scenario-based
Review narrative and caveats against evidence level
NFR-008
Wider sharing requires method and data credibility.
Sign-off gate
Method note + assumptions register + scenario comparison accepted as credible by designated approvers
Explicit review against sign-off pack contents
3) Acceptance criteria (finalised)


ID
Acceptance criterion
Traceability
AC-001
The model can project the P&A workforce forward from the latest approved baseline over a configurable number of years.
FR-001, FR-002, FR-014
AC-002
The user can change at least Early Careers intake %, attrition %, and attrition age distribution.
FR-005, FR-006, FR-011
AC-003
The output shows change over time by age band, service length, job family, and grade.
FR-007, FR-010
AC-004
The output includes a WEI with a visible year-by-year trend and a clearly identified decline point or threshold event.
FR-008
AC-005
The output also provides at least one simplified presentation lens using either cohort crossover or capability-risk view.
FR-009
AC-006
The minimum decision-support pack includes assumptions register and scenario comparison table.
CTX-012
AC-007
The analysis can be rerun using a small number of pre-set scenarios without altering core logic.
FR-011, FR-012
AC-008
Assumptions and calculated outputs are clearly separated so stakeholders can challenge the model without ambiguity.
NFR-002, FR-011
AC-009
Retirement proxy assumptions, projection horizon, and promotion/grade assumptions can be varied if enabled in the selected scenario set.
FR-013, FR-014, FR-015, FR-019
AC-010
The preferred WEI compares projected future states against the current reference profile.
FR-017
AC-011
If the preferred WEI cannot be fully implemented, the prototype still provides an expert-weighted WEI with transparent assumptions.
FR-018, NFR-002
AC-012
Wider sharing cannot proceed unless method and data credibility are judged acceptable by the designated approvers.
GOV-004, NFR-008
4) Artefacts required by end May


ID
Artefact
Priority
Notes
ART-001
Assumptions register
Must
Core challenge/control document
ART-002
Scenario comparison table
Must
Essential because attrition will be debated
ART-003
Decision-support report / slide pack
Should
Presentation-ready output
ART-004
WEI method note
Should
Critical for method credibility
ART-005
Caveats and limitations note
Should
Protects against overclaiming
ART-006
Restricted-audience summary narrative for leadership
Should
Useful for controlled stakeholder discussion
ART-007
Data dictionary / field map
Could
Helpful but not essential for first proof of concept
ART-008
Re-runnable prototype model
Could
Valuable, but not required for initial “done” threshold
5) Dependency and readiness view


ID
Dependency
Status
Practical implication
DEP-001
Latest approved P&A headcount baseline
Green
Good starting anchor
DEP-002
2024/25 attrition extract
Amber
High attention area; likely challenge point
DEP-011
Service length field
Amber
Experience proxy may need caveating
DEP-012
Job family field
Green
Ready
DEP-013
Grade field
Green
Ready
DEP-014
Early Careers identification
Amber
Separate apprentice/graduate treatment may be partial
DEP-015
Retirement-age rule / proxy
Red → now mitigated by FR-019
Use proxy retirement logic instead of waiting for a hard rule
6) Risk register (final)


ID
Risk
Impact
Mitigation
R-001
Capability risk may remain disputed if not explicitly defined.
H
Use WEI as primary method and lighter secondary views for presentation
R-002
Early Careers subgroups may behave differently and distort pooled assumptions.
H
Keep separate modelling optional for prototype
R-003
Politically sensitive findings may trigger pushback before method acceptance.
H
Restrict circulation and keep proof-of-concept framing
R-004
External sanitised prototyping could create governance concern if abstraction is incomplete.
M
Keep outside current scope unless separately approved
R-005
Attrition assumptions will be hotly debated.
H
Use explicit scenario comparison rather than a single “truth”
R-006
No hard retirement rule exists.
M
Use proxy retirement rule based on thresholds/assumptions
R-007
Amber fields may weaken segmentation fidelity.
M
Degrade gracefully and caveat where fidelity is lower
7) Retirement proxy stance (locked)
You chose a proxy retirement rule rather than excluding the concept.
Locked requirement


ID
Item
Locked position
FR-019
Retirement modelling
Model retirement using a proxy rule based on thresholds and assumptions, such as the proportion of people above a chosen age likely to retire each year, a natural upper-age cut-off if observed, or a maximum dwell period within the oldest age band.
Recommended prototype framing
Use this wording in the assumptions register:
Retirement is modelled as a scenario-based proxy, not a factual prediction.
The prototype may apply a configurable rule for employees in the oldest age band(s), such as an annual probability of exit above a threshold age, or a maximum dwell-time assumption in the oldest age category.
This is strong because it avoids pretending precision where none exists.
8) Coverage scoring (final)


Area
Score
Reason
Functional
5.0 / 5
Core behaviours, controls, outputs, fallback logic, and retirement stance are now defined
Non-functional
4.0 / 5
Governance, credibility, explainability, and sign-off gate are now measurable
Constraints
4.5 / 5
Scope, restricted handling, source system, and proof-of-concept posture are clear
Dependencies
4.5 / 5
Major inputs identified, statused, and retirement risk mitigated
Risks
4.5 / 5
Main methodological and political risks are explicit with mitigation direction
Acceptance criteria
4.5 / 5
Strong traceability and clear done-tests for a first prototype
NFR check
Because NFR score is now ≥3, I checked for metric + threshold + test and added them explicitly under NFR-001 to NFR-008.
9) Reviewable conclusion
What “done enough for end May” now looks like
A credible first proof of concept exists if you can produce:
A baseline-driven scenario model for the P&A population
A visible WEI trend against the current reference profile
A scenario comparison table, especially around attrition assumptions
A clean assumptions register
A short decision-support narrative that stays proportional to the evidence
Clear caveats around attrition, service length fidelity, and retirement proxy logic
What is most likely to make or break acceptance
Not the data source itself — that is broadly accepted.
The decisive issue is whether the method is seen as transparent, proportionate, and challengeable, especially around attrition assumptions.
10) JSON Lines record (single interview record)
{"interview_id":"INT-2026-04-20-001","aggregationMode":"single","status":"phase_4_complete","style":["Requirements Elicitation","Governance"],"domain":["Data/Analytics","Facilities/Asset Engineering"],"output":"Markdown","context":[{"id":"CTX-001","text":"Reusable scenario tool and decision-support pack to show year-on-year shift in workforce age, experience, and capability profile."},{"id":"CTX-002","text":"Baseline is the latest approved P&A headcount report."},{"id":"CTX-003","text":"Scope is the P&A sub-function only, approximately 1100 people."},{"id":"CTX-004","text":"Population includes all employees, including Early Careers cohorts such as apprentices and graduates."},{"id":"CTX-005","text":"Experience proxy uses age bands, service length, job family, and grade."},{"id":"CTX-006","text":"Deadline is end May 2026."},{"id":"CTX-009","text":"Primary tipping-point method is Weighted Experience Index decline."},{"id":"CTX-010","text":"Secondary presentation lenses include cohort crossover and capability-risk views."},{"id":"CTX-011","text":"A small set of pre-set scenarios is sufficient for done."},{"id":"CTX-012","text":"Minimum accepted package is a decision-support pack."},{"id":"CTX-013","text":"Preferred WEI method is reference-profile comparison against the current workforce profile."},{"id":"CTX-014","text":"Minimum acceptable fallback is an expert-weighted WEI."}],"governance":[{"id":"GOV-001","text":"Source data comes from Workday AP reports."},{"id":"GOV-002","text":"Initial storage location is the access-controlled P&A Business Operations library."},{"id":"GOV-003","text":"Outputs are restricted management information until credible and approved for wider sharing."},{"id":"GOV-004","text":"Wider sharing requires method credibility and data credibility; narrative remains inherently subjective."}],"owners":[{"id":"DEP-006","text":"Requester/customer owner decides baseline workforce definition."},{"id":"DEP-007","text":"Requester/customer owner decides attrition assumption."},{"id":"DEP-008","text":"Requester/customer owner decides Early Careers intake assumption."},{"id":"DEP-009","text":"Engineering director owner decides capability-risk interpretation."},{"id":"DEP-010","text":"Engineering director owner signs off wider sharing."}],"requirements":[{"id":"FR-001","text":"Load baseline workforce from latest approved P&A headcount report.","priority":"Must"},{"id":"FR-002","text":"Model the workforce forward year by year using ageing, inflow, outflow, and retirement rules.","priority":"Must"},{"id":"FR-003","text":"Include all employee populations, including Early Careers cohorts.","priority":"Must"},{"id":"FR-004","text":"Support separate treatment of apprentices and graduates where needed.","priority":"Could"},{"id":"FR-005","text":"Apply annual Early Careers intake using configurable assumptions and explicit age-band definitions.","priority":"Must"},{"id":"FR-006","text":"Apply annual attrition using the most recent full-year attrition profile.","priority":"Must"},{"id":"FR-007","text":"Track workforce composition by age band, service length, job family, and grade over time.","priority":"Must"},{"id":"FR-008","text":"Calculate a Weighted Experience Index to show change in aggregate experience/capability profile over time.","priority":"Must"},{"id":"FR-009","text":"Provide secondary views for simple cohort crossover and capability-risk interpretation.","priority":"Should"},{"id":"FR-010","text":"Produce visual outputs that make trend, cohort shift, and tipping point easy to interpret.","priority":"Must"},{"id":"FR-011","text":"Allow authorised users to adjust a defined set of assumptions and rerun pre-set scenarios without redesigning the model.","priority":"Must"},{"id":"FR-012","text":"Support alternative scenario presets such as high-attrition and high-intake cases.","priority":"Should"},{"id":"FR-013","text":"Support alternative retirement-age assumptions.","priority":"Should"},{"id":"FR-014","text":"Support alternative projection horizons.","priority":"Should"},{"id":"FR-015","text":"Support alternative grade progression and promotion assumptions.","priority":"Should"},{"id":"FR-016","text":"Support separate job-family behaviour where required.","priority":"Could"},{"id":"FR-017","text":"Use the current workforce profile as the reference baseline for the preferred WEI method.","priority":"Must"},{"id":"FR-018","text":"If the reference-profile method is not yet supportable, allow an expert-weighted WEI fallback.","priority":"Should"},{"id":"FR-019","text":"Implement a proxy retirement rule based on thresholds and assumptions, rather than relying on a fixed hard retirement age.","priority":"Must"}],"non_functional":[{"id":"NFR-001","text":"Output must be suitable for a restricted management-information setting.","metric":"Access scope","threshold":"Restricted audience only until approval","test":"Verify storage location and audience permissions before circulation"},{"id":"NFR-002","text":"The model must be transparent and challengeable.","metric":"Assumption visibility","threshold":"All active scenario drivers visible in one place","test":"Confirm assumptions register exists and matches model inputs"},{"id":"NFR-003","text":"The approach must avoid premature platform lock-in.","metric":"Design coupling","threshold":"Method can be described independently of implementation tool","test":"Review method note without reference to tool-specific features"},{"id":"NFR-004","text":"Person-level data exposure must be minimised in outputs.","metric":"Granularity of published outputs","threshold":"Leadership outputs aggregated; no unnecessary person-level display","test":"Review final pack for aggregate presentation only"},{"id":"NFR-005","text":"Senior stakeholders must be able to understand and challenge the logic.","metric":"Explainability","threshold":"WEI method and scenario logic summarised in concise form","test":"Review with non-technical stakeholder and confirm interpretability"},{"id":"NFR-006","text":"The design must support later creation of a sanitised simplified version if approved.","metric":"Abstraction readiness","threshold":"Business logic separable from organisation-specific labels","test":"Review whether terms can be abstracted without changing method"},{"id":"NFR-007","text":"Claims in the pack must remain proportionate to evidence.","metric":"Claim strength","threshold":"No scenario-based conclusion presented as causal","test":"Review narrative and caveats against evidence level"},{"id":"NFR-008","text":"Wider sharing requires method and data credibility.","metric":"Sign-off gate","threshold":"Method note, assumptions register, and scenario comparison accepted as credible by designated approvers","test":"Explicit review against sign-off pack contents"}],"acceptance_criteria":[{"id":"AC-001","text":"The model can project the P&A workforce forward from the latest approved baseline over a configurable number of years."},{"id":"AC-002","text":"The user can change at least Early Careers intake percentage, attrition percentage, and attrition age distribution."},{"id":"AC-003","text":"The output shows change over time by age band, service length, job family, and grade."},{"id":"AC-004","text":"The output includes a WEI with a visible year-by-year trend and a clearly identified decline point or threshold event."},{"id":"AC-005","text":"The output also provides at least one simplified presentation lens using either cohort crossover or capability-risk view."},{"id":"AC-006","text":"The minimum decision-support pack includes assumptions register and scenario comparison table."},{"id":"AC-007","text":"The analysis can be rerun using a small number of pre-set scenarios without altering core logic."},{"id":"AC-008","text":"Assumptions and calculated outputs are clearly separated so stakeholders can challenge the model without ambiguity."},{"id":"AC-009","text":"Retirement proxy assumptions, projection horizon, and promotion or grade assumptions can be varied if enabled in the selected scenario set."},{"id":"AC-010","text":"The preferred WEI compares projected future states against the current reference profile."},{"id":"AC-011","text":"If the preferred WEI cannot be fully implemented, the prototype still provides an expert-weighted WEI with transparent assumptions."},{"id":"AC-012","text":"Wider sharing cannot proceed unless method and data credibility are judged acceptable by the designated approvers."}],"artefacts":[{"id":"ART-001","text":"Assumptions register","priority":"Must"},{"id":"ART-002","text":"Scenario comparison table","priority":"Must"},{"id":"ART-003","text":"Decision-support report or slide pack","priority":"Should"},{"id":"ART-004","text":"WEI method note","priority":"Should"},{"id":"ART-005","text":"Caveats and limitations note","priority":"Should"},{"id":"ART-006","text":"Restricted-audience summary narrative for leadership","priority":"Should"},{"id":"ART-007","text":"Data dictionary or field map","priority":"Could"},{"id":"ART-008","text":"Re-runnable prototype model","priority":"Could"}],"dependencies":[{"id":"DEP-001","text":"Latest approved P&A headcount baseline","status":"Green"},{"id":"DEP-002","text":"2024/25 attrition extract","status":"Amber"},{"id":"DEP-011","text":"Service length field readiness","status":"Amber"},{"id":"DEP-012","text":"Job family field readiness","status":"Green"},{"id":"DEP-013","text":"Grade field readiness","status":"Green"},{"id":"DEP-014","text":"Early Careers identification readiness","status":"Amber"},{"id":"DEP-015","text":"Retirement-age rule or proxy readiness","status":"Mitigated via FR-019"}],"risks":[{"id":"R-001","text":"Capability risk may remain disputed if not explicitly defined.","impact":"H"},{"id":"R-002","text":"Early Careers subgroups may behave differently and distort pooled assumptions.","impact":"H"},{"id":"R-003","text":"Politically sensitive findings may trigger pushback before method acceptance.","impact":"H"},{"id":"R-004","text":"External sanitised prototyping could create governance concern if abstraction is incomplete.","impact":"M"},{"id":"R-005","text":"Attrition assumptions will be hotly debated.","impact":"H"},{"id":"R-006","text":"No hard retirement rule exists.","impact":"M"},{"id":"R-007","text":"Amber fields may weaken segmentation fidelity.","impact":"M"}],"coverage":{"functional":5.0,"non_functional":4.0,"constraints":4.5,"dependencies":4.5,"risks":4.5,"acceptance_criteria":4.5},"interview_result":"Validated specification complete for first proof of concept"}