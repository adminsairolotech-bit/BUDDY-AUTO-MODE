# 🚀 ULTIMATE AI ENGINEERING SYSTEM (FINAL v5.0 - LEARNING + COMPLETE)

MODE: FULL AUTO + SELF HEAL + SMART CONTROL + FAILSAFE + ERROR INTELLIGENCE + LEARNING

--------------------------------------------------
# 🧠 SYSTEM OVERVIEW
--------------------------------------------------
Codex = executor
ChatGPT = auditor
System = detect → fix → verify → learn → improve → repeat

--------------------------------------------------
# 🔒 CORE RULES
--------------------------------------------------
NO GUESSING
NO FAKE SUCCESS
NO PARTIAL FIX
ONLY VERIFIED OUTPUT

--------------------------------------------------
# 📁 FILE CONTROL
--------------------------------------------------
ALLOW:
src/
api/
engines/

BLOCK:
dist/
build/
__pycache__/
exports/

--------------------------------------------------
# 🧪 PRE-OUTPUT VALIDATION
--------------------------------------------------
Before ANY output:
- Check syntax
- Validate logic
- Simulate execution
- Check dependencies
- Handle edge cases

If doubt → STOP

--------------------------------------------------
# 🔁 EXECUTION LOOP (SMART + LEARNING)
--------------------------------------------------
MAX_CYCLES = 5
ERROR_REPEAT_LIMIT = 2

last_error = ""
repeat_count = 0

FOR each cycle:

1. node -v
2. npm -v
3. npm install
4. npm run typecheck 2> error.log
5. npm test 2>> error.log

capture current_error from error.log (last 20 lines)

normalize error:
- remove timestamps
- remove random values

IF current_error == last_error:
    repeat_count += 1
ELSE:
    repeat_count = 0
    last_error = current_error

IF repeat_count >= ERROR_REPEAT_LIMIT:
    STOP
    SAVE error to learning log
    RETURN FAILED

IF FAIL:
    Fix root cause
    CONTINUE

IF PASS:
    BREAK

IF cycles > MAX_CYCLES:
SAVE failure to learning log
RETURN FAILED

--------------------------------------------------
# 🧠 LEARNING SYSTEM
--------------------------------------------------
Store errors in:
.ai_memory/errors.log

Store fixes in:
.ai_memory/solutions.log

Before fixing:
Check if similar error exists
Reuse previous solution if available

--------------------------------------------------
# 📊 SYSTEM VALIDATION
--------------------------------------------------
Stage-1:
attempted > 0
verified > 0

--------------------------------------------------
# 💾 PROOF SYSTEM
--------------------------------------------------
git diff > codex_changes.patch
git diff --name-only > changed_files.txt

--------------------------------------------------
# 🧾 COMMIT + SAFE ROLLBACK
--------------------------------------------------
git add .
git commit -m "ultimate auto fix v5"

IF system breaks:
git reset --hard HEAD~1

--------------------------------------------------
# ☁️ CLOUD AUTO (CI)
--------------------------------------------------
Run every 30 min:
- Typecheck
- Tests
- Validation

--------------------------------------------------
# 🤖 PIPELINE CONTROL
--------------------------------------------------
MAX_PIPELINE_RUN = 5

IF pipeline runs > MAX_PIPELINE_RUN:
STOP and return FAILED

--------------------------------------------------
# 📋 FINAL REPORT
--------------------------------------------------
---REPORT START---

STATUS: SUCCESS / FAILED
CYCLES_USED: number
TYPECHECK: PASS / FAIL
TESTS: PASS / FAIL
VERIFIED: number
FILES_CHANGED: number
COMMIT: hash

---REPORT END---

--------------------------------------------------
# 🎯 FINAL LAW
--------------------------------------------------
SMART > FAST
SAFE > SMART
LEARNING > REPEATING
VERIFIED > ASSUMED

SYSTEM MUST LEARN, ADAPT, AND IMPROVE OVER TIME
