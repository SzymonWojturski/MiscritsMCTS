from enum import Enum, auto


class BasicTypes(Enum):
    INSTA_HEAL = auto
    PHYSICAL = auto
    FIRE = "Fire" 
    WATER = "Water"
    NATURE = "Nature"
    EARTH = "Earth"
    WIND = "Wind"
    LIGHTNING = "Lightning"
    PIOSON = auto

    def get_counter_by(self, other: "BasicTypes") -> bool:
        rules = {
            BasicTypes.FIRE:      [BasicTypes.WATER],
            BasicTypes.WATER:     [BasicTypes.NATURE],
            BasicTypes.NATURE:    [BasicTypes.FIRE],
            BasicTypes.EARTH:     [BasicTypes.WIND],
            BasicTypes.WIND:      [BasicTypes.LIGHTNING],
            BasicTypes.LIGHTNING: [BasicTypes.EARTH],
            BasicTypes.PHYSICAL:  [],
        }
        return other in rules[self]


    def counters(self, other: "BasicTypes") -> bool:
        rules = {
            BasicTypes.FIRE:      [BasicTypes.NATURE],
            BasicTypes.WATER:     [BasicTypes.FIRE],
            BasicTypes.NATURE:    [BasicTypes.WATER],
            BasicTypes.EARTH:     [BasicTypes.LIGHTNING],
            BasicTypes.WIND:      [BasicTypes.EARTH],
            BasicTypes.LIGHTNING: [BasicTypes.WIND],
            BasicTypes.PHYSICAL:  [],
        }
        return other in rules[self]


