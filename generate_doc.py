from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
section = doc.sections[0]
section.top_margin    = Inches(1)
section.bottom_margin = Inches(1)
section.left_margin   = Inches(1.2)
section.right_margin  = Inches(1.2)

# ── Helper functions ──────────────────────────────────────────────────────────
def heading1(text):
    p = doc.add_heading(text, level=1)
    p.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    return p

def heading2(text):
    p = doc.add_heading(text, level=2)
    p.runs[0].font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)
    return p

def body(text):
    p = doc.add_paragraph(text)
    p.runs[0].font.size = Pt(11)
    return p

def bullet(text, level=0):
    p = doc.add_paragraph(text, style='List Bullet')
    p.runs[0].font.size = Pt(11)
    return p

def note(text):
    p = doc.add_paragraph()
    run = p.add_run(f'Note: {text}')
    run.italic = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    return p

def spacer():
    doc.add_paragraph()

# ── Title block ───────────────────────────────────────────────────────────────
title = doc.add_heading('CompTIA A+ Study Buddy', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

sub = doc.add_paragraph('Project Overview — Version 3.0')
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub.runs[0].font.size = Pt(13)
sub.runs[0].font.color.rgb = RGBColor(0x59, 0x59, 0x59)

date_p = doc.add_paragraph('June 2026')
date_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
date_p.runs[0].font.size = Pt(11)
date_p.runs[0].font.color.rgb = RGBColor(0x59, 0x59, 0x59)

doc.add_page_break()

# ── 1. What It Is ─────────────────────────────────────────────────────────────
heading1('1. What It Is')
body(
    'CompTIA A+ Study Buddy is a self-contained web-based quiz application '
    'designed to help IT professionals prepare for the CompTIA A+ certification '
    'exams: 220-1201 (Core 1) and 220-1202 (Core 2), Version 15 (V15), '
    'released March 2025.'
)
spacer()
body(
    'The application runs entirely in a web browser with no installation, '
    'no login, and no backend server required. It is a single HTML file that '
    'contains all questions, logic, and styling. It can be opened locally or '
    'accessed from any device via a hosted URL.'
)
spacer()
body('Key characteristics:')
bullet('111 questions total: 56 Core 1 questions, 55 Core 2 questions')
bullet('Questions are organized by CompTIA exam domain and objective number')
bullet('Each question includes four answer options, the correct answer, a full explanation, and a specific reason why each wrong answer is wrong')
bullet('Difficulty is rated per question: easy, medium, or hard')
bullet('Designed as a diagnostic tool: take a pass, identify weak domains, study those sections, retest')

spacer()

# ── 2. How the Information Was Seeded ─────────────────────────────────────────
heading1('2. How the Information Was Seeded')
body(
    'Questions were written against the official CompTIA A+ V15 exam objectives '
    'and validated through a structured four-layer process before being included '
    'in the application.'
)
spacer()

heading2('Layer 0 — Structural Integrity')
body(
    'Every question passes an automated 16-point structural check run via Node.js. '
    'Checks include: valid JavaScript syntax, correct question count per exam, '
    'no duplicate question IDs, all required fields present, correct answer index '
    'in range 0–3, exactly four answer options per question, exactly one null '
    'placeholder in wrong-reason fields at the correct answer position, no '
    'accidental "null" string literals, and all objective numbers valid against '
    'the official V15 objective list.'
)

heading2('Layer 1 — Objective Assignment')
body(
    'Each question is assigned to the specific CompTIA objective it tests. '
    'Objective numbers were validated against the official V15 PDF structure. '
    'During development, 38 Core 1 questions required objective number corrections '
    '(wrong domain assignments from earlier iterations were identified and fixed). '
    'Objective text descriptions are currently approximate paraphrases — exact '
    'wording from the official PDF is a planned refinement.'
)

heading2('Layer 2 — Answer Accuracy')
body(
    'Every question was reviewed individually for factual accuracy. '
    'The correct answer was verified against authoritative sources. '
    'Wrong answers were confirmed as definitively incorrect, not just less optimal. '
    'Explanations were reviewed to ensure they teach the right concept and '
    'accurately explain why each wrong option fails.'
)
body('Three corrections were identified and applied during this process:')
bullet('c1-4.1-003 (Containers): Removed commentary about exam version changes; replaced with factual content about container behavior')
bullet('c2-1.7-001 (dnf/Linux): Removed exam-specific commentary; replaced with factual content about DNF improvements over yum')
bullet('c2-2.2-001 (WPA3): Fixed a technical error — the explanation incorrectly stated WPA3 is "defined in IEEE 802.11ax." IEEE 802.11ax is the Wi-Fi 6 radio standard; WPA3 is a Wi-Fi Alliance security certification.')

heading2('Layer 3 — Question Quality')
body(
    'Not yet completed. This pass reviews whether each question has a single '
    'unambiguous correct answer, whether distractors are realistic, whether '
    'difficulty ratings are calibrated correctly, and whether questions '
    'accidentally telegraph their answers. Planned for a future session.'
)

spacer()

# ── 3. Supporting File Structure ──────────────────────────────────────────────
heading1('3. Supporting File Structure')
body('The project lives in a GitHub repository: antoniogarcia1978/comptia-study-buddy')
spacer()

body('File layout:')
bullet('index.html — the complete application (HTML, CSS, JavaScript, all 111 questions in a single file)')
bullet('.claude/skills/validate-questions.md — the full 4-layer validation protocol, including the automated Layer 0 check script')
bullet('.claude/skills/validation-status.md — per-question validation tracking, honest status for every question across all four layers')
bullet('q_core1.js — source question data for Core 1 (reference file)')
bullet('q_core2.js — source question data for Core 2 (reference file)')

spacer()
body(
    'The validation-status.md file serves as the project\'s source of truth for '
    'what has and has not been verified. It distinguishes between PROVEN '
    '(source confirmed), PARTIAL (some layers checked), FAILED (known error), '
    'and NOT YET CHECKED (assumed correct, no evidence). The rule: unflagged '
    'does not mean correct — only proven means correct.'
)

spacer()

# ── 4. How It Was Shared ──────────────────────────────────────────────────────
heading1('4. How It Was Shared')
body(
    'The application is hosted via GitHub Pages at:'
)
p = doc.add_paragraph()
run = p.add_run('https://antoniogarcia1978.github.io/comptia-study-buddy/')
run.font.size = Pt(11)
run.bold = True

spacer()
body(
    'GitHub Pages serves the index.html file directly from the repository — '
    'no web server configuration required. The URL is accessible from any '
    'device with a browser, including mobile phones. On iPhone, users can '
    'tap Share → Add to Home Screen to create an app-like icon.'
)
spacer()
body('Sharing history:')
bullet('Jordan — shared the URL with an honest briefing of what is validated and what is still approximate. Jordan was asked to flag any questions where two answers seem equally correct or where explanations contradict known facts.')
bullet('Coleman — introduced the project and offered a walkthrough call to discuss potential applications for internal training.')

spacer()

# ── 5. The Interface ──────────────────────────────────────────────────────────
heading1('5. How It Was Orchestrated Into an Interface')
body(
    'The application is a single-page interface with six screens, all running '
    'client-side in the browser with no page reloads:'
)
spacer()
bullet('Home screen — select Core 1 or Core 2 exam')
bullet('Domain selection — choose a specific domain to focus on, or run all domains')
bullet('Question screen — displays the question, four answer options as clickable buttons')
bullet('Answer feedback screen — immediately shows correct/incorrect, the full explanation, and the specific reason why each wrong option is wrong')
bullet('Results screen — shows total score and a breakdown by domain, highlighting areas for further study')
bullet('Review screen — allows the user to go back through all questions and answers after completion')

spacer()
body(
    'The interface requires no account, no login, and stores nothing between '
    'sessions. Each use is independent. Answer randomization (so the correct '
    'answer is not always in the same position) is planned for v4.0.'
)

spacer()

# ── 6. Results and Retention ──────────────────────────────────────────────────
heading1('6. Recording Results and Gauging Retention')

heading2('Current State (v3.0)')
body(
    'Results in v3.0 are session-only. The application calculates and displays '
    'a score at the end of each session broken down by domain, but does not '
    'persist results between sessions. There is no user account system, no '
    'database, and no history tracking. When the browser is closed, the session '
    'results are gone.'
)
note(
    'This is an honest limitation. The tool currently functions as a diagnostic '
    'snapshot, not a longitudinal tracker.'
)

spacer()
heading2('What the Results Show')
body('At the end of each session the user sees:')
bullet('Overall percentage score')
bullet('Score broken down by domain (e.g., Domain 2: Networking — 7/9 correct)')
bullet('Which specific questions were answered incorrectly, with the correct answer shown')

spacer()
heading2('What the Results Gauge')
body(
    'The domain breakdown is the most actionable output. A low score in a specific '
    'domain indicates a study gap in that area — not a general knowledge problem. '
    'The intended use pattern is:'
)
bullet('Take a full exam pass cold (no studying first) to establish a baseline')
bullet('Note which domains scored lowest')
bullet('Study those domains specifically (Professor Messer videos, study guides)')
bullet('Retest the same domains to measure improvement')
bullet('Repeat until all domains are consistently above a comfort threshold')

spacer()
body(
    'For users with on-the-job IT experience, this pattern quickly separates '
    'practical knowledge already retained from exam-specific concepts that '
    'require deliberate study — making preparation more efficient than '
    'watching all course material from scratch.'
)

spacer()

# ── 7. Planned v4.0 ───────────────────────────────────────────────────────────
heading1('7. What\'s Next — Version 4.0')
body('The following improvements are planned for the next version:')
bullet('Answer randomization — correct answer position randomized per session so users cannot memorize answer positions')
bullet('Video-aligned question sets — ~5 questions per Professor Messer course video, organized by video section rather than just exam domain. Approximately 300 questions per exam.')
bullet('Increased granularity — specific IP addresses, port numbers, command syntax, and configuration details tested explicitly rather than concept-only questions')
bullet('Style guide for question consistency — a defined spec for question length, level of detail, and explanation format to prevent drift across development sessions')
bullet('Persistent result tracking — score history stored locally in the browser so users can track improvement over time')

spacer()

# ── Footer note ───────────────────────────────────────────────────────────────
doc.add_page_break()
closing = doc.add_paragraph(
    'This document was prepared in June 2026. The application is actively '
    'being developed. Questions about validation status, known limitations, '
    'or planned features should be directed to the project owner.'
)
closing.runs[0].font.size = Pt(10)
closing.runs[0].font.color.rgb = RGBColor(0x59, 0x59, 0x59)
closing.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ── Save ──────────────────────────────────────────────────────────────────────
out = '/home/user/comptia-study-buddy/StudyBuddy_ProjectOverview.docx'
doc.save(out)
print(f'Saved: {out}')
