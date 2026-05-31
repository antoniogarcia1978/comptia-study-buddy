# Skill: validate-questions

## Purpose
Full validation of CompTIA A+ Study Buddy questions. This skill exists because
we learned the hard way that fixing what gets flagged is not the same as
validating everything. This checklist must be completed top-to-bottom, in order,
for EVERY question — not just new ones, not just flagged ones. ALL of them.

## Golden Rule
**Never assume a question is correct because it wasn't flagged.**
Unflagged = unchecked. The only correct status is Proven or Not Yet Proven.

---

## The Validation Stack (do in this order)

### LAYER 0: Structural Integrity
Run this first. If it fails, stop and fix before proceeding.

```bash
node -e "
const fs = require('fs');
const content = fs.readFileSync('./index.html', 'utf8');
const start = content.indexOf('const QUESTIONS = [');
const end = content.indexOf('];', start) + 2;
const QUESTIONS = eval('(' + content.slice(start + 'const QUESTIONS = '.length, end - 1).trim() + ')');

const validCore1Objs = ['1.1','1.2','1.3','2.1','2.2','2.3','2.4','2.5','2.6','2.7','2.8','3.1','3.2','3.3','3.4','3.5','3.6','3.7','3.8','4.1','4.2','5.1','5.2','5.3','5.4','5.5','5.6'];
const validCore2Objs = ['1.1','1.2','1.3','1.4','1.5','1.6','1.7','1.8','1.9','1.10','1.11','2.1','2.2','2.3','2.4','2.5','2.6','2.7','2.8','2.9','2.10','2.11','3.1','3.2','3.3','3.4','4.1','4.2','4.3','4.4','4.5','4.6','4.7','4.8','4.9','4.10'];

let pass = true;
function chk(label, cond, detail) {
  if (!cond) { console.log('FAIL', label, detail||''); pass = false; }
  else console.log('PASS', label);
}

chk('JS syntax valid', true); // if eval didn't throw
chk('111 total questions', QUESTIONS.length === 111);
chk('56 Core 1', QUESTIONS.filter(q=>q.exam==='core1').length === 56);
chk('55 Core 2', QUESTIONS.filter(q=>q.exam==='core2').length === 55);

const ids = QUESTIONS.map(q=>q.id);
chk('No duplicate IDs', ids.length === new Set(ids).size);

const req = ['id','exam','domainNum','domainName','objective','objectiveText','question','options','correct','explanation','wrongReasons','source1','source2','messerSection','difficulty'];
const missingF = QUESTIONS.filter(q=>req.some(f=>q[f]===undefined));
chk('All required fields', missingF.length===0, missingF.map(q=>q.id).join(','));

chk('All correct 0-3', QUESTIONS.filter(q=>![0,1,2,3].includes(q.correct)).length===0);
chk('All exam values valid', QUESTIONS.filter(q=>!['core1','core2'].includes(q.exam)).length===0);
chk('All options 4 items', QUESTIONS.filter(q=>!Array.isArray(q.options)||q.options.length!==4).length===0);
chk('All wrongReasons 4 items', QUESTIONS.filter(q=>!Array.isArray(q.wrongReasons)||q.wrongReasons.length!==4).length===0);
chk('null at correct index', QUESTIONS.filter(q=>q.wrongReasons[q.correct]!==null).length===0, QUESTIONS.filter(q=>q.wrongReasons[q.correct]!==null).map(q=>q.id).join(','));
chk('No null string literals', QUESTIONS.filter(q=>JSON.stringify(q).includes('\"null\"')).length===0);

const badObj = QUESTIONS.filter(q=>{
  const valid = q.exam==='core1' ? validCore1Objs : validCore2Objs;
  return !valid.includes(q.objective);
});
chk('All objectives valid', badObj.length===0, badObj.map(q=>q.id+':'+q.objective).join(','));

const dmMis = QUESTIONS.filter(q=>q.objective.split('.')[0] !== (q.domainNum||'').split('.')[0]);
chk('domainNum matches objective', dmMis.length===0, dmMis.map(q=>q.id).join(','));

const msMis = QUESTIONS.filter(q=>q.messerSection !== q.objective);
chk('messerSection matches objective', msMis.length===0, msMis.map(q=>q.id+' obj:'+q.objective+' ms:'+q.messerSection).join(','));

const oldSrc = QUESTIONS.filter(q=>(q.source1||'').includes('v4.0'));
chk('No old v4.0 sources', oldSrc.length===0, oldSrc.map(q=>q.id).join(','));

console.log(pass ? 'ALL STRUCTURAL CHECKS PASS' : 'STRUCTURAL FAILURES - FIX BEFORE PROCEEDING');
"
```

All checks must pass before continuing.

---

### LAYER 1: Objective Assignment
For EVERY question, verify that the question topic genuinely belongs under the
assigned objective — not just that the objective number is valid.

**How to check:**
1. Fetch the official objective PDF (both exams):
   - 220-1201 V15: search for "CompTIA A+ 220-1201 exam objectives V15 PDF"
   - 220-1202 V15: search for "CompTIA A+ 220-1202 exam objectives V15 PDF"
2. For each question, confirm the topic appears explicitly in the bullet points
   of the assigned objective — not just in the domain generally.
3. Confirm the objectiveText is the exact wording from the PDF, not a paraphrase.

**What to look for:**
- Question topic is listed in a DIFFERENT objective's bullet points
- objectiveText is approximate or from an older exam version
- The question tests a sub-topic that belongs under a sibling objective

**Do NOT assume:** "This seems related to this objective" is not validation.
The bullet point must be there in the document.

**Checklist per question (Layer 1):**
- [ ] Question topic appears in assigned objective's bullet points
- [ ] objectiveText matches official document exactly (not paraphrased)
- [ ] domainName matches official document exactly
- [ ] source1 subdomain label is accurate

---

### LAYER 2: Answer Accuracy
For EVERY question, verify the correct answer is factually correct.

**How to check:**
1. Identify the authoritative source for the specific fact being tested
2. Confirm the correct answer against that source
3. Confirm the wrong answers are definitively wrong (not just less correct)
4. Confirm the explanation is technically accurate and teaches the right concept

**Sources in priority order (use highest available):**
1. Official CompTIA A+ Study Guide (Mike Meyers or Darril Gibson for V15)
2. Professor Messer's specific video for that section (look up the video, not just the outline)
3. The official CompTIA exam objectives bullet point (confirms the topic exists, not the answer)
4. Primary technical documentation (RFC, Microsoft docs, Apple docs, IEEE spec)

**What to look for:**
- Correct answer is actually a common misconception
- Explanation teaches a rule that has exceptions not mentioned
- Wrong options could be correct in certain contexts (question needs to be more specific)
- Explanation is technically accurate but doesn't match what the exam likely tests

**Do NOT use:**
- Other quiz sites (they copy each other's errors)
- General web search results (too many inaccurate sources)
- Your own training data confidence as validation (that's how errors were introduced)

**Checklist per question (Layer 2):**
- [ ] Correct answer verified against authoritative source (name the source)
- [ ] Explanation is technically accurate
- [ ] Explanation correctly explains WHY this is the right answer
- [ ] Each wrong reason correctly explains WHY that option is wrong
- [ ] Wrong options are definitively wrong, not just less optimal

---

### LAYER 3: Question Quality
After Layers 1 and 2 pass, check whether the question is a good test item.

**Checklist per question (Layer 3):**
- [ ] The question has a single unambiguous correct answer
- [ ] The scenario is realistic and tests practical knowledge
- [ ] The wrong options are plausible (a test-taker who doesn't know would consider them)
- [ ] The difficulty rating matches: easy = recall, medium = application, hard = analysis
- [ ] The question doesn't telegraph the answer (e.g., don't use the answer's keyword in the question)

---

### LAYER 4: Validate Your Own Fixes
After making any correction, check that the correction itself is correct.

**This is not optional.** Fixing an error incorrectly is a new error.

**For every fix made:**
- [ ] Re-read the fixed field against the source document
- [ ] Run Layer 0 structural check again
- [ ] Verify the fix didn't introduce a mismatch with other fields

---

## Tracking Template

When running a validation pass, maintain a log:

```
Question: c1-X.X-XXX
L0 Structure: PASS / FAIL (describe)
L1 Objective: PASS / FAIL / NOT YET CHECKED
  - Source confirmed: [document name + page/section]
  - objectiveText exact: YES / NO (actual text: ...)
L2 Answer: PASS / FAIL / NOT YET CHECKED
  - Correct answer source: [document + quote]
  - Explanation accurate: YES / NO (issue: ...)
  - Wrong reasons accurate: YES / NO (issue: ...)
L3 Quality: PASS / FAIL / NOT YET CHECKED
Notes:
```

Do not mark a question PASS on any layer until you have the source reference.
"Seems right" is not a source.

---

## Common Failure Modes (learned from this project)

1. **Citation-first writing**: Questions written from memory, citations assigned after.
   Result: citations reference old objective structure, content is newer.
   Fix: Always start from the official objective bullet point, write question to test it.

2. **Unflagged = assumed correct**: Only fixing what breaks structural checks.
   Result: wrong answers and explanations persist indefinitely.
   Fix: Treat every question as Not Yet Checked until Layer 2 is complete.

3. **Approximate objectiveText**: Using paraphrases instead of exact document wording.
   Result: study app teaches slightly wrong objective descriptions.
   Fix: Copy-paste from PDF; never rephrase.

4. **Cascade correction errors**: Fixing a wrong objective number but not checking
   if the explanation or wrong reasons then need updating for the new context.
   Fix: When changing objective, re-check all fields in Layer 2 and 3.

5. **Source version drift**: Using v4.0 objective structure for V15 content.
   Result: domain numbers, objective counts all off.
   Fix: Confirm exam version for every source reference before writing.

---

## Before Adding New Questions

Do not add questions until:
1. The authoritative source (official objective bullet point) is in hand
2. The correct answer is confirmed from a primary source — not generated from memory
3. All 4 layers above are pre-checked before the question is written into the file
4. Layer 0 structural check passes after insertion

## Reference: Official Document URLs (fetch fresh, do not use cached)

- 220-1201 V15 objectives: search "CompTIA A+ 220-1201 exam objectives" on comptia.org
- 220-1202 V15 objectives: search "CompTIA A+ 220-1202 exam objectives" on comptia.org  
- Professor Messer 220-1201 course: professormesser.com/free-a-plus-training/220-1201/
- Professor Messer 220-1202 course: professormesser.com/free-a-plus-training/220-1202/
