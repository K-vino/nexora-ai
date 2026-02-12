

# NEXORA AI – Explainable Decision Intelligence

## Design System

**Colors:**
- Primary Blue: `hsl(215, 60%, 45%)` — headings, active stepper, buttons
- Light Blue: `hsl(215, 40%, 95%)` — card backgrounds, highlights
- Gray 700: `hsl(215, 15%, 30%)` — body text
- Gray 400: `hsl(215, 10%, 65%)` — muted text, borders
- White: `hsl(0, 0%, 100%)` — page background
- Alert Yellow: `hsl(45, 90%, 95%)` — warning banners
- Success Green: `hsl(145, 45%, 42%)` — completed steps, approve state
- Error Red: `hsl(0, 65%, 55%)` — reject state, validation errors

**Typography:**
- Font: Inter (system sans-serif fallback)
- H1: 28px semibold — page titles
- H2: 20px semibold — card headings
- Body: 16px regular — content
- Caption: 14px regular — labels, hints

**Spacing:** 8px grid system. Cards use 24px padding. Page content max-width 800px, left-aligned within centered container.

**Borders:** 1px solid gray-200, border-radius 8px on cards. No box-shadows except subtle 1px on cards.

---

## Global Layout

- **Top bar:** "NEXORA AI" wordmark (left), subtitle "Explainable Decision Intelligence" (right-aligned, muted)
- **Progress Stepper:** Horizontal 8-step stepper below top bar. Shows step numbers + short labels. Current step = blue filled circle. Completed = green check. Future = gray outline. Thin connecting lines between steps.
- **Content area:** Single centered column (max 800px), left-aligned text. Each page renders here.
- **Navigation:** "Back" (text button, left) and "Next/Proceed" (primary button, right) at bottom of each step. Back is hidden on step 1 and disabled after finalization (step 7+).

---

## Page-by-Page Design

### Step 1: Introduction
- Large heading: "NEXORA AI"
- Subtitle paragraph: 2-3 sentences explaining this is an academic prototype for explainable decision intelligence
- Three principle cards in a row:
  - 🔍 "Explainability First" — AI shows WHY before WHAT
  - 🤝 "Human-in-the-Loop" — Every decision requires human validation
  - 📋 "Decision Support Only" — AI recommends, never decides
- Each card: icon top, title, one-line description
- CTA: "Start Decision Flow →" primary button

### Step 2: Evidence Upload
- Heading: "Upload Evidence Documents"
- Drag-and-drop zone: dashed border box with upload icon and "Drop files here or click to browse" text
- Accepted types note below: "PDF, TXT, DOCX — Max 10MB per file"
- Warning banner (yellow background): "⚠ Only uploaded documents will be used for analysis. No internet retrieval."
- Uploaded file list: each file shows name, size, remove button
- "Proceed to Analysis" button — disabled (grayed) until at least one file is uploaded

### Step 3: Processing Pipeline
- Heading: "Analyzing Evidence"
- Vertical pipeline visualization — 5 stages displayed as a checklist with status indicators:
  1. Chunking Evidence
  2. Generating Embeddings
  3. Retrieving Relevant Context
  4. Constructing Structured Prompt
  5. Generating Explainable Recommendation
- Each stage: checkbox/checkmark icon → label → status text (Pending / Processing / Complete)
- Currently processing stage shows a simple horizontal progress bar (no spinner)
- Auto-advances to next page when all stages complete
- Note at bottom: "Processing is simulated for demonstration purposes."

### Step 4: AI Insight
- Heading: "Structured AI Recommendation"
- Three stacked cards with clear borders:
  - **Card 1 — Recommendation:** Bold statement of the AI's suggested decision
  - **Card 2 — Influencing Factors:** Bulleted list of 3-5 factors that shaped the recommendation
  - **Card 3 — Confidence Explanation:** Text explaining confidence level with a simple horizontal bar (e.g., 78% — Moderate-High)
- Muted footer text: "This is an AI-generated recommendation. It requires human validation before finalization."
- "View Explanation →" button

### Step 5: Explainability
- Heading: "Why This Recommendation?"
- Banner: "This recommendation is based on the following retrieved evidence."
- Evidence snippets section: 2-4 cards, each containing:
  - Source document name (small label)
  - Highlighted text excerpt (light blue background block quote)
  - Relevance score badge (e.g., "92% relevant")
- Section: "Reasoning Chain" — numbered list showing how evidence was connected to produce the recommendation
- Clean, analytical layout — feels like a research paper appendix

### Step 6: Human Validation
- Heading: "Human Decision Required"
- Alert banner (blue): "⚠ AI cannot finalize decisions. Human validation is required."
- AI recommendation summary displayed in a read-only card
- Three radio-style option cards (no default selected):
  - ✅ **Approve** — "Accept the AI recommendation as-is"
  - ❌ **Reject** — "Decline the recommendation entirely"
  - ✏️ **Modify** — "Accept with changes"
- If Reject or Modify selected: text area appears — "Please explain your reasoning" (required, minimum 20 characters)
- "Finalize Decision" button — disabled until a valid selection is made (and explanation provided if needed)
- Validation error shown inline if user tries to proceed without completing requirements

### Step 7: Final Outcome
- Heading: "Decision Record"
- Structured report layout (like an academic table):
  - **Human Decision:** Approved / Rejected / Modified
  - **AI Recommendation:** (original text)
  - **Difference:** (shown only if Modified — displays what changed)
  - **Human Reasoning:** (the explanation text, if provided)
  - **Timestamp:** Date and time of finalization
  - **Decision ID:** Auto-generated reference number
- Card styled like a formal document/report
- Back button is now disabled
- "View Defense Summary →" button

### Step 8: Defense Summary
- Heading: "Project Defense Summary"
- Designed as a printable page (clean margins, no interactive elements)
- Sections:
  1. **RAG Pipeline Flow:** Simple horizontal flowchart diagram (Document → Chunking → Embeddings → Retrieval → Prompt → LLM → Output) built with styled div boxes and arrows
  2. **Explainability Architecture:** Shows how evidence maps to recommendations
  3. **Human-in-the-Loop Flow:** Diagram showing AI recommends → Human validates → Final decision
  4. **Data Storage Summary:** Table showing what data is captured at each step
  5. **Limitations:** Bulleted list (simulated processing, no real LLM, limited file types, etc.)
- "Print Summary" button that triggers browser print dialog
- "Start New Decision" button to reset and return to Step 1

---

## UX Flow Rules

- Steps are strictly sequential — clicking a future step in the stepper does nothing
- Clicking a completed past step navigates back (except after Step 7 finalization)
- All state is held in React context (no backend needed)
- File upload is simulated (files are listed but not actually processed)
- Processing pipeline is simulated with timed delays
- AI outputs are hardcoded demo content
- Form validation is enforced before proceeding

---

## Error & Validation States

- Upload page: "Please upload at least one file" if proceeding with no files
- Validation page: "Please select a decision" if no option chosen; "Please provide an explanation" if Reject/Modify without text
- All errors shown as inline red text below the relevant element
- Disabled buttons use reduced opacity (0.5) and cursor-not-allowed

