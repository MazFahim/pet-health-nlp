# pet-health-nlp

A lightweight tool that reads a short pet health text — either something an
owner writes about their pet, or a line from a vet's clinical note — and
automatically extracts (1) a likely condition category and (2) key symptom
keywords. It turns unstructured pet health text into structured, searchable
data without manual tagging.

## Project status

This project is under **active, public development** on GitHub, working
toward submission to the [Journal of Open Source Software (JOSS)](https://joss.theoj.org/).
The core extraction function is complete and validated (see
[Accuracy](#accuracy) below); ongoing work adds batch processing, a CLI
wrapper, confidence scoring, and expanded documentation ahead of a first
tagged release.

Feedback, bug reports, and pull requests are welcome — see
[CONTRIBUTING.md](CONTRIBUTING.md). If you're using this tool or have ideas
for it, opening an issue helps show real-world interest, which is genuinely
useful for this kind of research-software project.

## What it does

Given a short piece of text describing a pet's symptoms, the tool classifies
it into one of five fixed condition categories and pulls out the symptom
keywords mentioned. It works across species (cats, dogs, rabbits, ferrets,
guinea pigs, hamsters, birds) and across both casual owner-written text and
formal veterinary clinical notes.

```python
extract_pet_health_info("My dog has been scratching his ears and shaking his head.")
# {"condition": "Ear Infections", "keywords": ["scratching", "ears", "shaking his head"]}
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mazfahim/pet-health-nlp.git
   cd pet-health-nlp
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get a free Google Gemini API key from
   [Google AI Studio](https://aistudio.google.com), then set it as an
   environment variable:

   **macOS/Linux:**
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```

   **Windows (PowerShell, permanent):**
   ```powershell
   setx GEMINI_API_KEY "your-key-here"
   ```

   The tool reads the key from this environment variable only — it is never
   read from or written to any file in this repository.

## Usage

```python
from pet_health_nlp.extractor import extract_pet_health_info

result = extract_pet_health_info(
    "My cat vomited what looked like a roundworm."
)
print(result)
# {"condition": "Parasites", "keywords": ["vomited", "roundworm"]}
```

The function returns a dict with two keys:
- `"condition"`: one of the 5 categories below, or `None` if the text has no
  identifiable symptom content (see [Limitations](#limitations))
- `"keywords"`: a list of symptom keywords found in the text

### Condition categories

The tool classifies text into exactly one of these five categories:

- Ear Infections
- Skin Irritations
- Parasites
- Digestive Issues
- Mobility Problems

## Accuracy

Validated on the full 2,000-row
[`karenwky/pet-health-symptoms-dataset`](https://huggingface.co/datasets/karenwky/pet-health-symptoms-dataset)
(Hugging Face, MIT license, synthetic, multi-species, all 5 conditions):

**1728/2000 matched (86.4%)**, holding steady in an 84-92% per-batch range
across the entire dataset with no meaningful accuracy drop on non-cat
species.

## Limitations

Nearly all misclassifications trace back to four well-understood patterns
rather than random model error:

1. **Cause-vs-symptom labeling mismatch** — the dataset sometimes labels a
   row by its underlying cause (often an unstated parasite), while the model
   reads the visible/described symptom. This is the single largest source of
   disagreement.
2. **Ear Infections vs. Skin Irritations overlap** — ear-adjacent
   dermatological presentations (redness, crusts, flakes near but not
   clearly inside the ear) are genuinely ambiguous between these two
   categories.
3. **Ear mite inconsistency** — the source dataset itself labels confirmed
   ear mite cases inconsistently (sometimes Ear Infections, sometimes
   Parasites, occasionally Skin Irritations) even for near-identical
   phrasing.
4. **Case-context-dependent notes** — short administrative or templated
   clinical notes (e.g. "schedule a follow-up appointment") sometimes carry
   a condition label from broader case context that isn't recoverable from
   the single line of text alone. This is a fundamental limitation of
   single-row-text input, not a fixable prompting issue.

See `findings.md` in this repository for the full experimental breakdown.

## License

MIT — see [LICENSE](LICENSE) for details.
