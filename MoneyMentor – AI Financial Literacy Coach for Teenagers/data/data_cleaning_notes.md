
---

## 🧹 `datacleaningnotes.md` – Data Cleaning Notes

```markdown
# 🧼 Data Cleaning Notes – sim_scenarios_fixed.csv

## 📥 Source

Original scenarios were manually written and reviewed by the project team. The file was cleaned and standardized before use.

## ✅ Cleaning Steps

1. **Removed Duplicates**  
   - Any scenario with identical `scenario_text` was removed.

2. **Trimmed Whitespace**  
   - Leading/trailing spaces removed from all text columns.

3. **Ensured Column Consistency**  
   - All rows must have valid `A` or `B` for `correct_option`.

4. **Validated Feedback Pairs**  
   - `feedback_correct` and `feedback_incorrect` were rewritten to be distinct, educational, and friendly.

5. **Encoding Check**  
   - Saved with UTF-8 encoding to avoid issues in non-Windows environments.

6. **Manual Spot Checks**  
   - 100% manually reviewed for grammar, tone, and Gen Z relatability.

## 📈 Stats

- Total scenarios: 30
- Target audience: Teens (13–19)
- Tone: Light, encouraging, clear

## 🚩 Common Fixes

- Replaced slang with readable alternatives where too obscure.
- Changed ambiguous financial terms to simpler ones.
- Unified capitalization style.

## 🔮 Future Improvements

- Add tags or topic categories (e.g., budgeting, impulse spending)
- Include image or meme-based questions for engagement
