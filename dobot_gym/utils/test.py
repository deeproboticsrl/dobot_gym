from dobot_gym.utils.dobot_controller import DobotController

dobot = DobotController()
print("cmd")
# dobot.continuousCMD(50,0,0)
print(dobot.get_dobot_joint())
dobot.moveangleinc(0,50,0)
print(dobot.get_dobot_joint())
dobot.disconnect()
