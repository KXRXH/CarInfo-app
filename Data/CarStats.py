import ac
import acsys


def getCarStats():
    curr_RPM = ac.getCarState(0, acsys.CS.RPM)
    curr_Speed = ac.getCarState(0, acsys.CS.SpeedKMH)
    curr_Gear = ac.getCarState(0, acsys.CS.Gear)
    curr_boost = ac.getCarState(0, acsys.CS.TurboBoost)
    curr_dts = ac.getCarState(0, acsys.CS.DriveTrainSpeed)

    return [curr_Speed, curr_RPM, curr_Gear, curr_boost, curr_dts]


def carStatsOutput(boost_label, gear_label, rpm_label, speed_label, maxRPM, scaleTurbo=1, scaleSpeed=1):
    curr_RPM = ac.getCarState(0, acsys.CS.RPM)

    curr_Speed = ac.getCarState(0, acsys.CS.SpeedKMH) * scaleSpeed

    curr_Gear = ac.getCarState(0, acsys.CS.Gear)

    curr_boost = ac.getCarState(0, acsys.CS.TurboBoost)

    if curr_boost > 2:
        ac.setFontColor(boost_label, 1, 0, 0, 1)
    elif 1 < curr_boost < 2:
        ac.setFontColor(boost_label, 1, 0.9, 0, 1)
    elif curr_boost < 1:
        ac.setFontColor(boost_label, 1, 1, 1, 1)

    if maxRPM - 500 < curr_RPM:
        ac.setFontColor(rpm_label, 1, 0, 0, 1)
        if curr_Gear != 1:
            ac.setFontColor(gear_label, 1, 0, 0, 1)

    elif maxRPM - 500 > curr_RPM > maxRPM - 1250:
        ac.setFontColor(rpm_label, 1, 0.9, 0, 1)
        ac.setFontColor(gear_label, 1, 1, 1, 1)

    else:
        ac.setFontColor(rpm_label, 1, 1, 1, 1)
        ac.setFontColor(gear_label, 1, 1, 1, 1)
    if scaleTurbo == 1:
        ac.setText(boost_label, "Boost: {} bar".format(round(curr_boost * scaleTurbo, 2)))
    else:
        ac.setText(boost_label, "Boost: {} psi".format(round(curr_boost * scaleTurbo, 2)))
    ac.setText(rpm_label, "RPM: {}".format(round(curr_RPM)))
    if scaleSpeed == 1:
        ac.setText(speed_label, "KM/H: {}".format(round(curr_Speed, 1)))
    else:
        ac.setText(speed_label, "MP/H: {}".format(round(curr_Speed, 1)))
    if curr_Gear == 0:
        ac.setText(gear_label, "Gear: {}".format("R"))
    elif curr_Gear == 1:
        ac.setText(gear_label, "Gear: {}".format("N"))
    else:
        ac.setText(gear_label, "Gear: {}".format(curr_Gear - 1))
