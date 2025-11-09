# Presentation Styling Options for CE101 Master Deck

## Context

The master presentation (`CE101-Master-Presentation.pptx`) consists of pre-rendered PNG images for each slide, making it non-editable. We need to create a professionally styled, editable presentation featuring orange (Little Caesars branding).

## Option A: Style Individual Session Files

### Overview
Work with the 7 individual session PowerPoint files in `slides/` directory, which appear to be editable PowerPoint presentations (not images).

### Files to Work With
```
slides/
├── CE101-Session1-CoreConcepts.pptx (2.1M)
├── CE101_Session2_Filesystem_Organization.pptx (324K)
├── CE101_Session3_Multi_Tab_Orchestration.pptx (560K)
├── CE101_Session4_Local_Data_Stores.pptx (605K)
├── CE101_Session5_Integration_Patterns.pptx (258K)
├── CE101_Session6_Practical_Patterns.pptx (941K)
└── CE101_Session7_Common_Pitfalls.pptx (1.1M)
```

### Approach
1. **Analyze one session file** (e.g., Session1) to confirm it's editable
2. **Apply orange color scheme** to the PowerPoint theme
3. **Test visual improvements** (accent bars, headers, styling)
4. **Replicate across all 7 sessions** if successful
5. **Combine styled sessions** into master presentation using `combine_presentations.py`

### Color Scheme to Apply
- Primary Orange: #F96D00
- Deep Orange: #E85D04
- Charcoal: #222831 (text)
- Cool Gray: #546E7A (secondary text)
- Light Background: #F5F5F5
- Accent Teal: #4A90A4

### Advantages
- ✅ Existing slides may already be properly formatted
- ✅ Known working structure
- ✅ Can preserve existing layouts
- ✅ Faster than recreating from scratch

### Challenges
- ❓ Unknown if session files are truly editable or also images
- ❓ May need to manually update 7 separate files
- ❓ Consistency across sessions needs verification

### Next Steps
1. Unpack one session file to verify editability
2. If editable: apply theme updates and visual improvements
3. If not editable: fall back to Option B

---

## Option B: Generate from Markdown Source

### Overview
Create new presentation from `CE101-Master-Presentation.md` using html2pptx workflow with professional orange styling.

### Current Status
- ✅ Generator script created: `workspace/generate-presentation.js`
- ✅ Color scheme designed
- ✅ HTML templates designed
- ⚠️ Layout validation errors on some slides (text overflow, spacing)

### Technical Approach
- Parse markdown into slide objects
- Generate styled HTML for each slide type:
  - Title slides: Dark background with orange accent bar
  - Module dividers: Full orange background
  - Content slides: White with orange left accent bar
- Convert HTML to PowerPoint using html2pptx.js library

### Current Issues
Encountered layout validation errors:
- Slide 10: Text too close to bottom edge
- Some slides: Horizontal overflow
- Need to adjust font sizes, padding, and max-widths

### Advantages
- ✅ Fully editable PowerPoint output
- ✅ Consistent styling across all slides
- ✅ Source of truth is markdown (easy to update)
- ✅ Complete control over design

### Challenges
- ❌ Complex layout validation issues
- ❌ Need to debug 56 slides individually
- ❌ Time-intensive to perfect all layouts
- ❌ Limited by html2pptx rendering capabilities

---

## Recommendation

**Try Option A first:**
1. Verify session files are editable (5 minutes)
2. If yes: style and combine (1-2 hours)
3. If no: switch to Option B debugging

**Option B as fallback:**
- More time investment but guarantees full control
- Consider if presentation will be frequently updated from markdown
- Worth it for long-term maintainability

---

## Related Files

- Original: `CE101-Master-Presentation.pptx` (images only)
- Improved theme: `CE101-Master-Presentation-Improved.pptx` (theme updated, still images)
- Markdown source: `CE101-Master-Presentation.md`
- Generator script: `workspace/generate-presentation.js`
- Combine script: `combine_presentations.py`
