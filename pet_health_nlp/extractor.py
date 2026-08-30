"""
Core extraction function for the pet health NLP tool.

Classifies a short pet health text (owner description or vet clinical-style
note) into one of 5 fixed condition categories and extracts key symptom
keywords, using the Google Gemini API.

This is the locked prompt/disambiguation-rule version validated in
Experiment 3 (1728/2000 matched, 86.4%, full multi-species dataset).
See findings.md in the project docs for the known failure patterns.
"""

import os
import json

from google import genai

_CONDITIONS = [
    "Skin Irritations",
    "Digestive Issues",
    "Parasites",
    "Ear Infections",
    "Mobility Problems",
]

_MODEL_NAME = "gemini-3.1-flash-lite"


def _get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Get a free API key from Google AI Studio and set it before calling "
            "extract_pet_health_info()."
        )
    return genai.Client(api_key=api_key)


def extract_pet_health_info(text: str) -> dict:
    """
    Extract a condition category and symptom keywords from a short pet
    health text.

    Args:
        text: A short pet health description (owner note or vet clinical
            note). The pet may be a cat, dog, ferret, rabbit, or other
            companion animal.

    Returns:
        A dict: {"condition": <one of 5 categories or None>, "keywords": [...]}

    Raises:
        RuntimeError: if GEMINI_API_KEY is not set.
        ValueError: if text is empty or not a string.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")

    client = _get_client()

    prompt = f"""You are extracting structured data from a short pet health text
(the pet could be a cat, dog, ferret, rabbit, or other companion animal).

The "condition" MUST be exactly one of these 5 categories - do not invent new ones,
even if another label seems medically more precise:
- Skin Irritations
- Digestive Issues
- Parasites
- Ear Infections
- Mobility Problems

Use these disambiguation rules when the text is ambiguous between categories:
1. If a skin symptom (scratching, hair loss, scabs, sores, raw spots) is
   described as being CAUSED BY scratching or irritation originating in the
   ear (e.g. "scratching behind her ears," "hair loss from scratching near
   the ear"), prefer "Ear Infections" over "Skin Irritations" - this pattern
   usually indicates an underlying ear condition driving the behavior.
   Do NOT apply this rule to symptoms that are simply located on ear-area
   skin without a scratching/irritation cause (e.g. "scaly patches on ear
   tips" is a primary skin condition, not caused by scratching - leave that
   as "Skin Irritations").
2. Only prefer "Parasites" when a parasite is the CONFIRMED or PRIMARY cause
   being discussed - e.g. a parasite is directly observed (seen in stool, on
   the skin, visible worm), tested and confirmed (positive fecal test,
   diagnosed with Giardia/Coccidia/mites), or the main subject of the text
   (a worm/flea/tick is what the owner is describing or asking about).
   Do NOT prefer "Parasites" just because a parasite is mentioned as one
   possible differential among others (e.g. "consider flea allergy vs food
   allergy" is NOT primarily about parasites - the symptom presentation
   should decide the category in that case).
3. If the text describes neurological/balance symptoms - head tilt, circling,
   loss of balance, stumbling, nystagmus (rapid eye movement), eyes darting -
   prefer "Ear Infections" over "Mobility Problems." These are classic signs
   of inner-ear/vestibular disease, not primary movement problems.

Given the text, return ONLY a JSON object (no markdown, no explanation) with:
- "condition": one of the 5 categories above that best fits, applying the
  disambiguation rules above when relevant
- "keywords": a list of key symptom keywords mentioned in the text

Text: "{text}"

JSON:"""

    response = client.models.generate_content(
        model=_MODEL_NAME,
        contents=prompt,
    )

    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)
