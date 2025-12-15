
def hp_value_of(name:str):
    match name:
        case "Weak":
            return 162
        case "Moderate":
            return 176
        case "Strong":
            return 190
        case "Max":
            return 104
        case "Elite":
            return 218

def stat_value_of(name:str):
    match name:
        case "Weak":
            return 83
        case "Moderate":
            return 95
        case "Strong":
            return 106
        case "Max":
            return 118
        case "Elite":
            return 130
