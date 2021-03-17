import configparser
import os
import platform
import sys

import ac

from Data.CarPerfomanceTest import avgSpeedTest
from Data.CarStats import carStatsOutput, getCarStats
from Data.Odometer import odometerUpdate

if platform.architecture()[0] == "64bit":
    libdir = "stdlib/lib64"
else:
    libdir = "stdlib/lib"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."
from stdlib.sim_info import info

PATH = os.path.realpath(os.getcwd() + '/apps/python/CarInfo/config.ini')
config = configparser.ConfigParser()
config.read(PATH)
carconfig = configparser.ConfigParser()
carconfig.read(os.path.realpath(os.getcwd() + '/apps/python/CarInfo/Data/carsInfo.ini'))
scaleSpeed = 1 if config["Scales"]["Speed"][0] == "0" else 0.609
scaleTurbo = 1 if config["Scales"]["TurboPressure"][0] == "0" else 14.504
try:
    try:
        uconst = float(carconfig["CarsUnits"][ac.getCarName(0)])
    except ValueError:
        uconst = 1
except KeyError:
    uconst = 1
count = 0
Avg_Speed = 0
speed = None
gear = None
rpm = None
avg_speed = None
boost = None
resetBtn = None
odomTrip = None
trip = 0


def acMain(ac_version):
    global speed, gear, rpm, avg_speed, boost, resetBtn, odomTrip
    MainWindow = ac.newApp("CarInfo")
    PerformanceWindow = ac.newApp("Performance")
    ac.setBackgroundOpacity(MainWindow, 0.3)
    ac.setSize(MainWindow, 150, 150)
    ac.setSize(PerformanceWindow, 150, 150)
    speed = ac.addLabel(MainWindow, "KMH: None ")
    avg_speed = ac.addLabel(PerformanceWindow, "AVG KMH: None")
    gear = ac.addLabel(MainWindow, "Gear: None")
    rpm = ac.addLabel(MainWindow, "RPM: None")
    boost = ac.addLabel(MainWindow, "Boost: None")
    resetBtn = ac.addButton(PerformanceWindow, "Reset")
    odomTrip = ac.addLabel(PerformanceWindow, "test:")
    ac.setSize(resetBtn, 30, 20)
    ac.addOnClickedListener(resetBtn, resetAVG)

    ac.setIconPosition(MainWindow, 0, -10000)
    ac.setIconPosition(PerformanceWindow, 0, -10000)

    ac.setPosition(odomTrip, 3, 60)
    ac.setPosition(speed, 3, 30)
    ac.setPosition(rpm, 3, 60)
    ac.setPosition(gear, 3, 90)
    ac.setPosition(avg_speed, 3, 30)
    ac.setPosition(boost, 3, 120)

    return "CarInfo"


def resetAVG(*args):
    global Avg_Speed, count, trip
    Avg_Speed = 0
    count = 0
    trip = 0


def acUpdate(deltaT):
    global speed, gear, rpm, avg_speed, count, Avg_Speed, boost, scaleSpeed, scaleTurbo, trip, odomTrip, uconst
    if round(getCarStats()[0], 1) >= 1:
        Avg_Speed += round(getCarStats()[0], 1)
        count += 1

    if round(getCarStats()[0]) == 0:
        Avg_Speed = 0
        count = 0
        ac.setText(avg_speed, "AVG KMH: Waiting...")

    avgSpeedTest(count, Avg_Speed, avg_speed, scaleSpeed)
    carStatsOutput(boost, gear, rpm, speed, info.static.maxRpm, scaleTurbo, scaleSpeed)
    trip, uconst = odometerUpdate(odomTrip, getCarStats()[4], scaleSpeed, trip, deltaT, uconst)
