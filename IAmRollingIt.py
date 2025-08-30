import random
import os
import cmd
import json

mainDir = "RollData"
attackDir = "RollData/AttackData"
checkDir = "RollData/CheckData"

class DiceRoll(cmd.Cmd):
        intro = 'I am rolling it so hard.   Type help or ? to list commands.\n'
        prompt = 'IAmRollingIt> '

        def do_attack(self, args):
            """Says hello to the given name."""
            Attack().cmdloop()
            

        def do_quit(self, args):
            """Exits the dice roller."""
            print("kys")
            return True # Returning True exits the interpreter
        
class Attack(cmd.Cmd):
        intro = 'Attack mode enabled.\n'
        prompt = 'Attack Mode> '

        data = {
            "Attack-Damage": "None",
            "Flat-Damage": "None",
            "Attack-Amount": "None",
            "Crit-Threshold" : "None",

            "Armor-Class": "None",
            "Attack-Roll-Bonus": "None",
            "Attack-Roll-Advantage": "None",
        }

        def do_roll(self, args):
            """Roll with the current settings"""
            # Get data
            attackDamage = self.data["Attack-Damage"].split(",")
            flatDamage = int(self.data["Flat-Damage"])
            attackAmount = int(self.data["Attack-Amount"])
            critThreshold = int(self.data["Crit-Threshold"])

            armorClass = int(self.data["Armor-Class"]) if self.data["Armor-Class"] != "None" else "None"
            attackRollBonus = int(self.data["Armor-Class"])
            attackRollAdvantage = int(self.data["Armor-Class"])

            # Calculated Data
            attackRawResult = []
            attackResult = []

            attackRollRawResult = []
            attackRollResult = []
            attackRollCrit = []
            
            # Calculate attack raw result
            for _ in range(attackAmount):
                buffer = flatDamage
                for dice in attackDamage:
                    buffer += rollDice(dice)
                attackRawResult.append(buffer)
            
            # Roll for attack
            for _ in range(attackAmount):
                buffer = []
                for _ in range(1 + abs(attackRollAdvantage)):
                    buffer.append(rollDice("1d20"))
                attackRollRawResult.append(buffer)
            
            # filter highest/lowest based on advantage
            for attackRoll in attackRollRawResult:
                selectedRoll = max(attackRoll) if attackRollAdvantage >= 0 else min(attackRoll)
                attackRollCrit.append(selectedRoll >= critThreshold)
                attackRollResult.append(selectedRoll + attackRollBonus)

            # filter damage
            for i in range(len(attackRollResult)):
                attackRoll = attackRollResult[i]
                attackCrit = attackRollCrit[i]

                if attackCrit:
                    #get max dice roll
                    buffer = flatDamage
                    for dice in attackDamage:
                        buffer += maxDice(dice)
                    attackResult.append(buffer)
                    continue
                elif attackRoll >= armorClass:
                    attackResult.append(attackRawResult[i])
                else:
                    attackResult.append(0)

            print("=========================")
            print("Result of Attack Roll:")
            print("Attack Damage:", attackDamage)
            print("Flat Damage Bonus", flatDamage)
            print("Attack Amount:", attackAmount)
            print("Crit Threshold:", critThreshold)
            print("=========================")
            print("Armor Class Value:", armorClass)
            print("Attack Roll Flat Bonus:", attackRollBonus)
            print("Attack Roll Advantage:", attackRollAdvantage)
            print("Attack Rolls Raw:", attackRollRawResult)
            print("Attack Rolls", attackRollResult)
            print("=========================")
            print("Attack Raw Results:", attackRawResult)
            print("Attack Results:", attackResult)
            print("Total Damage:", sum(attackResult))
            print("=========================")




        def do_show(self, args):
            """Show the current settings or show specific value of a property"""
            args = args.split(" ")

            if len(args) == 0 or args[0] == "":
                for key in list(self.data.keys()):
                    print(f"{key}: {self.data[key]}")
            else:
                value = self.data.get(args[0])
                if value == None:
                    print(f"Property '{args[0]}' is not found")
                    return
                
                print(f"{args[0]}: {value}")

        def do_set(self, args):
            """Set the value of something"""
            args = args.split(" ")
            value = self.data.get(args[0])

            if value == None:
                print("Property not found")
                return False
            
            self.data[args[0]] = args[1]
            print(f"Property '{args[0]}' is set from {value} to {args[1]}")

        def do_save(self, args):
            """Save the current setting to a file"""
            args = args.split(" ")

            with open(f"{attackDir}/{args[0]}.json", "w") as fp:
                json.dump(self.data, fp)

        def do_load(self, args):
            """Load a setting from a file"""

            args = args.split(" ")

            with open(f"{attackDir}/{args[0]}.json", "r") as fp:
                self.data = json.load(fp)

        def do_quit(self, args):
            """Exits attack mode."""
            print("kys")
            return True # Returning True exits the interpreter

def rollDice(dice):
    buffer = 0
    splice = dice.split("d")
    for _ in range(int(splice[0])):
        buffer += random.randint(1, int(splice[1]))
    return buffer

def maxDice(dice):
    splice = dice.split("d")
    return int(splice[0]) * int(splice[1])

def init():
    try:
        os.mkdir(mainDir)
    except:
        pass

    try:
        os.mkdir(attackDir)
    except:
        pass

    try:
        os.mkdir(checkDir)
    except:
        pass

def main():
    DiceRoll().cmdloop()
    pass

if __name__ == "__main__":
    init()
    main()