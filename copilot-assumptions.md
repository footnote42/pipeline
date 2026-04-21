**Assumptions Register Template**

Workforce Age / Experience Scenario Model

Classification: Restricted Management Information

Scope: P&A sub-function only

Population: All employees including Early Careers cohorts

Primary analytical method: Weighted Experience Index (WEI) decline

Preferred WEI design: Reference-profile comparison against current “as is” workforce profile

Fallback WEI design: Expert-weighted WEI

Status: Draft working register

---

**1) Document control**

__

|   |   |
|---|---|
|Field|Value|
|Register ID|AR-001|
|Version|v0.1|
|Owner|Requester / Customer Owner|
|Method reviewer|Engineering Director Owner|
|Data source|Workday AP reports|
|Storage location|Access-controlled P&A Business Operations library|
|Wider-sharing gate|Method credibility + data credibility|
|Last updated|[DD/MM/YYYY]|
|Next review date|[DD/MM/YYYY]|

---

**2) How to use this register**

Use one row per assumption.

Recommended status values:

- Proposed
- Accepted
- Rejected
- Superseded
- Needs evidence

Recommended sensitivity values:

- H = highly material to outcome / likely to be challenged
- M = moderately material
- L = low materiality

---

**3) Master register**

__

|   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|
|Assumption ID|Section|Assumption statement|Base-case value / rule|Allowed alternatives / scenario values|Rationale|Evidence / source|Owner|Status|Sensitivity|Related Stable IDs|Review date|

---

**4) Register entries (pre-populated template)**

**A. Baseline, scope, and population assumptions**

__

|   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|
|Assumption ID|Section|Assumption statement|Base-case value / rule|Allowed alternatives / scenario values|Rationale|Evidence / source|Owner|Status|Sensitivity|Related Stable IDs|Review date|
|AS-001|Baseline|Baseline population is taken from the latest approved P&A headcount report.|Latest approved P&A headcount snapshot|Alternative snapshot only if explicitly approved|Common baseline required for all scenarios|Latest approved headcount extract|Requester / Customer Owner|Proposed|H|CTX-002, CTX-003, FR-001, AC-001, DEP-001|[DD/MM/YYYY]|
|AS-002|Scope|Model scope is limited to the P&A sub-function.|P&A only|None unless scope expansion is formally approved|Keeps first proof of concept bounded and reviewable|Agreed interview output|Requester / Customer Owner|Accepted|H|CTX-003, GOV-003|[DD/MM/YYYY]|
|AS-003|Population|Population includes all employees, including Early Careers cohorts such as apprentices and graduates.|All employees in scope|Apprentices / graduates may be separated in optional scenarios|Required to reflect intake mix and experience shift|Agreed interview output + headcount definition|Requester / Customer Owner|Accepted|H|CTX-004, FR-003, FR-004|[DD/MM/YYYY]|
|AS-004|Experience proxy|Experience / capability risk is represented using age band, service length, job family, and grade.|Four-factor proxy|If one field is weak, model may degrade gracefully with caveat|Avoids relying on age alone|Agreed interview output|Engineering Director Owner|Proposed|H|CTX-005, FR-007, FR-008, R-001|[DD/MM/YYYY]|

---

**B. Attrition logic assumptions**

__

|   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|
|Assumption ID|Section|Assumption statement|Base-case value / rule|Allowed alternatives / scenario values|Rationale|Evidence / source|Owner|Status|Sensitivity|Related Stable IDs|Review date|
|AS-101|Attrition logic|Annual attrition percentage used in the model.|[TBC]% per year|Low / Base / High attrition presets|Attrition is a key driver and likely challenge point|2024/25 attrition extract + owner decision|Requester / Customer Owner|Proposed|H|FR-006, FR-011, FR-012, AC-002, AC-007, R-005, DEP-002|[DD/MM/YYYY]|
|AS-102|Attrition logic|Attrition age distribution is based on the most recent full-year attrition profile.|2024/25 age distribution|Alternative distribution if later evidence supersedes|Keeps model anchored to observed pattern rather than arbitrary split|2024/25 attrition extract|Requester / Customer Owner|Proposed|H|FR-006, AC-002, DEP-002, R-005|[DD/MM/YYYY]|
|AS-103|Attrition logic|Attrition age distribution is applied proportionally each simulated year unless a scenario overrides it.|Fixed annual proportional application|Year-specific or scenario-specific distribution overrides|Simple, explainable first-pass rule|Modelling choice for prototype|Requester / Customer Owner|Proposed|H|FR-006, FR-011, AC-007, NFR-002|[DD/MM/YYYY]|
|AS-104|Attrition logic|Attrition is initially modelled at aggregate population level unless segmentation is evidenced and approved.|Aggregate attrition rule|Segment by grade / job family / Early Careers if data supports|Prevents overfitting weak evidence in first proof of concept|Data readiness and method note|Requester / Customer Owner|Proposed|M|FR-006, FR-016, NFR-007, R-007|[DD/MM/YYYY]|
|AS-105|Attrition logic|Attrition assumptions must be tested through scenario comparison rather than presented as a single “true” forecast.|Scenario comparison mandatory|None|Stakeholders are expected to debate attrition heavily|Interview outcome|Requester / Customer Owner|Accepted|H|ART-002, AC-006, R-005, NFR-007|[DD/MM/YYYY]|
|AS-106|Attrition logic|Joiners and leavers are not assumed to be behaviourally identical across all age / grade groups unless explicitly evidenced.|No behavioural equivalence assumed|Optional segmented scenarios|Avoids hidden bias in model interpretation|Method governance decision|Engineering Director Owner|Proposed|M|NFR-007, R-001, R-005|[DD/MM/YYYY]|

---

**C. Retirement proxy logic assumptions**

__

|   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|
|Assumption ID|Section|Assumption statement|Base-case value / rule|Allowed alternatives / scenario values|Rationale|Evidence / source|Owner|Status|Sensitivity|Related Stable IDs|Review date|
|AS-201|Retirement proxy|Retirement is modelled as a proxy rule, not as a factual prediction of individual behaviour.|Proxy-based logic only|None|No hard retirement rule is currently available|Interview outcome|Engineering Director Owner|Accepted|H|FR-019, NFR-007, R-006, DEP-015|[DD/MM/YYYY]|
|AS-202|Retirement proxy|Threshold age above which retirement probability may begin to apply.|[TBC age]|Alternative threshold ages in sensitivity scenarios|Creates controllable entry point to oldest-cohort exit assumption|Assumption to be set by owners|Requester / Customer Owner|Proposed|H|FR-013, FR-019, AC-009, DEP-015|[DD/MM/YYYY]|
|AS-203|Retirement proxy|Annual probability of retirement for individuals at or above the threshold age.|[TBC % per year]|Low / Base / High retirement-proxy rates|Allows gradual exits rather than cliff-edge removal|Scenario-based proxy rule|Requester / Customer Owner|Proposed|H|FR-013, FR-019, AC-009, R-006|[DD/MM/YYYY]|
|AS-204|Retirement proxy|Optional natural upper-age cut-off if data shows effectively no service beyond a specific age.|None unless evidenced|Fixed maximum age if supported by data|Useful if a natural cut-off clearly emerges from current population profile|Headcount profile review|Requester / Customer Owner|Proposed|M|FR-019, DEP-015, R-006|[DD/MM/YYYY]|
|AS-205|Retirement proxy|Optional maximum dwell period in the oldest age band, after which exit probability becomes 100%.|None unless approved|Dwell-time rule by oldest age band|Provides a softer alternative to fixed-age cut-off|Prototype design option|Engineering Director Owner|Proposed|M|FR-019, R-006|[DD/MM/YYYY]|
|AS-206|Retirement proxy|Retirement proxy exits must not double-count attrition exits in the same simulation year.|Mutually exclusive exit treatment|Sequenced or reconciled exit logic|Prevents overstating total workforce loss|Model design control|Requester / Customer Owner|Proposed|H|FR-002, FR-019, AC-009, NFR-002|[DD/MM/YYYY]|
|AS-207|Retirement proxy|Retirement logic is a sensitivity-tested assumption, not a prerequisite for a valid first proof of concept.|Sensitivity-tested|None|Prevents Red dependency from blocking prototype value|Interview outcome|Engineering Director Owner|Accepted|M|R-006, DEP-015, NFR-007|[DD/MM/YYYY]|

---

**D. WEI weighting and reference-profile assumptions**

__

|   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|
|Assumption ID|Section|Assumption statement|Base-case value / rule|Allowed alternatives / scenario values|Rationale|Evidence / source|Owner|Status|Sensitivity|Related Stable IDs|Review date|
|AS-301|WEI method|Primary tipping-point measure is Weighted Experience Index (WEI) decline.|WEI used as primary analytical measure|Secondary views may supplement, not replace|Main analytical frame agreed in interview|Interview outcome|Engineering Director Owner|Accepted|H|CTX-009, FR-008, AC-004|[DD/MM/YYYY]|
|AS-302|WEI method|Preferred WEI method compares projected future states against the current “as is” workforce reference profile.|Reference-profile method|Expert-weighted fallback if reference profile is not fully supportable|Shows direction and magnitude of change relative to today|Interview outcome|Engineering Director Owner|Accepted|H|CTX-013, FR-017, AC-010|[DD/MM/YYYY]|
|AS-303|WEI method|Minimum acceptable fallback is an expert-weighted WEI with transparent assumptions.|Expert-weighted fallback permitted|None|Ensures prototype remains deliverable if reference-profile design is incomplete|Interview outcome|Engineering Director Owner|Accepted|H|CTX-014, FR-018, AC-011|[DD/MM/YYYY]|
|AS-304|WEI components|WEI is built from age band, service length, job family, and grade.|Four-component index|Temporary degraded version if one field is weak, with caveat|Reflects agreed experience proxy|Agreed interview output|Engineering Director Owner|Proposed|H|CTX-005, FR-007, FR-008, R-007|[DD/MM/YYYY]|
|AS-305|WEI weighting|Component weights used in the WEI.|[TBC weighting set]|Equal-weight sensitivity / expert-weight sensitivity|Weight choice materially affects interpretation|Method note + stakeholder judgement|Engineering Director Owner|Proposed|H|FR-008, FR-018, ART-004, R-001|[DD/MM/YYYY]|
|AS-306|WEI normalisation|Reference-profile baseline index value.|100 = current reference profile|Alternative normalisation if explicitly justified|Makes trend easier to interpret over time|Method design choice|Engineering Director Owner|Proposed|M|FR-017, AC-010, NFR-005|[DD/MM/YYYY]|
|AS-307|WEI threshold|Definition of “material decline” or tipping point in the WEI.|[TBC threshold / rule]|Absolute drop / relative drop / multi-year decline rule|Needed to convert trend into decision signal|Method governance decision|Engineering Director Owner|Proposed|H|AC-004, R-001, NFR-008|[DD/MM/YYYY]|
|AS-308|WEI reference population|Definition of the reference profile population.|Current full P&A workforce unless otherwise approved|Experienced-core reference subgroup if explicitly approved|Avoids ambiguity about what “as is” means|Baseline definition + method approval|Engineering Director Owner|Proposed|H|CTX-013, FR-017, R-001|[DD/MM/YYYY]|
|AS-309|Secondary presentation lenses|Simple cohort crossover and capability-risk views may be used as supporting visuals for simplified discussion.|Include at least one secondary lens|Include both if useful|Allows proportionate communication without stronger claims than evidence supports|Interview outcome|Engineering Director Owner|Accepted|M|CTX-010, FR-009, AC-005, NFR-007|[DD/MM/YYYY]|

---

**E. Scenario preset assumptions**

__

|   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|
|Assumption ID|Section|Assumption statement|Base-case value / rule|Allowed alternatives / scenario values|Rationale|Evidence / source|Owner|Status|Sensitivity|Related Stable IDs|Review date|
|AS-401|Scenario presets|Base-case scenario uses agreed intake, attrition, reference profile, and retirement-proxy assumptions.|Base case|None|Anchor for all comparison|Approved assumptions register|Requester / Customer Owner|Proposed|H|FR-011, AC-007|[DD/MM/YYYY]|
|AS-402|Scenario presets|High-attrition scenario is included in the minimum scenario set.|Included|Low-attrition scenario optional|Attrition is the main credibility challenge|Interview outcome|Requester / Customer Owner|Accepted|H|FR-012, AC-007, ART-002, R-005|[DD/MM/YYYY]|
|AS-403|Scenario presets|High Early Careers intake scenario is included in the minimum scenario set.|Included|Low-intake scenario optional|Important for stress-testing demographic shift|Interview outcome|Requester / Customer Owner|Accepted|H|FR-005, FR-012, AC-007|[DD/MM/YYYY]|
|AS-404|Scenario presets|Projection horizon is scenario-controlled.|[TBC years]|5 / 10 / 15 years or approved alternatives|Time horizon changes tipping-point interpretation|Scenario design choice|Requester / Customer Owner|Proposed|M|FR-014, AC-001, AC-009|[DD/MM/YYYY]|
|AS-405|Scenario presets|Grade progression / promotion assumptions are scenario-controlled where enabled.|[TBC rule]|No progression / baseline / accelerated progression|Promotion dynamics may affect capability interpretation|Interview outcome|Requester / Customer Owner|Proposed|M|FR-015, AC-009|[DD/MM/YYYY]|
|AS-406|Scenario presets|Apprentice and graduate populations may be pooled in base case unless separation is required for fidelity.|Pooled unless approved otherwise|Separate apprentice / graduate treatment|Supports pragmatic proof of concept without blocking nuance later|Data readiness and delivery posture|Requester / Customer Owner|Proposed|M|FR-004, DEP-014, R-002|[DD/MM/YYYY]|

---

**F. Data quality, evidence, and caveat assumptions**

__

|   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|
|Assumption ID|Section|Assumption statement|Base-case value / rule|Allowed alternatives / scenario values|Rationale|Evidence / source|Owner|Status|Sensitivity|Related Stable IDs|Review date|
|AS-501|Data readiness|Latest approved P&A headcount baseline is considered fit for prototype use.|Fit for use|None unless baseline changes|Green dependency|Workday AP report extract|Requester / Customer Owner|Accepted|H|DEP-001|[DD/MM/YYYY]|
|AS-502|Data readiness|2024/25 attrition extract is sufficient for prototype use but remains challenge-prone.|Usable with caveat|Replace if a better extract becomes available|Amber dependency and likely debate area|Attrition extract review|Requester / Customer Owner|Proposed|H|DEP-002, R-005|[DD/MM/YYYY]|
|AS-503|Data readiness|Service length field is usable for prototype, subject to validation and caveat if needed.|Use with caveat if required|Exclude or proxy if validation fails|Amber dependency affecting experience fidelity|Field validation|Requester / Customer Owner|Proposed|M|DEP-011, R-007|[DD/MM/YYYY]|
|AS-504|Data readiness|Job family field is considered fit for use.|Use as-is|None|Green dependency|Field extract review|Requester / Customer Owner|Accepted|M|DEP-012|[DD/MM/YYYY]|
|AS-505|Data readiness|Grade field is considered fit for use.|Use as-is|None|Green dependency|Field extract review|Requester / Customer Owner|Accepted|M|DEP-013|[DD/MM/YYYY]|
|AS-506|Data readiness|Early Careers identification is usable for prototype, but separation of sub-types may be partial.|Use with caveat|Pool categories if needed|Amber dependency affecting subgroup fidelity|Workday tagging / extract review|Requester / Customer Owner|Proposed|M|DEP-014, R-002, R-007|[DD/MM/YYYY]|
|AS-507|Evidence posture|Claims in reporting remain proportionate to the evidence and scenario-based nature of the model.|No causal claims|Stronger claims only if separately evidenced|Prevents overreach in politically sensitive output|Governance decision|Engineering Director Owner|Accepted|H|NFR-007, GOV-004, R-003|[DD/MM/YYYY]|

---

**G. Output and sign-off assumptions**

__

|   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|
|Assumption ID|Section|Assumption statement|Base-case value / rule|Allowed alternatives / scenario values|Rationale|Evidence / source|Owner|Status|Sensitivity|Related Stable IDs|Review date|
|AS-601|Sign-off|Wider sharing requires both method credibility and data credibility.|Method + data credibility gate|None|Agreed sign-off threshold|Interview outcome|Engineering Director Owner|Accepted|H|GOV-004, NFR-008, AC-012|[DD/MM/YYYY]|
|AS-602|Artefacts|Assumptions register and scenario comparison table are the two mandatory artefacts for “done”.|Both must exist|None|These are essential to challengeability|Interview outcome|Requester / Customer Owner|Accepted|H|ART-001, ART-002, AC-006|[DD/MM/YYYY]|
|AS-603|Artefacts|Decision-support report / slide pack, WEI method note, caveats note, and restricted leadership narrative are desirable for first proof of concept.|Should-have artefacts|Can phase if needed|Supports adoption and controlled review|Interview outcome|Requester / Customer Owner|Accepted|M|ART-003, ART-004, ART-005, ART-006|[DD/MM/YYYY]|

---

**5) Change log**

__

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|Change ID|Date|Changed by|Description of change|Impacted Assumption IDs|Impacted Stable IDs|
|CHG-001|[DD/MM/YYYY]|[Name / role]|Initial register creation|AS-001 to AS-603|FR-001 to FR-019, AC-001 to AC-012, NFR-001 to NFR-008, DEP-001 to DEP-015, R-001 to R-007, ART-001 to ART-008|

---

**6) Approval block**

__

|   |   |   |   |   |
|---|---|---|---|---|
|Role|Name / descriptor|Decision|Date|Notes|
|Requester / Customer Owner|[Role only]|Approve / Reject / Amend|[DD/MM/YYYY]||
|Engineering Director Owner|[Role only]|Approve / Reject / Amend|[DD/MM/YYYY]||
|Data reviewer (optional)|[Role only]|Approve / Reject / Amend|[DD/MM/YYYY]||

---

**7) Recommended immediate fill order**

If you want to get this usable quickly, fill in these first:

1. AS-101 to AS-105 — attrition logic
2. AS-201 to AS-206 — retirement proxy logic
3. AS-301 to AS-308 — WEI design and tipping-point rule
4. AS-401 to AS-405 — scenario presets
5. AS-601 to AS-603 — sign-off and artefact expectations

That sequence surfaces the contested assumptions first.

---