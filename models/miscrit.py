from . import Status, BasicTypes

COUNTER_BONUS = 1.25
WEAKNESS_PENALTY = 0.75
NORMAL_MULTIPLIER = 1.0

class Stats:
    def __init__(self, hp, speed, ea, pa, ed, pd):
        self.hp = hp
        self.speed = speed
        self.ea = ea
        self.pa = pa
        self.ed = ed
        self.pd = pd

STAT_NAMES = ["hp", "speed", "ea", "pa", "ed", "pd"]

class Miscrit:
    def __init__(self, name:str, types:list[BasicTypes], stats:Stats, status:Status, attacks:list):
        self.name = name
        self.types = types
        self.base_stats = stats
        self.status = status
        self.attacks = attacks 
    
    def get_stat(self, name: str):
        base = getattr(self.base_stats, name)
        add  = self.status.additive[name]

        value = base + add

        return max(value, 0)

    def __getattr__(self, name):
        if name in STAT_NAMES:
            return self.get_stat(name)
        raise AttributeError(name)
    
    def heal(self, ammount):
        if self.status.additive["anti_heal"]:
            self.base_stats.hp -= ammount
        else:
            self.base_stats.hp += ammount
            try:
                self.status.scaling.pop("bleed")
            except Exception as e:
                print(e)

    def deal_damage(self, basic_attack, target: "Miscrit"):
        if basic_attack.type == BasicTypes.PHYSICAL:
            atk_stat = self.pa
            def_stat = target.pd
        else:
            atk_stat = self.ea
            def_stat = target.ed

        base = basic_attack.damage * (atk_stat / def_stat)
        multiplier = NORMAL_MULTIPLIER

        if any(basic_attack.type.counters(t) for t in target.types):
            multiplier = COUNTER_BONUS
        elif any(t.get_counter_by(basic_attack.type) for t in target.types):
            multiplier = WEAKNESS_PENALTY

        dmg = base * multiplier
        target.base_stats.hp -= dmg
        target.status.additive["sleep"] = 0

    def deal_true_damage(self, dmg, target: "Miscrit"):
        if target.status.dominant["Etheral"]:
            target.status.dominant["Etheral"]-=1
            return

        target.base_stats.hp -= dmg
        target.status.additive["sleep"] = 0

    def apply_dot(self, other:"Miscrit"):

        for dot in self.status.dot:
            if dot.type == BasicTypes.INSTA_HEAL:
                self.heal(dot.damage)

        for dot in self.status.dot:
            if dot.type != BasicTypes.INSTA_HEAL:
                key = (dot.type, dot.damage)
                other.deal_damage(atack.BasicAttack(dot.type, dot.damage), self)

                if key in other.status.dot:
                    self.status.dot[key] = self.status.dot[key] - 1
                else:
                    self.status.dot.pop(key)

        for name, data in self.status.scaling.items():
            if data["turns"]:
                self.base_stats.hp = self.base_stats.hp - data["dmg"]
                self.status.scaling[name]["turns"] -= 1
                self.status.scaling[name]["dmg"] = max(16, data["dmg"] + 4)           


    def make_attack(self, attack , other: "Miscrit"):
        for basic in attack.basic_attacks:
            self.deal_damage(basic, other)

        for status in attack.enemy_status:
            other.status += status

        for status in attack.self_status:
            self.status += status

        if attack.insta_heal:
            self.heal(attack.insta_heal)

    def is_dead(self):
        return self.base_stats.hp > 0

    def __str__(self):
        return f"{self.name}: {self.base_stats.hp}, attacks:{self.attacks}"
