from loaders import load_database, build_team

if __name__ == "__main__":
    MISCRIT_DB = load_database("miscrits.json")

    team = build_team(range(len(MISCRIT_DB)), MISCRIT_DB)
   
