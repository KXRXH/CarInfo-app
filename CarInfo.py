import json
import os

import ac

import acsys

carName = ac.getCarName(0)
carPATH = os.path.realpath("content/cars/" + carName + '/ui/ui_car.json').replace("\\", "/")
ac.log(carPATH)
speed = 0
gear = 0
rpm = 0
avg_speed = 0
curr_max_Speed = 0
to100 = 0
sr = 0
sr_Speed = 0
boost = 0
with open(carPATH, "r", encoding='utf-8-sig') as read_file:
    data = json.load(read_file)
    carMaxRPM = float(data["torqueCurve"][-1][0])


    def acMain(ac_version):
        global speed, gear, rpm, avg_speed, boost

        appWindow = ac.newApp("CarInfo")
        ac.setSize(appWindow, 150, 240)
        speed = ac.addLabel(appWindow, "KMH:P ")
        avg_speed = ac.addLabel(appWindow, "AVG KMH: ")
        gear = ac.addLabel(appWindow, "Gear: ")
        rpm = ac.addLabel(appWindow, "RPM: ")
        boost = ac.addLabel(appWindow, "Boost: ")

        ac.setPosition(speed, 3, 30)
        ac.setPosition(rpm, 3, 70)
        ac.setPosition(gear, 3, 110)
        ac.setPosition(avg_speed, 3, 190)
        ac.setPosition(boost, 3, 150)

        return "CarInfo"


    def acUpdate(deltaT):
        global speed, gear, rpm, avg_speed, curr_max_Speed, sr, sr_Speed, boost, carName, carMaxRPM

        curr_RPM = ac.getCarState(0, acsys.CS.RPM)

        curr_Speed = ac.getCarState(0, acsys.CS.SpeedKMH)

        curr_Gear = ac.getCarState(0, acsys.CS.Gear)

        curr_boost = ac.getCarState(0, acsys.CS.TurboBoost)

        sr_Speed += round(curr_Speed, 1)
        sr += 1

        if curr_max_Speed < curr_Speed:
            curr_max_Speed = curr_Speed

        if round(curr_Speed) == 0:
            curr_max_Speed = 0
            sr_Speed = 0
            sr = 0
            ac.setVisible(avg_speed, 0)
        else:
            ac.setVisible(avg_speed, 1)
        if curr_boost > 2:
            ac.setFontColor(boost, 1, 0, 0, 1)
        elif 1 < curr_boost < 2:
            ac.setFontColor(boost, 1, 0.9, 0, 1)
        elif curr_boost < 1:
            ac.setFontColor(boost, 1, 1, 1, 1)

        if carMaxRPM - 1250 < curr_RPM:
            ac.setFontColor(rpm, 1, 0, 0, 1)
            if curr_Gear != 1:
                ac.setFontColor(gear, 1, 0, 0, 1)

        elif carMaxRPM - 1250 > curr_RPM > carMaxRPM - 2500:
            ac.setFontColor(rpm, 1, 0.9, 0, 1)
            ac.setFontColor(gear, 1, 1, 1, 1)
        else:
            ac.setFontColor(rpm, 1, 1, 1, 1)
            ac.setFontColor(gear, 1, 1, 1, 1)

        ac.setText(speed, "KMH {}".format(round(curr_Speed, 1)))
        if curr_Gear == 0:
            ac.setText(gear, "Gear {}".format("R"))
        elif curr_Gear == 1:
            ac.setText(gear, "Gear {}".format("N"))
        else:
            ac.setText(gear, "Gear {}".format(curr_Gear - 1))
        ac.setText(boost, "Boost: {}".format(round(curr_boost, 2)))
        ac.setText(rpm, "RPM {}".format(round(curr_RPM)))
        ac.setText(avg_speed, "AVG KMH {}".format(round(sr_Speed / sr, 1)))
