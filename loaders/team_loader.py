import json
import re
from models import Miscrit, BasicTypes, Status, Stats
from .stats_values import hp_value_of, stat_value_of

def normalize_status_name(name: str) -> str:
    STATUS_NAME_MAP = {
        "AI": "AntihealImmunity",
        "SI": "SleepImmunity",
        "PI": "ParalyzeImmunity",
        "CI": "ConfuseImmunity",
    }
    return STATUS_NAME_MAP.get(name, name)

def fix_attack(attack):
    attack_type = attack["type"]
    
    match attack_type:
        case 'CI' | 'SI': 
            attack["ap"] = 5
        case "Cleanser":
            attack["accuracy"] = 100
        case _ :
            pass

def enchant_attack(attack):
    enchant = attack["enchant"]

    for key, val in enchant.items():
        match key:
            case "ap" | "accuracy" | "times" | "turns": 
                attack[key] += val
            case "additional":
                if key not in attack:
                    attack[key] = []
                attack[key].extend(val)
            case _ :
                print(key, val)

def parse_types(value: str) -> list[BasicTypes]:
    parts = re.findall(r"[A-Z][a-z]+", value)

    result = []
    for p in parts:
        for t in BasicTypes:
            if t.value == p:
                result.append(t)
                break
    return result


def build_miscrit(raw):
    name = raw["names"][0]
    types = parse_types(raw["element"])

    base_stats = {
        "hp": raw["hp"],
        "speed": raw["spd"],
        "ea": raw["ea"],
        "pa": raw["pa"],
        "ed": raw["ed"],
        "pd": raw["pd"],
    }

    stats = Stats(
        hp_value_of(base_stats["hp"]),
        stat_value_of(base_stats["speed"]),
        stat_value_of(base_stats["ea"]),
        stat_value_of(base_stats["pa"]),
        stat_value_of(base_stats["ed"]),
        stat_value_of(base_stats["pd"]),
    )

    attacks = raw["abilities"]
    for attack in attacks:
        fix_attack(attack)
        enchant_attack(attack)

        if "type" in attack:
            attack["type"] = normalize_status_name(attack["type"])

        if "additional" in attack:
            for add in attack["additional"]:
                if "type" in add:
                    add["type"] = normalize_status_name(add["type"])

        attack["cooldown"] = 0
    print(raw)

    return Miscrit(name, types, stats, status=Status(), attacks=attacks)

def load_database(path="miscrits.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_team(ids, db):
    idset = set(ids)
    raw_list = [m for m in db if m["id"] in idset]
    return [build_miscrit(m) for m in raw_list]
