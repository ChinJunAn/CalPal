def inform(net_calories):
    if abs(net_calories) < 100:
        return str(net_calories) + " Calories\n\nGood job at balancing your Calories, keep it up!"
    elif net_calories > 100:
        return str(net_calories) + " Calories\n\nYou are consuming more than you are burning. You could run for " + str(calculateRun(net_calories)) + " minutes to burn off the excess Calories."
    elif net_calories < (-100):
        return str(net_calories) + " Calories\n\nGood job at burning off excess Calories! You can rewards yourself with " + str(calculateReward(net_calories)) + "g of apple without worrying:))"
    
def calculateReward(net_calories):
     return int(-(net_calories) / 59 / 100)

def calculateRun(net_calories):
    return int(net_calories / ((7.5 * 3.5 * 65) / 200))
    
