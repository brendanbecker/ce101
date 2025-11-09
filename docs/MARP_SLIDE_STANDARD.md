# Marp Slide Content Standard

## Maximum Content Limits

To ensure slides render without overflow in Marp presentations:

### Content Density Rules

**Per slide maximum:**
- **Title**: 1 line (or title + subtitle)
- **Body content**: 6-8 lines of visible text
- **Bullet points**: 3-5 top-level bullets (max)
- **Sub-bullets**: 1-2 per parent bullet (use sparingly)
- **Code blocks**: 5-8 lines maximum
- **Tables**: 4-5 rows maximum
- **Examples (❌/✅ pairs)**: 3 pairs maximum

### Content Line Counting

**What counts as a "line":**
- Each bullet point = 1 line (even if text wraps)
- Each sub-bullet = 1 line
- Bold statements = 1 line
- Code block lines = 1 line each
- Table rows = 1 line each

**What doesn't count:**
- Slide titles/subtitles
- Speaker notes (HTML comments)
- Horizontal rules (---)

### Example: Good Slide

```markdown
# Slide Title

**Key concept**: Brief explanation in one line

- Bullet point one
- Bullet point two
- Bullet point three

**Takeaway**: Brief closing statement

<!-- Speaker notes don't count toward content -->
```

**Content lines**: 5 (1 concept + 3 bullets + 1 takeaway) ✅

### Example: Overflow Slide

```markdown
# Slide Title

**Intro**: Some introduction text

**Section 1**: Description
- Sub-point A
- Sub-point B

**Section 2**: Description
- Sub-point C
- Sub-point D

**Section 3**: Description
- Sub-point E
- Sub-point F

**Closing**: Summary statement
```

**Content lines**: 13 (1 intro + 3 sections × 3 lines + 1 closing) ❌ OVERFLOW

### Fixing Overflow

**Option 1: Split into multiple slides** (preferred)
```markdown
# Slide Title - Part 1

**Section 1**: Description
- Sub-point A
- Sub-point B

**Section 2**: Description
- Sub-point C
- Sub-point D

---

# Slide Title - Part 2

**Section 3**: Description
- Sub-point E
- Sub-point F

**Takeaway**: Key message
```

**Option 2: Simplify content**
```markdown
# Slide Title

**Three approaches:**
- Section 1: Brief description
- Section 2: Brief description
- Section 3: Brief description

**Takeaway**: Key message
```

**Option 3: Move details to speaker notes**
```markdown
# Slide Title

**Key sections:**
- Section 1
- Section 2
- Section 3

<!--
Speaker Note:
Section 1: Full detailed description with examples
Section 2: Full detailed description with examples
Section 3: Full detailed description with examples
-->
```

## Validation Checklist

Before running `marp` to convert:

- [ ] No slide has more than 8 content lines
- [ ] Multi-section slides are split appropriately
- [ ] Long examples are shortened or split
- [ ] Code blocks are ≤ 8 lines
- [ ] Tables are ≤ 5 rows
- [ ] Complex content moved to speaker notes

## Testing for Overflow

**Manual check:**
1. Count content lines per slide (excluding title and notes)
2. If > 8 lines, refactor using options above

**After conversion:**
1. Open generated PPTX
2. Scan through slides for text overflow
3. Note slide numbers with overflow
4. Fix in markdown and regenerate

## Common Overflow Patterns

**Pattern 1: Directory trees**
- Problem: Large ASCII directory structures
- Fix: Show only 2-3 levels, simplify

**Pattern 2: Multi-column comparisons**
- Problem: Before/after, ❌/✅ with long text
- Fix: Shorten examples, max 3 pairs

**Pattern 3: Multiple examples**
- Problem: 4+ code/text examples on one slide
- Fix: Split into 2 slides or show only best 2 examples

**Pattern 4: Itemized sections**
- Problem: 4 sections × 2 bullets each = 12 lines
- Fix: Split sections across 2 slides

## Quick Reference

```
Content Lines    Status
0-6              ✅ Ideal
7-8              ⚠️  Borderline (verify in PPTX)
9+               ❌ Overflow likely - refactor required
```

## Standard Application

When creating new slides for CE101 or similar presentations:

1. Draft slide content
2. Count content lines
3. If > 8, immediately refactor using patterns above
4. Add detailed info to speaker notes
5. Validate after `marp` conversion
6. Iterate if needed

**Remember**: Less content per slide = better audience retention and clearer messaging.
