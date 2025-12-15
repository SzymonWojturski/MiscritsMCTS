
ADDITIVE_NAMES = ["spd", "ea", "pa", "ed", "pd", "acc", "Paralyze", "ParalyzeImmunity", "Sleep", "SleepImmunity", "Confuse", "ConfuseImmunity", "Antiheal", "AntihealImmunity"]
DOMINANT_NAMES = ["Negate", "Barbed", "Shield", "Ethereal"]
SCALING_NAMES = ["Bleed", "SwitchCurse"]

class Status:
    def __init__(self):
        self.additive = {s: 0 for s in ADDITIVE_NAMES}
        self.dominant = {s: 0 for s in DOMINANT_NAMES}
        self.scaling = {s: {"turns": 0, "dmg": 0} for s in SCALING_NAMES}
        self.dot = {}

    def add(self, name, ap):
        if name in ADDITIVE_NAMES:
            immunity = f"{name}Immunity"
            if immunity in self.additive and self.additive[immunity]:
                return
            self.additive[name] += ap
            return

        if name in DOMINANT_NAMES:
            self.dominant[name] = max(self.dominant[name], ap)
            return

        if name in SCALING_NAMES:
            self.scaling[name]["turns"] = max(self.scaling[name]["turns"], ap)
            return

        raise AttributeError(name)
    
    def add_dot(self):
        pass

