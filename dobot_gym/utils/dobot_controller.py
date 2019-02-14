import time
from sys import exit

import dobot_gym.utils.DobotDllType as dType


class DobotController:

    def __init__(self, port="ttyUSB0"):
        self.DEFINED_HOME = (206, 0, 135, 0)
        # self.DEFINED_HOME = (190,58,146,17)
        CON_STR = {
            dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

        self.api = dType.load()
        print("Loaded API")
        state = dType.ConnectDobot(self.api, port, 115200)[0]
        print("Connect status:", CON_STR[state])

        if (state == dType.DobotConnect.DobotConnect_Occupied):
            print("Error - Dobot Can't Connect")
            print("Possible Problems - ")
            print("1) Wrong Port. Pls check /dev and use the correct port.")
            print(
                "2) User doesn't have required priveleges for the port. Pls add user to dialout group or use chmod on the port.")
            print("3) Robot wasn't disconnected properly. Pls restart the robot and replug the USB and try again.")
            exit()
        if (state == dType.DobotConnect.DobotConnect_NoError):
            print("Connected.")
            # Clean Command Queued
            dType.SetQueuedCmdClear(self.api)

            # Async Motion Params Setting
            dType.SetHOMEParams(self.api, 206, 0, 135, 0, isQueued=1)  # set home co-ordinates  [x,y,z,r]
            # dType.SetPTPJointParams(self.api, 100, 100, 100, 100, 100, 100, 100, 100,
            #                         isQueued=1)  # joint velocities(4) and joint acceleration(4)
            print(1)
            dType.SetPTPCommonParams(self.api, 90, 90, isQueued=1)  # velocity ratio, acceleration ratio
            print(2)
            dType.SetPTPJumpParams(self.api, 30, 135, isQueued=1)  # jump height , zLimit
            print(3)
            dType.SetPTPJointParams(self.api, 50, 50, 50, 50, 50, 50, 50, 50, isQueued=1)
            print(4)
            # dType.SetJOGJointParams(self.api, 10, 10, 10, 10, 10, 10, 10, 10, isQueued=1)
            # dType.SetJOGCoordinateParams(self.api, 100, 100, 100, 100, 100, 100, 100,100, isQueued=1)

            # lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVJXYZMode, 212, -83, 20, 100, isQueued=1)[0]
            #   # mode, x,y,z,r
            print ("start moving")
            lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVJXYZMode, *self.DEFINED_HOME, isQueued=1)[0]
            print ("got initial command")
            dType.SetQueuedCmdStartExec(self.api)
            print("step1")
            while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                print("step2")
                dType.dSleep(500)
                # print(dType.GetQueuedCmdCurrentIndex(self.api))
            # print(lastIndex)
            # print(lastIndex)
            dType.SetQueuedCmdStopExec(self.api)
            dType.SetQueuedCmdClear(self.api)
            print ("Done moving to home")

    def disconnect(self):
        try:
            dType.DisconnectDobot(self.api)
            print("Disconnected")
        except:
            pass



    def moveangleinc(self, x, y, z, r=0, q=1):
        if q == 1:
            lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVJANGLEINCMode, x, y, z, r, isQueued=1)[0]
            dType.SetQueuedCmdStartExec(self.api)

            while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                # print(f"{dType.GetQueuedCmdCurrentIndex(self.api)} :current index")
                # print(dType.GetQueuedCmdCurrentIndex(self.api))
                dType.dSleep(500)
                # Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(self.api)
            dType.SetQueuedCmdClear(self.api)
        else:
            dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVJANGLEINCMode, x, y, z, r, isQueued=0)

    def movexyz(self,x,y,z,r=0,q=1):
        if q == 1:
            lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVJXYZMode, *self.DEFINED_HOME, isQueued=1)[0]
            dType.SetQueuedCmdStartExec(self.api)

            while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                # print(f"{dType.GetQueuedCmdCurrentIndex(self.api)} :current index")
                # print(dType.GetQueuedCmdCurrentIndex(self.api))
                dType.dSleep(500)
                # Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(self.api)
            dType.SetQueuedCmdClear(self.api)
        else:
            dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVJANGLEINCMode, x, y, z, r, isQueued=0)

    def jog(self, cmd, isJoint=1, q=1):
        ##  Jogging Mode isJoint 0: Cartesian Coordinate System
        ##                       1 : Joint Coordinate System
        ## cmd :joint coordinate: joint1+/- joint2+/- joint3 +/- joint4+/-
        ##cmd: cartesian :X +/- Y +/- Z +/- R+/- L+/-
        if q == 1:
            lastIndex = dType.SetJOGCmd(self.api, isJoint=isJoint, cmd=cmd, isQueued=1)
            print("Command executed")
            dType.SetQueuedCmdStartExec(self.api)
            while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                # print(f"{dType.GetQueuedCmdCurrentIndex(self.api)} :current index")
                # print(dType.GetQueuedCmdCurrentIndex(self.api))
                dType.dSleep(500)
                # Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(self.api)
            dType.SetQueuedCmdClear(self.api)

        elif q == 0:
            dType.SetJOGCmd(self.api, isJoint=isJoint, cmd=cmd, isQueued=0)
        else:
            print("enter q=0 or 1 for isQueued")

    def grip(self, grip=0, t=0.5, q=0):
        if q == 1:
            if grip == 0:
                lastIndex = dType.SetEndEffectorGripper(self.api, 1, grip, isQueued=1)[0]  # control,enable/disable

                dType.SetQueuedCmdStartExec(self.api)

                while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                    dType.dSleep(500)
                time.sleep(t)
                # Stop to Execute Command Queued
                dType.SetQueuedCmdStopExec(self.api)
                dType.SetQueuedCmdClear(self.api)

                lastIndex = dType.SetEndEffectorGripper(self.api, 0, grip, isQueued=1)[0]  # control,enable/disable
                dType.SetQueuedCmdStartExec(self.api)

                while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                    dType.dSleep(500)
                time.sleep(t)
                # Stop to Execute Command Queued
                dType.SetQueuedCmdStopExec(self.api)
                dType.SetQueuedCmdClear(self.api)
            else:
                lastIndex = dType.SetEndEffectorGripper(self.api, 1, grip, isQueued=1)[0]  # control,enable/disable

                dType.SetQueuedCmdStartExec(self.api)

                # while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                #     dType.dSleep(500)
                time.sleep(t)
                # Stop to Execute Command Queued
                dType.SetQueuedCmdStopExec(self.api)
                dType.SetQueuedCmdClear(self.api)
        else:
            dType.SetEndEffectorGripper(self.api, 1, grip, isQueued=0)
            time.sleep(t)
            dType.SetEndEffectorGripper(self.api, 0, grip, isQueued=0)

    def get_dobot_joint(self):
        # return float x, float y,float z, float r, float joint1,...joint 4
        poses = dType.GetPose(self.api)
        return poses

    def continuousCMD(self,x,y,z):
        lastIndex = dType.SetCPCmd(self.api,cpMode=0,x=x,y=y,z=z,isQueued=1,velocity=100)[0]
        dType.SetQueuedCmdStartExec(self.api)
        # print (lastIndex)
        while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
            dType.dSleep(500)
            # Stop to Execute Command Queued
        dType.SetQueuedCmdStopExec(self.api)
        dType.SetQueuedCmdClear(self.api)

if __name__== '__main__':
    ob = DobotController()
