import json
from pathlib import Path


def extract_elements(page):
    return page.locator("input, select, textarea, button").evaluate_all("""
        elements => elements.map(element => ({
            tag: element.tagName.toLowerCase(),
            type: element.type || null,
            name: element.name || null,
            id: element.id || null,
            placeholder: element.placeholder || null,
            required: element.required || false,
            visible: !!(element.offsetWidth || element.offsetHeight || element.getClientRects().length)
        }))
    """)


def save_elements(elements):
    path = Path(__file__).resolve().parents[1] / "data" / "campos_extraidos.json"
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(elements, file, ensure_ascii=False, indent=2)
