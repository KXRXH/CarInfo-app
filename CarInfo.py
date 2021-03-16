import configparser
import os
import platform
import sys

import ac

from Data.CarPerfomanceTest import avgSpeedTest
from Data.CarStats import carStatsOutput, getCarStats

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
ac.log(os.getcwd())
scaleSpeed = 1 if config["Scales"]["Speed"][0] == "0" else 0.609
scaleTurbo = 1 if config["Scales"]["TurboPressure"][0] == "0" else 14.504
count = 0
Avg_Speed = 0
speed = None
gear = None
rpm = None
avg_speed = None
boost = None
resetBtn = None


def acMain(ac_version):
    global speed, gear, rpm, avg_speed, boost, resetBtn
    MainWindow = ac.newApp("CarInfo")
    PerfomanceWindow = ac.newApp("Perfomance")
    ac.setBackgroundOpacity(MainWindow, 0.3)
    ac.setSize(MainWindow, 150, 150)
    ac.setSize(PerfomanceWindow, 150, 150)
    speed = ac.addLabel(MainWindow, "KMH: None ")
    avg_speed = ac.addLabel(PerfomanceWindow, "AVG KMH: None")
    gear = ac.addLabel(MainWindow, "Gear: None")
    rpm = ac.addLabel(MainWindow, "RPM: None")
    boost = ac.addLabel(MainWindow, "Boost: None")
    resetBtn = ac.addButton(PerfomanceWindow, "Reset")
    ac.setSize(resetBtn, 30, 20)
    ac.addOnClickedListener(resetBtn, resetAVG)

    ac.setIconPosition(MainWindow, 0, -10000)
    ac.setIconPosition(PerfomanceWindow, 0, -10000)

    ac.setPosition(speed, 3, 30)
    ac.setPosition(rpm, 3, 60)
    ac.setPosition(gear, 3, 90)
    ac.setPosition(avg_speed, 3, 30)
    ac.setPosition(boost, 3, 120)

    return "CarInfo"


def resetAVG(*args):
    global Avg_Speed, count
    Avg_Speed = 0
    count = 0


def acUpdate(deltaT):
    global speed, gear, rpm, avg_speed, count, Avg_Speed, boost, scaleSpeed, scaleTurbo
    if round(getCarStats()[0], 1) >= 1:
        Avg_Speed += round(getCarStats()[0], 1)
        count += 1

    if round(getCarStats()[0]) == 0:
        Avg_Speed = 0
        count = 0
        ac.setText(avg_speed, "AVG KMH: Waiting...")

    avgSpeedTest(count, Avg_Speed, avg_speed, scaleSpeed)
    carStatsOutput(boost, gear, rpm, speed, info.static.maxRpm, scaleTurbo, scaleSpeed)
