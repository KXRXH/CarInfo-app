import configparser
import os

import ac
import acsys

PATH = os.path.realpath(os.getcwd() + '/apps/python/CarInfo/Data/carsInfo.ini')
config = configparser.ConfigParser()
config.read(PATH)

slips = 0


def odometerUpdate(trip_label, dts, units, trip, delt, uconst):
    global slips
    trip += delt * dts / 3.6
    gs = ac.getCarState(0, acsys.CS.SpeedKMH)
    if uconst == 1.0 and gs > 50:
        slips = ac.getCarState(0, acsys.CS.SlipRatio)
        uconst = gs / dts * (1 + (slips[2] + slips[3]) / 2.0)
        config["CarsUnits"][ac.getCarName(0)] = str(uconst)
        config.write(open(PATH, 'w'))
    current_trip = str(round(units * uconst * trip / 1000, 1))
    if units == 1:
        ac.setText(trip_label, "Trip: {} KMs".format(current_trip))
    else:
        ac.setText(trip_label, "Trip: {} Miles".format(current_trip))
    return trip, uconst
