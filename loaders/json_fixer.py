import json
import re

DEFAULT_AP = {
    "Attack": 10,
    "Special": 10,
    "Surprise": 10,
    "Heal": 5,
    "Hot": 5,
    "LifeSteal": 5,
    "Poison": 3,
    "Bleed": 3,
    "Dot": 3,
    "Barbed": 3,
    "Buff": 5,
    "Debuff": 5,
    "Confuse": 3,
    "Sleep": 3,
    "Paralyze": 3,
    "Block": 10,
    "Negate": 1,
    "Cleanser": 1,
    "Purge": 1,
    "ForceSwitch": 1,
    "SwitchCurse": 4,
    "StatSteal": 5,
    "Antiheal": 4,
    "Bot": 5,
    "Ethereal": 2,
}

def normalize_status_name(name: str) -> str:
    STATUS_NAME_MAP = {
        "AI": "Antiheal",
        "SI": "Sleep",
        "PI": "Paralyze",
        "CI": "Confuse",
    }
    return STATUS_NAME_MAP.get(name, name)

def apply_default_ap(obj):
    if "ap" not in obj:
        obj["ap"] = DEFAULT_AP.get(obj.get("type"), 0)

def apply_debuff_fix(attack):
    if attack.get("type") == "Buff" and attack.get("ap", 0) < 0:
        attack["type"] = "Debuff"
        attack["target"] = "Enemy"

def parse_types(value: str):
    return re.findall(r"[A-Z][a-z]+", value)

def normalize_attack(obj):
    if "type" in obj:
        obj["type"] = normalize_status_name(obj["type"])
    apply_default_ap(obj)
    if "cooldown" not in obj:
        obj["cooldown"] = 0
    obj.pop("accuracy", None)
    obj.pop("enchant", None)
    obj.pop("enchant_desc", None)
    obj.pop("desc", None)

def build_miscrit(raw):
    raw = dict(raw)
    raw["name"] = raw["names"][0]
    raw["types"] = parse_types(raw["element"])
    raw.pop("descriptions", None)
    raw.pop("locations", None)

    attacks = raw.get("abilities", [])
    for attack in attacks:
        normalize_attack(attack)
        apply_debuff_fix(attack)

        if "additional" in attack:
            for add in attack["additional"]:
                normalize_attack(add)

    raw["abilities"] = attacks
    return raw

def load_database(path="miscrits.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_database(data, path="miscrits_fixed.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    db = load_database("miscrits.json")
    fixed = [build_miscrit(m) for m in db]
    save_database(fixed, "miscrits_fixed.json")
