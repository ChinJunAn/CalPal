import calories_in.variables as ciVariables

def inform(net_calories):
    if abs(net_calories) < 100:
        return str(net_calories) + " Calories\n\nGood job at balancing your Calories, keep it up!"
    elif net_calories > 100:
        run = str(calculateRun())
        return str(net_calories) + " Calories\n\nYou are consuming more than you are burning. You could run for " + run + "mins to burn off the excess Calories."
    elif net_calories < (-100):
        reward = str(calculateReward())
        return str(net_calories) + " Calories\n\nGood job at burning off excess Calories! You can rewards yourself with " + reward + "g of apple without worrying:))"
    
def calculateReward(net_calories):
    ciVariables.calories_table["apple"]
    return

def calculateRun(net_calories):
    return
