import random

def getInput(prompt=""):
    buffer = input(prompt)
    buffer = buffer.lower().split(" ")
    return buffer

def rollDice(dice):
    buffer = 0
    splice = dice.split("d")
    for _ in range(int(splice[0])):
        buffer += random.randint(1, int(splice[1]))
    return buffer

class Commands:
    def __init__(self):
        self.commands = {
            "1": self.attack,
            "2": self.check, 
        }

    def execute(self, args):
        command = args[0]

        commandFunction = self.commands.get(command)
        if commandFunction:
            commandFunction(args[1:])
        else:
            print("Unknown command:", command)
    
    def attack(self, args):
        # Data
        attackResults = []
        acValues = []
        acRolls = []
        acRollsWeighted = []
        rollType = 0

        print("Attack damage? (1d6, 2d8, etc...)")
        userInput = getInput()
        attackDamage = userInput

        userInput = getInput("Flat bonus? ")
        flatDamageBonus = int(userInput[0])

        userInput = getInput("Attack amount? ")
        attackAmount = int(userInput[0])

        print("Armor Class Check?")
        userInput = getInput("(y/n) ")
        armorClassCheck = userInput[0] == "y"
        if armorClassCheck:
            userInput = getInput("Armor Class Value? ")
            acValues = [int(x) for x in userInput]

            userInput = getInput("Flat bonus? ")
            flatBonus = int(userInput[0])

            userInput = getInput("Roll with advantage/disadvantage/none? (+,-,0) ")
            rollType = int(userInput[0])

            # Calculate AC rolls
            if rollType == 0:
                for _ in range(attackAmount):
                    acRollsWeighted.append(random.randint(1, 20) + flatBonus)
            else:
                for _ in range(attackAmount):
                    acBuffer = []
                    for _ in range(abs(rollType)):
                        acBuffer.append(random.randint(1, 20) + flatBonus)
                    acRolls.append(acBuffer)
                    if rollType > 0:
                        acRollsWeighted.append(max(acBuffer))
                    elif rollType < 0:
                        acRollsWeighted.append(min(acBuffer))

        # Calculate attack rolls
        for i in range(attackAmount):
            attackResult = 0
            for dice in attackDamage:
                attackResult += rollDice(dice)
            
            if armorClassCheck:
                if acRollsWeighted[i] < acValues[i]:
                    continue
            
            attackResults.append(attackResult + flatDamageBonus)

        # Print results
        print("=========================")
        print("Result of Attack Roll:")
        print("Attack Damage:", attackDamage)
        print("Flat Damage Bonus", flatDamageBonus)
        print("Attack Amount:", attackAmount)
        print("=========================")
        print("Armor Class Check?:", armorClassCheck)
        if armorClassCheck:
            print("Armor Class Values:", acValues)
            print("Flat Bonus:", flatBonus)
            print("Advantage:", rollType)
            print("AC Rolls:", acRolls)
            print("AC advantage/disadvantage rolls", acRollsWeighted)
        print("=========================")
        print("Attack Results:", attackResults)
        print("Total Damage:", sum(attackResults))
        print("=========================")
        getInput("Enter to continue... ")
    
    def check(self, args):
        # Data
        checkRolls = []
        checkRollsWeighted = 0

        userInput = getInput("Roll with advantage/disadvantage/none? (+,-,0) ")
        rollType = int(userInput[0])

        userInput = getInput("Flat bonus? ")
        flatBonus = int(userInput[0])

        if rollType == 0:
            checkRollsWeighted = random.randint(1, 20) + flatBonus
        else:
            for _ in range(abs(rollType)):
                checkRolls.append(random.randint(1, 20) + flatBonus)
                if rollType > 0:
                    checkRollsWeighted = max(checkRolls)
                elif rollType < 0:
                    checkRollsWeighted = min(checkRolls)
        
        print("=========================")
        print("Results of Check Roll:")
        print("Flat Bonus:", flatBonus)
        print("Advantage:", rollType)
        print("Check Rolls:", checkRolls)
        print("Check advantage/disadvantage rolls:", checkRollsWeighted)
        print("=========================")
        print("Check Result:", checkRollsWeighted)
        print("=========================")
        getInput("Enter to continue... ")

        


            

            




def main():
    commands = Commands()
    while True:
        print("emoji ta")
        print("1. Attack")
        print("2. Check")
        userInput = getInput("> ")

        commands.execute(userInput)






if __name__ == "__main__":
    main()