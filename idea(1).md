# People’s Priorities — MVP idea.md

## 0. Working title

**People’s Priorities**

## 1. Product thesis

People’s Priorities is a **constituency intelligence platform** for elected representatives and their offices.

It helps citizens submit local issues through a natural conversation, then turns those conversations into structured, location-mapped, evidence-backed issue clusters. These clusters become ranked development priorities for the MP office.

The MP and staff can then interact with the constituency knowledge base conversationally:

- “What are the top issues this week?”
- “Which areas have the most water complaints?”
- “What issues are affecting elderly citizens?”
- “Why is this issue ranked first?”
- “Generate a report for tomorrow’s review.”
- “What should my team verify first?”

The platform does not replace official grievance systems. It acts as a **listening, prioritization, guidance, and planning layer**.

---

## 2. One-line pitch

A conversational constituency intelligence platform that turns scattered citizen complaints into ranked, evidence-backed development priorities while guiding citizens to relevant schemes, services, and complaint channels.

---

## 3. Product category

This should not be positioned as only an AI complaint chatbot.

Better category:

```text
Constituency intelligence system
```

Or:

```text
AI-powered public issue intelligence platform for elected representatives
```

Or:

```text
Citizen input → constituency priority engine
```

The chatbot is only the interface. The real product is the structured knowledge base, issue clustering, prioritization, and reports.

---

## 4. Why this should exist

### 4.1 Citizen problem

Citizens often know their pain point but not the right path to solve it.

Examples:

- “My pension has not come.”
- “Water has not come for five days.”
- “The road near the school is broken.”
- “Drainage water is overflowing.”
- “Streetlights are not working.”
- “I may be eligible for a scheme but do not know how to apply.”
- “I do not know whether this is a local body, state department, central grievance, or MP office matter.”

Current citizen reality:

- They complain through WhatsApp, phone calls, letters, public meetings, social media, and local workers.
- They do not know which department or scheme applies.
- They may not know the official complaint channel.
- They rarely receive a clear explanation of what was understood.
- They often feel their issue went into a black hole.
- Repeated issues from many citizens are not visible as a collective pattern.

### 4.2 MP office problem

MPs and their teams receive large volumes of unstructured public input, but they lack a clean system to convert it into actionable priorities.

Current MP office reality:

- Complaints come from too many channels.
- Staff manually remember, forward, or track issues.
- Similar complaints are not grouped.
- The MP sees noise instead of patterns.
- It is difficult to know which issue affects the most people.
- Reports for meetings and field visits are prepared manually.
- Location-wise impact is hard to visualize.
- Scheme/service awareness gaps are not systematically identified.
- No conversational layer exists over the constituency’s issue memory.

### 4.3 Core opportunity

Current systems mostly stop at:

```text
Complaint → record → forward → status
```

This product should go further:

```text
Citizen issue
→ structured submission
→ location mapping
→ similar issue clustering
→ priority scoring
→ citizen guidance
→ MP intelligence
→ staff action
→ public update
```

---

## 5. Main product decision

The platform must be **two-sided and conversational**.

### Side 1: Citizen-facing conversational intake

Citizens report issues naturally, in their own language.

The agent should:

- Understand the issue.
- Ask only necessary missing questions.
- Capture location.
- Structure the complaint.
- Save the issue.
- Attach it to a similar cluster if one exists.
- Give immediate guidance.
- Return a tracking ID.

### Side 2: MP-facing conversational intelligence

The MP and staff ask questions over the knowledge base.

The agent should:

- Search issue clusters.
- Rank priorities.
- Explain why an issue matters.
- Compare locations.
- Show trends.
- Generate reports.
- Suggest action plans.
- Surface citizen guidance gaps.

---

## 6. Product owner framing

The strongest first product is not:

```text
Public complaint chatbot
```

The stronger first product is:

```text
MP Office Issue Intelligence + Weekly Priority Brief
```

Why:

- The MP office already receives citizen issues.
- Staff already struggle with organizing them.
- This gives immediate value even before a public launch.
- It avoids dependence on large citizen adoption on day one.
- It allows controlled testing and verification.
- It produces a clear output: a weekly report.

### First real product wedge

The first wedge should be:

```text
Upload or enter messy citizen complaints → get ranked issue clusters and a weekly MP brief.
```

This is the demo wow moment:

```text
100 messy complaints become 12 issue clusters and a ranked top 5 priority list.
```

---

## 7. MVP goal

The MVP should prove this loop:

```text
Citizen/staff enters issue
→ AI structures it
→ location is resolved
→ similar issues are clustered
→ citizen receives guidance
→ MP asks questions
→ system returns ranked priorities and evidence
→ report is generated
```

### MVP success statement

An MP office should be able to use the MVP to understand:

1. What issues are coming from the constituency.
2. Where those issues are concentrated.
3. Which issues are repeated.
4. Which issues are urgent.
5. Which groups or areas are most affected.
6. What citizens can do immediately.
7. What the MP office should review or escalate first.

---

## 8. MVP non-goals

The MVP should not attempt to do these:

- Replace CPGRAMS or state grievance systems.
- File official grievances automatically.
- Track live official grievance status.
- Make final scheme eligibility decisions.
- Collect Aadhaar/KYC.
- Build a full government department workflow.
- Promise issue resolution.
- Provide legal advice.
- Perform political sentiment analysis.
- Publicly expose raw citizen complaints.
- Publicly expose personal data.
- Depend on government API access.
- Require WhatsApp integration in version 1.
- Build complex analytics before the core loop works.

---

## 9. CPGRAMS and official grievance systems decision

CPGRAMS and similar official grievance systems should be treated as **guidance/reference layers**, not as the core database.

### Use official grievance systems for:

- Citizen guidance.
- Complaint channel reference.
- Department/category inspiration.
- Public grievance taxonomy.
- Benchmarking where public data exists.
- Links to official filing/tracking pages.

### Do not use official systems for:

- Private citizen complaint data.
- Live official grievance status.
- Automatic filing without authorization.
- Official complaint tracking without user/auth access.
- Constituency-level raw data unless officially available.

### Product positioning

The product should say:

```text
We help citizens understand the right path and help MP offices identify repeated local issue patterns. We do not replace official grievance redressal systems.
```

---

## 10. Target users

### 10.1 Citizen

A citizen wants to:

- Report an issue simply.
- Use their own language.
- Avoid long forms.
- Know what the system understood.
- Know what to do next.
- Receive a tracking ID.
- See whether the issue is part of a larger local pattern.

### 10.2 MP

The MP wants to:

- Understand what matters most.
- See ranked constituency priorities.
- Know where issues are concentrated.
- Get evidence-backed briefs.
- Prepare for meetings, speeches, and field visits.
- Ask natural questions instead of filtering dashboards.

### 10.3 MP office staff

Staff are the daily operators.

They want to:

- Enter complaints from calls, WhatsApp, meetings, and letters.
- Review AI-extracted fields.
- Correct category/location.
- Merge or split clusters.
- Update status.
- Generate reports.
- Prepare briefs for the MP.
- Publish safe updates.

### 10.4 Field workers or volunteers

They may:

- Submit field reports.
- Verify issue locations.
- Add photos.
- Confirm whether a cluster is real.
- Support public intake campaigns.

---

## 11. Product surfaces

### Surface 1: Citizen chat

Route idea:

```text
/citizen
```

Purpose:

A citizen submits an issue conversationally.

Capabilities:

- Text input.
- Multilingual support.
- Optional photo/audio.
- Location sharing/manual location.
- Clarifying questions.
- Tracking ID.
- Immediate guidance.

### Surface 2: Staff console

Route idea:

```text
/staff
```

Purpose:

The MP office reviews and manages the data.

Capabilities:

- Submission inbox.
- Cluster management.
- Edit category/location.
- Merge/split clusters.
- Mark verification status.
- Add internal notes.
- Update issue status.
- Generate reports.
- Create manual submissions from offline inputs.

### Surface 3: MP chat intelligence

Route idea:

```text
/mp/chat
```

Purpose:

The MP asks natural language questions over the constituency knowledge base.

Capabilities:

- Ask top priorities.
- Ask area-wise questions.
- Ask demographic/impact questions.
- Ask trend questions.
- Ask report/action questions.
- Receive evidence-backed answers.

### Surface 4: MP dashboard

Route idea:

```text
/mp/dashboard
```

Purpose:

A visual overview of constituency issues.

Capabilities:

- Top priority cards.
- Issue heatmap.
- Category breakdown.
- Area ranking.
- Trend cards.
- Issue cluster cards.
- Report generation button.

### Surface 5: Public issue view

Route idea:

```text
/public/issues
```

Purpose:

Public transparency without exposing citizen identity.

Capabilities:

- Anonymized issue clusters.
- Category filters.
- Area filters.
- Public status updates.
- Guidance links.
- No personal data.

This can be delayed until after private pilot validation.

---

## 12. MVP scope

### Must have

```text
Citizen conversational issue intake
Staff/manual issue entry
Structured issue extraction
Location resolution
Submission database
Issue clustering
Citizen guidance
Priority ranking
MP conversational question answering
Issue scene
Location scene
Weekly report generation
Basic staff review
```

### Should have

```text
Map heatmap
Photo evidence
Public cluster page
CSV upload
Basic demographic context
Status updates
```

### Could have

```text
WhatsApp intake
Voice input
SMS updates
Advanced scheme matching
Department contact management
Multi-constituency support
```

### Not now

```text
Official grievance filing
Aadhaar/KYC
Live CPGRAMS tracking
Full government workflow
Political sentiment analysis
Complex eligibility engine
```

---

## 13. Core product loops

### 13.1 Citizen guidance loop

```text
Citizen submits issue
→ system understands issue
→ citizen gets tracking ID
→ citizen gets next step
→ citizen trusts platform
→ citizen shares/uses again
```

### 13.2 Clustering loop

```text
More issues come in
→ similar issues group together
→ clusters become stronger
→ priority ranking improves
→ MP gets clearer signal
```

### 13.3 Staff verification loop

```text
AI extracts issue
→ staff corrects mistakes
→ system stores corrections
→ future classification improves
```

### 13.4 MP decision loop

```text
MP asks question
→ system gives evidence scene
→ MP chooses action
→ staff updates status
→ action history improves future reports
```

### 13.5 Public trust loop

```text
Cluster receives update
→ citizens see anonymized progress
→ trust increases
→ more citizens submit
```

---

## 14. Core user journeys

### 14.1 Citizen issue journey

```text
Citizen opens chat
→ Describes issue
→ Agent asks missing question
→ Citizen gives location
→ Agent confirms understanding
→ System creates submission
→ System attaches to cluster
→ Agent gives tracking ID
→ Agent gives guidance
```

Example:

```text
Citizen:
Water has not come in our colony for five days.

Agent:
I understand. This looks like a water supply issue. Can you tell me your area or share your location?

Citizen:
Madhurwada near old school.

Agent:
Is this affecting only your house or multiple houses nearby?

Citizen:
The whole street.

Agent:
I understood this as a water supply issue in Madhurwada affecting multiple households.

Your issue has been submitted and added to an existing water shortage cluster in the area.

Tracking ID: PP-2026-0234

You can also raise this with the local municipal water department. If the issue remains unresolved, an official public grievance channel may be relevant.
```

### 14.2 Staff manual entry journey

```text
Staff opens console
→ Adds complaint from phone call/WhatsApp/public meeting
→ AI structures complaint
→ Staff reviews fields
→ Confirms location/category
→ Submission is saved
→ Cluster is updated
```

Example:

```text
Raw note:
"Caller from Ward 8 says drainage water has been overflowing near temple for 3 days."

Structured:
Category: Drainage
Urgency: High
Location: Ward 8
Duration: 3 days
Affected area: Near temple
Cluster suggestion: Drainage overflow in Ward 8
```

### 14.3 MP priority journey

```text
MP opens chat
→ Asks top issues
→ Agent calls priority tool
→ Agent builds issue scenes
→ Agent answers with evidence
→ MP asks follow-up
```

Example:

```text
MP:
What are the top issues this week?

Agent:
The top three constituency priorities this week are:

1. Water shortage in Madhurwada
   83 submissions, high urgency, increasing trend.

2. Drainage overflow in Ward 8
   52 submissions, health risk, repeated photo evidence.

3. Old age pension delays in Mandal B
   39 submissions, mostly affecting elderly citizens.
```

### 14.4 MP report journey

```text
MP asks for report
→ Agent collects priority/location/issue scenes
→ Report is generated
→ Staff edits if needed
→ Report is exported/shared
```

---

## 15. Agent architecture

### 15.1 High-level architecture

```text
Citizen Chat
   ↓
Citizen Intake Agent
   ↓
Structured issue parser
   ↓
Real tools:
- resolve_location
- create_submission
- find_or_create_issue_cluster
- get_citizen_guidance
   ↓
Constituency Knowledge Base
   ↓
MP Intelligence Agent
   ↓
Real tools:
- search_constituency_knowledge
- get_priority_issues
- get_issue_scene
- get_location_scene
- get_map_scene
- generate_report
```

### 15.2 Citizen Intake Agent responsibilities

The citizen agent should handle:

- Language understanding.
- Translation if needed.
- Extracting issue fields.
- Asking missing questions.
- Confirming issue summary.
- Calling real tools.
- Producing citizen-safe replies.

The citizen agent should not:

- Promise resolution.
- Give final legal/scheme eligibility decisions.
- Publish citizen data.
- Guess locations without confirmation when confidence is low.

### 15.3 MP Intelligence Agent responsibilities

The MP agent should handle:

- Understanding MP questions.
- Planning which scenes/tools are needed.
- Calling knowledge tools.
- Answering with evidence.
- Explaining uncertainty.
- Generating reports/action plans.

The MP agent should not:

- Invent numbers.
- Make claims without retrieved data.
- Reveal personal citizen data.
- Treat unverified AI outputs as confirmed facts.

---

## 16. Structured output vs tools

### Important product/engineering rule

Not everything should be a tool.

### Structured output should handle:

```text
Language detection
Translation
Issue extraction
Category prediction
Urgency interpretation
Missing-field reasoning
MP query planning
Natural language response
```

### Real tools should handle:

```text
Database writes
Location resolution
Issue clustering
Search
Priority scoring
Scene generation
Map data
Reports
Status updates
Guidance retrieval
Audit logging
```

### Rule

```text
LLM = understands messy language
Tool = touches real data, real logic, or real actions
```

---

## 17. Real tools to build

### Tool 1: `resolve_location`

#### Power function

```text
Messy place → structured geography
```

#### Purpose

Convert a citizen-provided place, landmark, pincode, GPS point, ward, village, or locality into a structured location object.

#### Used by

- Citizen Agent
- Staff Console
- MP Agent

#### Input

```json
{
  "location_text": "Madhurwada near old school",
  "gps": {
    "lat": 17.82,
    "lng": 83.35
  },
  "pincode": null,
  "state_hint": "Andhra Pradesh",
  "district_hint": "Visakhapatnam"
}
```

#### Output

```json
{
  "location_id": "LOC_123",
  "name": "Madhurwada",
  "type": "locality",
  "district": "Visakhapatnam",
  "state": "Andhra Pradesh",
  "lat": 17.82,
  "lng": 83.35,
  "confidence": 0.82,
  "needs_confirmation": true
}
```

#### Why it matters

The agent should not guess locations. Structured location IDs are necessary for maps, clustering, ranking, and area-wise insights.

---

### Tool 2: `create_submission`

#### Power function

```text
Conversation → saved complaint record
```

#### Purpose

Save a structured citizen issue into the database.

#### Used by

- Citizen Agent
- Staff Console

#### Input

```json
{
  "citizen_id": "anonymous",
  "conversation_id": "CONV_001",
  "source": "citizen_chat",
  "original_text": "మా ఏరియాలో నీళ్లు రావడం లేదు",
  "translated_text": "Water is not coming in our area",
  "language": "Telugu",
  "issue_summary": "No water supply in the area",
  "category": "Water",
  "secondary_category": "Water Supply Disruption",
  "urgency": "High",
  "location_id": "LOC_123",
  "evidence_urls": []
}
```

#### Output

```json
{
  "submission_id": "SUB_001",
  "tracking_id": "PP-2026-001",
  "status": "submitted"
}
```

#### Why it matters

This turns chat into durable issue data.

---

### Tool 3: `find_or_create_issue_cluster`

#### Power function

```text
Individual complaints → collective constituency issue
```

#### Purpose

Search existing issue clusters and either attach the new submission to a matching cluster or create a new cluster.

#### Used by

- Citizen Agent
- Staff Console

#### Input

```json
{
  "submission_id": "SUB_001",
  "category": "Water",
  "secondary_category": "Water Supply Disruption",
  "issue_summary": "No water supply in the area",
  "location_id": "LOC_123",
  "radius_km": 3,
  "time_window_days": 30
}
```

#### Output

```json
{
  "cluster_id": "CL_102",
  "cluster_action": "attached_to_existing",
  "cluster_title": "Water shortage in Madhurwada",
  "similarity_score": 0.89,
  "existing_submission_count": 47
}
```

#### Why it matters

This is the heart of the product. It transforms scattered complaints into issue intelligence.

---

### Tool 4: `get_citizen_guidance`

#### Power function

```text
Complaint → immediate next step for citizen
```

#### Purpose

Find relevant schemes, services, departments, complaint channels, helplines, or local actions.

#### Used by

- Citizen Agent
- Staff Console

#### Input

```json
{
  "category": "Water",
  "secondary_category": "Water Supply Disruption",
  "issue_summary": "No water supply in Madhurwada",
  "location_id": "LOC_123",
  "citizen_profile": {
    "age": null,
    "occupation": null,
    "income_group": null
  }
}
```

#### Output

```json
{
  "guidance": [
    {
      "type": "complaint_channel",
      "name": "Local municipal water department",
      "reason": "Water supply issues are usually handled locally.",
      "url": null,
      "confidence": 0.78
    },
    {
      "type": "grievance_portal",
      "name": "Official public grievance channel",
      "reason": "Useful if local resolution does not happen.",
      "url": "official_url",
      "confidence": 0.72
    }
  ],
  "disclaimer": "Verify final process on the official source."
}
```

#### Why it matters

The citizen gets value immediately. The platform is not just collecting complaints.

---

### Tool 5: `search_constituency_knowledge`

#### Power function

```text
MP question → relevant knowledge retrieval
```

#### Purpose

Search across submissions, clusters, locations, guidance resources, actions, and reports.

#### Used by

- MP Agent

#### Input

```json
{
  "query": "pension problems affecting elderly citizens",
  "filters": {
    "category": "Pension",
    "date_range": "last_30_days",
    "location_id": null,
    "urgency": null
  },
  "limit": 10
}
```

#### Output

```json
{
  "results": [
    {
      "type": "issue_cluster",
      "cluster_id": "CL_211",
      "title": "Old age pension delays",
      "submission_count": 39,
      "priority_score": 76,
      "location": "Mandal B"
    }
  ]
}
```

#### Why it matters

This gives the MP agent real retrieval capability over constituency memory.

---

### Tool 6: `get_priority_issues`

#### Power function

```text
Issue clusters → ranked MP priorities
```

#### Purpose

Return top-ranked issue clusters based on priority score.

#### Used by

- MP Agent
- Dashboard

#### Input

```json
{
  "area_id": "CONST_001",
  "date_range": {
    "from": "2026-06-27",
    "to": "2026-07-04"
  },
  "limit": 10,
  "category": null
}
```

#### Output

```json
{
  "priorities": [
    {
      "rank": 1,
      "cluster_id": "CL_102",
      "title": "Water shortage in Madhurwada",
      "category": "Water",
      "location": "Madhurwada",
      "submission_count": 83,
      "unique_citizen_count": 51,
      "urgency": "High",
      "priority_score": 91,
      "reason": "High volume, essential service issue, increasing trend."
    }
  ]
}
```

#### Why it matters

This is the MP’s clearest value: what needs attention first.

---

### Tool 7: `get_issue_scene`

#### Power function

```text
Cluster ID → evidence-based decision scene
```

#### Purpose

Build a complete context packet for one issue cluster.

#### Used by

- MP Agent
- Dashboard
- Report Generator

#### Input

```json
{
  "cluster_id": "CL_102",
  "include": [
    "summary",
    "metrics",
    "evidence",
    "trend",
    "demographics",
    "recommended_actions"
  ]
}
```

#### Output

```json
{
  "scene_type": "issue_scene",
  "cluster_id": "CL_102",
  "title": "Water shortage in Madhurwada",
  "summary": "Citizens report no water supply for 5–7 days.",
  "category": "Water",
  "location": {
    "name": "Madhurwada",
    "district": "Visakhapatnam"
  },
  "metrics": {
    "submissions": 83,
    "unique_citizens": 51,
    "photos": 27,
    "priority_score": 91
  },
  "trend": {
    "direction": "increasing",
    "change_percent": 38
  },
  "affected_groups": [
    "households",
    "elderly citizens",
    "school children"
  ],
  "recommended_actions": [
    "Forward to relevant local department",
    "Run field verification",
    "Send public advisory"
  ],
  "verification": {
    "status": "unverified",
    "staff_review_required": true
  }
}
```

#### Why it matters

The MP agent should answer from scenes, not raw rows.

---

### Tool 8: `get_location_scene`

#### Power function

```text
Location → area intelligence brief
```

#### Purpose

Return a complete view of what is happening in one area.

#### Used by

- MP Agent
- Dashboard
- Report Generator

#### Input

```json
{
  "location_id": "LOC_123",
  "date_range": {
    "from": "2026-06-04",
    "to": "2026-07-04"
  }
}
```

#### Output

```json
{
  "scene_type": "location_scene",
  "location": {
    "id": "LOC_123",
    "name": "Madhurwada",
    "type": "locality"
  },
  "top_issues": [
    {
      "cluster_id": "CL_102",
      "title": "Water shortage",
      "submissions": 83,
      "priority_score": 91
    },
    {
      "cluster_id": "CL_117",
      "title": "Road damage",
      "submissions": 34,
      "priority_score": 72
    }
  ],
  "demographic_context": {
    "population_estimate": 18000,
    "households": 4200,
    "source": "open public dataset",
    "limitations": "Baseline estimate, not real-time population."
  }
}
```

#### Why it matters

MPs think in terms of areas, wards, villages, and mandals.

---

### Tool 9: `get_map_scene`

#### Power function

```text
Issue data → map-ready hotspot layer
```

#### Purpose

Return map-ready points, clusters, heatmap weights, and labels.

#### Used by

- MP Agent
- Dashboard
- Public Issue Map

#### Input

```json
{
  "category": "Water",
  "date_range": {
    "from": "2026-06-04",
    "to": "2026-07-04"
  },
  "map_type": "heatmap",
  "area_id": "CONST_001"
}
```

#### Output

```json
{
  "scene_type": "map_scene",
  "map_type": "heatmap",
  "points": [
    {
      "lat": 17.82,
      "lng": 83.35,
      "weight": 83,
      "label": "Water shortage cluster",
      "cluster_id": "CL_102"
    }
  ]
}
```

#### Why it matters

Maps make issue concentration visible.

---

### Tool 10: `generate_report`

#### Power function

```text
Scenes → reusable planning/report artifact
```

#### Purpose

Generate an MP-ready report from priority, issue, location, and trend scenes.

#### Used by

- MP Agent
- Staff Console

#### Input

```json
{
  "report_type": "weekly_priority_report",
  "area_id": "CONST_001",
  "date_range": {
    "from": "2026-06-27",
    "to": "2026-07-04"
  },
  "format": "markdown"
}
```

#### Output

```json
{
  "report_id": "REP_001",
  "title": "Weekly Constituency Priority Report",
  "sections": [
    {
      "heading": "Top Priorities",
      "content": "Water shortage, drainage overflow, and pension delays are the top issues this week."
    },
    {
      "heading": "Hotspots",
      "content": "Madhurwada has the highest water-related submissions."
    },
    {
      "heading": "Recommended Actions",
      "content": "Verify water shortage cluster, prepare department note, and run pension support desk."
    }
  ],
  "source_cluster_ids": [
    "CL_102",
    "CL_211"
  ]
}
```

#### Why it matters

Reports are sticky outputs. MPs and staff can use them in real workflows.

---

### Tool 11: `update_issue_status`

#### Power function

```text
Insight → tracked action state
```

#### Purpose

Update the status of an issue cluster.

#### Used by

- Staff Console
- MP Agent with permission

#### Input

```json
{
  "cluster_id": "CL_102",
  "status": "forwarded",
  "note": "Forwarded to the relevant local department for review.",
  "updated_by": "STAFF_001"
}
```

#### Output

```json
{
  "updated": true,
  "cluster_id": "CL_102",
  "new_status": "forwarded"
}
```

#### Why it matters

The product should not stop at insights. It should track whether something happened.

---

### Tool 12: `publish_public_update`

#### Power function

```text
Internal action → safe citizen-facing update
```

#### Purpose

Publish an anonymized update to the public issue cluster page.

#### Used by

- Staff Console

#### Input

```json
{
  "cluster_id": "CL_102",
  "message": "The water supply issue has been forwarded for review.",
  "visibility": "public",
  "approved_by": "STAFF_001"
}
```

#### Output

```json
{
  "published": true,
  "update_id": "UPD_001",
  "visible_to_citizens": true
}
```

#### Why it matters

This closes the public trust loop.

---

## 18. Internal structured output schemas

These are not tools. These are LLM output contracts.

### 18.1 Citizen issue parser

```json
{
  "language": "Telugu",
  "original_text": "string",
  "translated_text": "string",
  "issue_summary": "string",
  "category": "Water",
  "secondary_category": "Water Supply Disruption",
  "urgency": "High",
  "duration": "5 days",
  "affected_people": "multiple households",
  "location_text": "Madhurwada near old school",
  "evidence_mentions": [],
  "missing_fields": ["location confirmation"],
  "sensitive_flags": []
}
```

### 18.2 Citizen response planner

```json
{
  "should_ask_followup": true,
  "next_question": "Can you tell me your area or share your location?",
  "ready_to_create_submission": false
}
```

### 18.3 MP query planner

```json
{
  "query_type": "priority_summary",
  "required_tools": [
    "get_priority_issues",
    "get_issue_scene"
  ],
  "filters": {
    "date_range": "last_7_days",
    "location_id": null,
    "category": null
  }
}
```

### 18.4 Answer grounding schema

```json
{
  "answer": "string",
  "data_used": ["CL_102", "CL_211"],
  "confidence": "high | medium | low",
  "limitations": ["Some issue clusters are not staff verified yet."],
  "suggested_followups": [
    "Show map",
    "Generate report",
    "Create action plan"
  ]
}
```

---

## 19. Priority scoring

### 19.1 Purpose

Convert issue clusters into ranked priorities.

The score should be explainable to MP staff.

### 19.2 MVP formula

```text
Priority Score =
submission_volume_score * 0.25
+ urgency_score * 0.25
+ affected_population_score * 0.20
+ vulnerable_group_score * 0.15
+ recency_trend_score * 0.10
+ evidence_quality_score * 0.05
```

### 19.3 Factors

#### Submission volume score

Higher when:

- Many unique citizens report the same issue.
- Reports come from multiple nearby locations.
- Complaint count is increasing.

#### Urgency score

Higher when:

- Essential services are affected.
- Health or safety risk exists.
- The issue has lasted several days.
- The issue affects public infrastructure.

#### Affected population score

Higher when:

- The issue affects a dense locality.
- The issue impacts a school, hospital, public road, water supply, or large residential zone.
- Multiple settlements report the same problem.

#### Vulnerable group score

Higher when:

- Elderly citizens are affected.
- Students/children are affected.
- People with disabilities are affected.
- Low-income or welfare-dependent groups are affected.

#### Recency/trend score

Higher when:

- Submissions increased compared to the previous period.
- Multiple complaints arrived in the last few days.
- Issue is linked to seasonal or urgent context like rain, exams, heat, water shortage, etc.

#### Evidence quality score

Higher when:

- Photos are attached.
- Multiple unique citizens confirm it.
- Location is clear.
- Staff verification exists.
- Similar complaints are consistent.

### 19.4 Explainability requirement

Every priority score must have a short explanation.

Example:

```text
Ranked first because it has high complaint volume, affects an essential service, is increasing this week, and has multiple photo submissions from nearby locations.
```

---

## 20. Data model

### Entity: `User`

```json
{
  "id": "USER_001",
  "role": "citizen | mp | staff | admin",
  "name": "string | null",
  "phone": "string | null",
  "language_preference": "string | null",
  "created_at": "datetime"
}
```

### Entity: `Conversation`

```json
{
  "id": "CONV_001",
  "user_id": "USER_001 | null",
  "agent_type": "citizen_agent | mp_agent",
  "status": "active | closed",
  "created_at": "datetime"
}
```

### Entity: `Message`

```json
{
  "id": "MSG_001",
  "conversation_id": "CONV_001",
  "role": "user | assistant | tool",
  "content": "string",
  "created_at": "datetime"
}
```

### Entity: `Submission`

```json
{
  "id": "SUB_001",
  "tracking_id": "PP-2026-001",
  "citizen_id": "USER_001 | anonymous",
  "conversation_id": "CONV_001",
  "source": "citizen_chat | staff_entry | csv_upload | field_report",
  "original_text": "string",
  "translated_text": "string",
  "language": "Telugu",
  "summary": "No water supply in the area",
  "category": "Water",
  "secondary_category": "Water Supply Disruption",
  "urgency": "High",
  "status": "submitted | under_review | attached_to_cluster | closed",
  "location_id": "LOC_123",
  "cluster_id": "CL_102 | null",
  "created_at": "datetime"
}
```

### Entity: `IssueCluster`

```json
{
  "id": "CL_102",
  "title": "Water shortage in Madhurwada",
  "summary": "Citizens report no water supply for 5–7 days.",
  "category": "Water",
  "secondary_category": "Water Supply Disruption",
  "location_ids": ["LOC_123"],
  "submission_count": 83,
  "unique_citizen_count": 51,
  "priority_score": 91,
  "urgency": "High",
  "verification_status": "unverified | staff_verified | disputed",
  "status": "new | verified | forwarded | in_progress | resolved | closed",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Entity: `Location`

```json
{
  "id": "LOC_123",
  "name": "Madhurwada",
  "type": "locality | ward | village | mandal | constituency | district",
  "state": "Andhra Pradesh",
  "district": "Visakhapatnam",
  "parent_location_id": "LOC_PARENT",
  "lat": 17.82,
  "lng": 83.35,
  "lgd_code": "string | null"
}
```

### Entity: `Evidence`

```json
{
  "id": "EVD_001",
  "submission_id": "SUB_001",
  "type": "photo | audio | document | text",
  "url": "string",
  "visibility": "private | staff_only | public_safe",
  "created_at": "datetime"
}
```

### Entity: `GuidanceResource`

```json
{
  "id": "GUIDE_001",
  "type": "scheme | complaint_channel | department | local_service | helpline",
  "name": "Official public grievance channel",
  "category": "general_grievance",
  "location_scope": "national | state | district | local",
  "description": "string",
  "url": "string | null",
  "source": "official | curated",
  "last_verified_at": "datetime"
}
```

### Entity: `PriorityScore`

```json
{
  "id": "PS_001",
  "cluster_id": "CL_102",
  "score": 91,
  "scoring_version": "v1",
  "breakdown": {
    "submission_volume": 22,
    "urgency": 25,
    "affected_population": 18,
    "vulnerable_group_impact": 12,
    "recency_trend": 9,
    "evidence_quality": 5
  },
  "explanation": "High volume, essential service disruption, rising trend.",
  "created_at": "datetime"
}
```

### Entity: `ActionUpdate`

```json
{
  "id": "ACT_001",
  "cluster_id": "CL_102",
  "status": "forwarded",
  "note": "Forwarded to the relevant department for review.",
  "visibility": "private | public",
  "created_by": "STAFF_001",
  "created_at": "datetime"
}
```

### Entity: `Report`

```json
{
  "id": "REP_001",
  "title": "Weekly Constituency Priority Report",
  "report_type": "weekly_priority_report",
  "area_id": "CONST_001",
  "date_range": {
    "from": "2026-06-27",
    "to": "2026-07-04"
  },
  "sections": [],
  "source_cluster_ids": ["CL_102"],
  "created_at": "datetime"
}
```

### Entity: `ToolCallLog`

```json
{
  "id": "LOG_001",
  "conversation_id": "CONV_001",
  "agent_type": "citizen_agent",
  "tool_name": "resolve_location",
  "input_summary": "Madhurwada near old school",
  "output_summary": "Resolved to Madhurwada, Visakhapatnam",
  "created_at": "datetime"
}
```

---

## 21. API design

### 21.1 Citizen chat

```http
POST /api/citizen/chat
```

Purpose:

Send citizen message to the intake agent.

Request:

```json
{
  "conversation_id": "CONV_001 | null",
  "message": "Water has not come in our colony for five days",
  "language_hint": "Telugu | Hindi | English | null",
  "attachments": []
}
```

Response:

```json
{
  "conversation_id": "CONV_001",
  "reply": "Can you tell me your area or share your location?",
  "state": {
    "current_step": "need_location",
    "known_fields": {
      "category": "Water",
      "issue_summary": "No water supply for five days"
    }
  }
}
```

### 21.2 Create submission

```http
POST /api/submissions
```

Request:

```json
{
  "conversation_id": "CONV_001",
  "issue_payload": {
    "summary": "No water supply in Madhurwada",
    "category": "Water",
    "location_id": "LOC_123"
  }
}
```

Response:

```json
{
  "submission_id": "SUB_001",
  "tracking_id": "PP-2026-001",
  "cluster_id": "CL_102"
}
```

### 21.3 Citizen status

```http
GET /api/submissions/{tracking_id}
```

Response:

```json
{
  "tracking_id": "PP-2026-001",
  "status": "attached_to_cluster",
  "cluster_title": "Water shortage in Madhurwada",
  "public_updates": []
}
```

### 21.4 MP chat

```http
POST /api/mp/chat
```

Request:

```json
{
  "conversation_id": "CONV_MP_001 | null",
  "message": "What are the top issues this week?",
  "filters": {
    "area_id": "CONST_001"
  }
}
```

Response:

```json
{
  "conversation_id": "CONV_MP_001",
  "answer": "The top three issues this week are...",
  "scenes": [
    {
      "scene_type": "priority_dashboard_scene"
    }
  ],
  "suggested_followups": [
    "Show map",
    "Generate report",
    "Create action plan"
  ]
}
```

### 21.5 Top priorities

```http
GET /api/mp/priorities?area_id=CONST_001&from=2026-06-27&to=2026-07-04&limit=10
```

Response:

```json
{
  "priorities": []
}
```

### 21.6 Issue scene

```http
GET /api/mp/issues/{cluster_id}/scene
```

Response:

```json
{
  "scene_type": "issue_scene"
}
```

### 21.7 Location scene

```http
GET /api/mp/locations/{location_id}/scene
```

Response:

```json
{
  "scene_type": "location_scene"
}
```

### 21.8 Map scene

```http
GET /api/mp/map-scene?category=Water&area_id=CONST_001&from=2026-06-04&to=2026-07-04&map_type=heatmap
```

Response:

```json
{
  "scene_type": "map_scene",
  "points": []
}
```

### 21.9 Generate report

```http
POST /api/mp/reports
```

Request:

```json
{
  "report_type": "weekly_priority_report",
  "area_id": "CONST_001",
  "date_range": {
    "from": "2026-06-27",
    "to": "2026-07-04"
  }
}
```

Response:

```json
{
  "report_id": "REP_001",
  "title": "Weekly Constituency Priority Report",
  "sections": []
}
```

### 21.10 Staff review queue

```http
GET /api/staff/review-queue
```

Response:

```json
{
  "items": [
    {
      "type": "submission",
      "id": "SUB_001",
      "reason": "low_location_confidence"
    }
  ]
}
```

### 21.11 Update cluster status

```http
PATCH /api/staff/clusters/{cluster_id}/status
```

Request:

```json
{
  "status": "forwarded",
  "note": "Sent to relevant department for review."
}
```

Response:

```json
{
  "updated": true
}
```

---

## 22. Frontend details

### 22.1 Citizen chat page

Must show:

- Friendly chat interface.
- Location capture button.
- Manual location input.
- Attachment upload.
- Issue summary confirmation.
- Tracking ID card.
- Guidance card.

### 22.2 Staff console

Must show:

- Submission table.
- Cluster table.
- Review flags.
- AI extracted fields.
- Edit controls.
- Merge/split cluster action.
- Status update action.
- Report generation action.

### 22.3 MP chat dashboard

Must show:

- Chat interface.
- Suggested questions.
- Tool result cards.
- Priority cards.
- Evidence cards.
- Report cards.
- Map cards.

### 22.4 MP dashboard

Must show:

- Top 5 priority issues.
- Issue category breakdown.
- Location hotspots.
- Rising issues.
- Unverified urgent issues.
- Reports section.

### 22.5 Public issue page

Must show:

- Anonymized cluster title.
- Category.
- Area.
- Status.
- Count of reports.
- Public updates.
- Guidance link.

Must not show:

- Citizen names.
- Phone numbers.
- Raw complaint text.
- Exact home locations.
- Sensitive evidence.

---

## 23. Data strategy

### 23.1 Core data sources

The platform’s primary data should be:

1. Citizen submissions through the platform.
2. Staff-entered complaints from calls/WhatsApp/meetings.
3. Field worker reports.
4. Demo seeded data for MVP.
5. Open public datasets for location/demographic context.
6. Curated scheme/service/complaint guidance resources.

### 23.2 Open data usage

Open data can support:

- Administrative geography.
- Population baseline.
- Household baseline.
- Location hierarchy.
- Scheme metadata.
- Complaint channel metadata.
- Map visualization.

Open data should not be treated as live truth unless it is actually live and verified.

### 23.3 Guidance knowledge base

Create a curated guidance database with:

- Scheme name.
- Scheme category.
- Who it may help.
- Required documents.
- Official source link.
- Application channel.
- Related issue categories.
- Location scope.
- Last verified date.
- Disclaimer.

### 23.4 Dataset limitation rule

Every dashboard insight based on public baseline data should include limitations.

Example:

```text
Population estimate is based on public baseline data and may not reflect current live population.
```

---

## 24. Privacy, trust, and safety

### 24.1 Privacy rules

- Public pages show clusters, not individuals.
- Citizen personal data is private by default.
- Exact home location is not public.
- Evidence is staff-only unless approved.
- Sensitive issues are hidden from public view.
- Citizen identity is optional in MVP.

### 24.2 Sensitive categories

Auto-flag submissions involving:

- Violence.
- Medical emergency.
- Child safety.
- Sexual abuse.
- Self-harm.
- Criminal allegation.
- Personal documents.
- Defamation risk.
- High-risk public safety.

These should go to staff review.

### 24.3 AI trust rules

AI outputs should show:

- Confidence.
- Data used.
- Whether staff verified it.
- Source data limitations.
- When the answer is inferred.

### 24.4 Citizen expectation wording

Never say:

```text
Your issue will be solved.
```

Say:

```text
Your issue has been recorded, grouped with similar local issues, and made visible to the MP office. Here are the official or local next steps you can take.
```

---

## 25. Metrics

### 25.1 Citizen metrics

- Time to complete complaint.
- Percentage of complaints with resolved location.
- Percentage receiving useful guidance.
- Percentage receiving tracking ID.
- Repeat usage.
- Citizen satisfaction.

### 25.2 Staff metrics

- Number of submissions reviewed.
- Time saved in organizing complaints.
- Percentage of AI fields corrected.
- Number of clusters merged/split.
- Number of reports generated.

### 25.3 MP metrics

- Weekly reports generated.
- Number of MP questions answered.
- Number of priority issues identified.
- Number of area-wise insights generated.
- Number of actions created from insights.

### 25.4 AI quality metrics

- Classification accuracy.
- Location resolution accuracy.
- Cluster matching accuracy.
- Priority score acceptance rate.
- Staff correction rate.
- Hallucination rate in guidance.

### 25.5 Product impact metrics

- Duplicate complaints grouped.
- Citizen issues turned into clusters.
- High-priority issues verified.
- Public updates published.
- Citizen guidance delivered.

---

## 26. MVP pilot strategy

### 26.1 Pilot shape

Start small:

```text
1 constituency
3–5 issue categories
2–3 languages
300–500 seeded/demo submissions
1 MP office workflow
1 weekly report format
1 citizen intake link
```

### 26.2 First categories

Start with visible civic and welfare categories:

```text
Water
Roads
Drainage
Streetlights
Pensions
Health access
Education infrastructure
```

Avoid starting with highly sensitive categories like:

```text
Crime
Abuse
Corruption allegations
Political allegations
Personal disputes
```

### 26.3 First adoption motion

Start with MP office staff.

Input sources:

- Staff manual entry.
- WhatsApp copy-paste.
- Public meeting notes.
- Call notes.
- Citizen chat link.

The product should work even if public adoption is low at first.

---

## 27. Roadmap

### Phase 0: Story demo

Goal:

Prove the product narrative.

Build:

- Seeded constituency data.
- Citizen chat mock.
- MP chat mock.
- Priority ranking.
- Issue scene.
- Location scene.
- Map view.
- Weekly report.

Success:

Demo shows 100 messy complaints becoming ranked issue clusters.

### Phase 1: Internal MP office pilot

Goal:

Make it useful for staff.

Build:

- Real database.
- Staff manual entry.
- Submission review.
- Basic clustering.
- Priority dashboard.
- Weekly report.

Success:

Staff can generate a weekly brief from real or semi-real issue inputs.

### Phase 2: Controlled citizen intake

Goal:

Collect real public submissions.

Build:

- Citizen chat.
- Tracking ID.
- Location confirmation.
- Guidance engine.
- Photo upload.
- Status page.

Success:

Citizens submit real issues and receive useful guidance.

### Phase 3: MP conversational intelligence

Goal:

Make the knowledge base queryable.

Build:

- MP chat.
- Search constituency knowledge.
- Issue scenes.
- Location scenes.
- Trend scenes.
- Report generation.

Success:

MP can ask natural questions and receive evidence-backed answers.

### Phase 4: Public transparency

Goal:

Build trust.

Build:

- Public issue map.
- Anonymized cluster pages.
- Public updates.
- Staff approval workflow.

Success:

Citizens can see safe cluster-level updates.

### Phase 5: Integrations

Goal:

Improve scale and convenience.

Build:

- WhatsApp intake.
- SMS updates.
- Official grievance guidance links.
- Scheme database expansion.
- Department contact workflows.
- Multi-constituency admin.

---

## 28. MVP backlog

### Epic 1: Citizen intake

Stories:

- As a citizen, I can describe my issue in chat.
- As a citizen, I can provide location.
- As a citizen, I can upload photo evidence.
- As a citizen, I can confirm what the AI understood.
- As a citizen, I receive a tracking ID.
- As a citizen, I receive useful next-step guidance.

### Epic 2: Staff issue management

Stories:

- As staff, I can enter a complaint manually.
- As staff, I can review AI-extracted fields.
- As staff, I can edit category/location.
- As staff, I can merge similar issues.
- As staff, I can update cluster status.
- As staff, I can approve public updates.

### Epic 3: Clustering and prioritization

Stories:

- As the system, I can group similar complaints.
- As the system, I can calculate priority score.
- As the system, I can explain why an issue is ranked.
- As staff, I can override incorrect clusters.

### Epic 4: MP intelligence

Stories:

- As an MP, I can ask for top issues.
- As an MP, I can ask why an issue is important.
- As an MP, I can ask what is happening in an area.
- As an MP, I can ask for a report.
- As an MP, I can see issue evidence and trends.

### Epic 5: Reports

Stories:

- As staff, I can generate a weekly report.
- As staff, I can edit the generated report.
- As staff, I can export/share the report.
- As an MP, I can ask for a meeting brief.

### Epic 6: Public transparency

Stories:

- As a citizen, I can view public issue clusters.
- As a citizen, I can see status updates.
- As staff, I can publish safe updates.
- As staff, I can keep sensitive issues hidden.

---

## 29. Demo dataset

Seed 300–500 sample submissions.

### Example clusters

```json
[
  {
    "title": "Water shortage in Madhurwada",
    "category": "Water",
    "submissions": 83,
    "unique_citizens": 51,
    "priority_score": 91,
    "trend": "increasing"
  },
  {
    "title": "Drainage overflow in Ward 8",
    "category": "Drainage",
    "submissions": 52,
    "unique_citizens": 37,
    "priority_score": 84,
    "trend": "stable"
  },
  {
    "title": "Old age pension delays in Mandal B",
    "category": "Pension",
    "submissions": 39,
    "unique_citizens": 34,
    "priority_score": 76,
    "trend": "increasing"
  },
  {
    "title": "Road damage near school zone",
    "category": "Roads",
    "submissions": 44,
    "unique_citizens": 29,
    "priority_score": 78,
    "trend": "increasing"
  }
]
```

---

## 30. Demo script

### Step 1: Citizen submits issue

```text
Citizen:
Water has not come in our colony for five days.
```

Agent:

```text
I understand. This looks like a water supply issue. Can you tell me your area or share your location?
```

Citizen:

```text
Madhurwada near old school.
```

Agent:

```text
I understood this as a water supply issue in Madhurwada affecting multiple households.

Your issue has been submitted and added to an existing water shortage cluster in the area.

Tracking ID: PP-2026-0234

You can also raise this with the local municipal water department. If the issue remains unresolved, an official public grievance channel may be relevant.
```

### Step 2: MP asks top issues

```text
MP:
What are the top issues this week?
```

Agent:

```text
The top three constituency priorities this week are:

1. Water shortage in Madhurwada
   83 submissions, high urgency, increasing trend.

2. Drainage overflow in Ward 8
   52 submissions, health risk, repeated photo evidence.

3. Old age pension delays in Mandal B
   39 submissions, mainly affecting elderly citizens.
```

### Step 3: MP asks why

```text
MP:
Why is water shortage ranked first?
```

Agent:

```text
It is ranked first because it has the highest combination of submission volume, urgency, affected population, and recent growth.

Evidence:
- 83 submissions
- 51 unique citizens
- 27 photos
- Reports from 6 nearby locations
- Increasing by 38% compared with the previous period
```

### Step 4: MP asks for report

```text
MP:
Generate a report for tomorrow's review.
```

Agent generates:

```text
Weekly Constituency Priority Report

Sections:
1. Top priorities
2. Location hotspots
3. Evidence summary
4. Recommended actions
5. Source issue clusters
```

---

## 31. Risks and product responses

| Risk | Why it matters | Response |
|---|---|---|
| Low citizen adoption | Weak data | Start with staff/manual uploads |
| Fake/spam complaints | Bad priorities | Rate limits, duplicate detection, staff review |
| AI misclassification | Trust loss | Confidence thresholds and review queue |
| Political sensitivity | Public controversy | Private-first pilot, anonymized public clusters |
| No government integration | Action may be limited | Position as intelligence/guidance, not official redressal |
| Stale demographic data | Wrong impact claims | Show data source and limitations |
| MP does not use daily | Low stickiness | Weekly brief and staff workflow |
| Citizens expect resolution | Disappointment | Clear expectation wording |
| Overbuilt agent | Slow MVP | Build scenes and core tools first |

---

## 32. Key product principles

### Principle 1: Do not build only a chatbot

The chatbot is the interface. The product is the issue intelligence system.

### Principle 2: Group before ranking

Ranking individual complaints is weak. Ranking issue clusters is powerful.

### Principle 3: Show evidence

Every major MP answer should include evidence:

- submission count
- unique citizens
- locations
- trend
- photos/evidence
- verification status

### Principle 4: Be honest with citizens

Never promise resolution. Promise recording, grouping, visibility, and guidance.

### Principle 5: Staff review is part of the product

Human verification is not a failure. It is how the system becomes trustworthy.

### Principle 6: Start private, then public

Start with MP office/staff dashboard. Open public cluster view after trust and moderation are ready.

### Principle 7: Scenes over raw rows

MP answers should be built from reusable scenes.

---

## 33. Final MVP decision

The MVP should focus on this exact loop:

```text
Citizen/staff enters issue
→ AI structures it
→ location is resolved
→ issue is saved
→ similar issues are clustered
→ citizen gets guidance
→ MP asks questions
→ system returns ranked priorities and scenes
→ report is generated
```

This is the smallest version that proves the product.

---

## 34. Final product statement

People’s Priorities is a constituency intelligence platform for elected representatives and their offices.

It collects citizen issues through conversation, converts them into structured and location-mapped submissions, groups similar complaints into issue clusters, ranks them by urgency and impact, guides citizens to relevant services or complaint channels, and lets MPs interact with the constituency knowledge base through a conversational interface.

The MVP starts as:

```text
MP Office Issue Intelligence + Weekly Priority Brief
```

It expands into:

```text
Public conversational issue intake + citizen guidance
```

It matures into:

```text
Full constituency intelligence and action-tracking platform
```
