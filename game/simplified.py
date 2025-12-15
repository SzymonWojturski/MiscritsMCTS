from models import Miscrit

class GameState:
    def __init__(self, active_double_flag: bool, active_team: list[Miscrit], opposing_team: list[Miscrit]):
        self.active_team = active_team
        self.opposing_team = opposing_team
        self.active_miscrit = self.active_team[0]
        self.opposing_miscrit = self.opposing_team[0]
        self.active_double_flag = active_double_flag

    #----------mcts-------------
    
    def get_legal_actions(self): 
        #todo zmeinic dodawanie swituch
        return self.active_miscrit.attacks.extend([self.active_team[1:]] if not self.active_miscrit.status.additive["paralyze"] else [])

    def is_game_over(self):
        return self.active_team and self.opposing_team

    def game_result(self):
        return min(1, len(self.active_team))

    def move(self,action):
        dot_phase = self.is_dot_phase()
        self._resolve_action(action)
        if dot_phase:
            self.apply_dot()

    #---------------------------
    
    def _resolve_action(self, action):
        self._make_move(action)
        for addiotional in action["additional"]:
            self._make_move(addiotional)

    def _make_move(self, action):
        action_type = action["type"]

        if action_type in ["Antiheal", "Confuse", "Paralyze", "Sleep"]:
            self.opposing_miscrit.status.add(action_type, action["ap"])
            self.opposing_miscrit.status.add(action_type+"Immunity", action["ap"]+1)

        elif action_type in ["AntihealImmunity", "ConfuseImmunity", "ParalyzeImmunity", "SleepImmunity", "Barbed", "Block", "Etheral", "Negate", "Bleed", "SwitchCurse"]:
            self.active_miscrit.status.add(action_type, action["ap"])

        elif action_type == "Attack":
            self.active_miscrit.deal_damage(action, self.opposing_miscrit)

        elif action_type == "LifeSteal":
            self.active_miscrit.deal_true_damage(action["ap"], self.opposing_miscrit)
            self.active_miscrit.heal(action["ap"])
        
        elif action_type == "Heal":
            self.active_miscrit.heal(action["ap"])
        
        elif action_type == "Buff":
            for stat in action[action_type]["keys"]:
                self.active_miscrit.status.add(stat,action["ap"])
        



        match action_type:
            case "Bot":
            case "Cleanser":
            case "Dot":
            case "ForceSwitch":
            case "Heal":
            case "Hot":
            case "Poison":
            case "Purge":
            case "Special":
            case "StatsSteal":
            case "Suprise":
                pass

    def is_dot_phase(self):
        return not self.is_opponent_faster()

    def is_opponent_faster(self):
        return self.opposing_miscrit.speed > self.active_miscrit.speed

    def apply_dot(self):
        self.opposing_miscrit.apply_dot(self.active_miscrit)
        self.active_miscrit.apply_dot(self.opposing_miscrit)

    def next_state(self):
        if not self.active_double_flag and not self.is_opponent_faster():
            return GameState(
                active_double_flag=True,
                active_team=self.active_team,
                opposing_team=self.opposing_team
            )

        return GameState(
            active_double_flag=not self.active_double_flag,
            active_team=self.opposing_team,
            opposing_team=self.active_team
        )



    #---------------------------

    def _switch_to(self, new_miscrit: Miscrit):
        team = self.active_team
        old_active = self.active_team[0]

        if new_miscrit not in team:
            return

        remaining = [m for m in team if m is not new_miscrit and m is not old_active]

        self.active_team = [new_miscrit] + remaining + [old_active]
        self.active_miscrit = self.active_team[0]

    
