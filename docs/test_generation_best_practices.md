# 📋 Test Generation Best Practices

## 🎯 Critical Principles

### 1. **ALWAYS Trust Source Files, NOT Verbal Communication** ⚠️

**Why This Matters:**

- Verbal communication can be outdated, misremembered, or misunderstood
- Source files are the **single source of truth**
- Discrepancies between verbal and written specs cause bugs

**Enforcement:**

1. ✅ **Extract values directly from files** using regex/parsing
2. ✅ **Run automated validation** against source files
3. ❌ **NEVER assume or remember** requirements from conversation
4. ⚠️ **When conflict arises**: Ask user which is correct, then update source file

**Example:**

```
❌ BAD: User said "API < 3s" → Generate test with 3000ms
✅ GOOD: Read PRD line 95 "< 1 giây" → Extract 1 → Generate test with 1000ms
```

---

### 2. **Validation is Mandatory, Not Optional**

**Every test case generation MUST:**

1. Generate raw test cases
2. Format to final output
3. **Run validation script**
4. **Fix issues if validation fails**
5. Re-validate until PASS (exit code 0)

**Workflow Integration:**

```bash
# Step 1: Generate
python -m test-gen.main --step prepare
# ... AI generation ...

# Step 2: Format
python -m test-gen.main --step format

# Step 3: VALIDATE (MANDATORY)
python -m test-gen.main --step validate --prd <prd>

# Step 4: If failed, fix and repeat 2-3
```

---

### 3. **Self-Correction Checklist**

Before finalizing test cases, verify:

**Coverage:**

- [ ] XSS injection test present?
- [ ] SQL injection test present?
- [ ] Boundary tests (min-1, min, max, max+1)?
- [ ] Empty field tests?
- [ ] All browsers from PRD tested?

**Accuracy:**

- [ ] Performance SLAs match PRD exactly?
- [ ] Browser list matches PRD exactly?
- [ ] Validation rules match Data Dictionary?
- [ ] Error messages match PRD specifications?

**Quality:**

- [ ] All PRD sections covered?
- [ ] Security requirements tested?
- [ ] Analytics events tracked (if in PRD)?
- [ ] Responsive breakpoints tested?

---

## 🛠️ Validation Script Usage

### Basic Usage

```bash
python -m test-gen.main --step validate --prd input/yourPrd.md
```

### Understanding Exit Codes

- **Exit 0**: ✅ All validations passed
- **Exit 1**: ❌ Issues found, review output

### What Gets Validated

1. **Performance SLAs**
   - API response time matches PRD
   - Email delivery time matches PRD

2. **Browser Compatibility**
   - All browsers from PRD have test cases
   - No extra browsers (warnings only)

3. **Validation Rules** (future)
   - Password min/max length
   - Email regex patterns
   - Field required/optional status

---

## 📚 Common Mistakes to Avoid

### Mistake 1: Trusting Memory Over Files

```diff
- User: "API should be < 3 seconds"
- Agent: "OK, generating test with 3000ms"
+ Agent: "Let me read the PRD file first..."
+ PRD Line 95: "< 1 giây"
+ Agent: "Generating test with 1000ms"
```

### Mistake 2: Skipping Validation

```diff
- Generate → Format → Done ❌
+ Generate → Format → Validate → Fix → Re-validate → Done ✅
```

### Mistake 3: Partial Requirements Coverage

```diff
- Only testing API response time ❌
+ Testing API response time AND email delivery time ✅
+ (Both are in PRD Section 4.2)
```

---

## 🎓 Lessons from Real Issues

### Case Study 1: Performance SLA Mismatch

**Issue:** Test case had "< 3s" but PRD specified "< 1s"  
**Root Cause:** Trusted verbal communication  
**Fix:** Read PRD file line 95, extracted exact value  
**Prevention:** Always validate against source file

### Case Study 2: Missing Browser Test

**Issue:** Generated 5 browser tests but PRD only listed 4  
**Root Cause:** Assumed Operamini was in list  
**Fix:** Read PRD Section 4.3, generated exactly 4 tests  
**Prevention:** Validation script catches missing/extra browsers

---

## ✅ Quality Checklist

Before delivering test cases:

1. [ ] Read ALL relevant source files (PRD, Swagger, Matrix)
2. [ ] Extract exact values (regex parsing, not assumptions)
3. [ ] Generate comprehensive test cases
4. [ ] Run format step
5. [ ] **Run validation script (MANDATORY)**
6. [ ] Fix any validation errors
7. [ ] Re-validate until exit code 0
8. [ ] Document what was tested and coverage

---

**Remember: Quality comes from systematic processes, not hope!** 🎯
