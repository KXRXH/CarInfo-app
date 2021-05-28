import configparser
import os
import platform
import sys
import ac

from PyFiles.CarPerfomanceTest import avgSpeedTest
from PyFiles.CarStats import *
from PyFiles.Odometer import odometerUpdate

if platform.architecture()[0] == "64bit":
    libDir = "stdlib/lib64"
else:
    libDir = "stdlib/lib"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), libDir))
os.environ['PATH'] = os.environ['PATH'] + ";."
from stdlib.sim_info import info

config = configparser.ConfigParser()
config.read(os.path.realpath(os.getcwd() + '/apps/python/CarInfo/config.ini'))
carConfig = configparser.ConfigParser()
PATHtoOdomInfo = os.path.realpath(os.getcwd() + '/apps/python/CarInfo/CarData/carsInfo.ini')
carConfig.read(PATHtoOdomInfo)
try:
    uconst = float(carConfig["CarsConst"][ac.getCarName(0)])
except KeyError or ValueError:
    uconst = 1
try:
    mileage = carConfig["CarsOdom"][ac.getCarName(0)]
except KeyError or ValueError:
    mileage = 0

count = Avg_Speed = sumTrip = altrip1 = trip = 0
speed = gear = rpm = avg_speed = boost = None
PerformanceFlag = False
CSM = CarStatsMain()
MainWindow = OdomWindow = resetBtn = odomTrip = MileageLabel = None
altrip = float(mileage)
scaleSpeed = 1 if config["Scales"]["Speed"][0] == "0" else 0.609
scaleTurbo = 1 if config["Scales"]["TurboPressure"][0] == "0" else 14.504


def acMain(ac_version):
    global speed, gear, rpm, avg_speed, boost, resetBtn, odomTrip, MileageLabel, MainWindow, OdomWindow
    ac.log("Loading...")
    MainWindow = ac.newApp("CarInfo")
    OdomWindow = ac.newApp("Odometer")
    PerformanceWindow = ac.newApp("Performance")

    ac.setBackgroundOpacity(MainWindow, 0)  # 0.3
    ac.setBackgroundOpacity(PerformanceWindow, 0.3)
    ac.setBackgroundOpacity(OdomWindow, 0)
    ac.drawBorder(MainWindow, 0)
    ac.drawBorder(OdomWindow, 0)
    ac.setSize(MainWindow, 250, 200)
    ac.setSize(OdomWindow, 280, 35)
    ac.setSize(PerformanceWindow, 150, 150)

    speed = ac.addLabel(MainWindow, "KMH: None ")
    avg_speed = ac.addLabel(PerformanceWindow, "AVG KMH: None")
    gear = ac.addLabel(MainWindow, "Gear: None")
    rpm = ac.addLabel(MainWindow, "RPM: None")
    boost = ac.addLabel(MainWindow, "Boost: None")
    MileageLabel = ac.addLabel(OdomWindow, "Mileage: None")
    resetBtn = ac.addButton(PerformanceWindow, "Reset")
    odomTrip = ac.addLabel(OdomWindow, "Trip: None")

    ac.setSize(resetBtn, 30, 20)
    ac.addOnClickedListener(resetBtn, resetAVG)

    ac.setIconPosition(MainWindow, 0, -10000)
    ac.setIconPosition(PerformanceWindow, 0, -10000)
    ac.setIconPosition(OdomWindow, 0, -10000)
    ac.setTitlePosition(OdomWindow, 0, -10000)

    ac.setPosition(speed, 3, 30)
    ac.setPosition(rpm, 3, 60)
    ac.setPosition(gear, 3, 90)
    ac.setPosition(avg_speed, 3, 30)
    ac.setPosition(odomTrip, 3, 10)
    ac.setPosition(MileageLabel, 250, 10)
    ac.setPosition(boost, 3, 120)

    ac.setCustomFont(speed, "Play", 0, 0)
    ac.setCustomFont(gear, "Play", 0, 0)
    ac.setCustomFont(boost, "Play", 0, 0)
    ac.setCustomFont(rpm, "Play", 0, 0)
    ac.setCustomFont(MileageLabel, "Play", 0, 0)
    ac.setCustomFont(odomTrip, "Play", 0, 0)
    ac.setFontSize(speed, 24)
    ac.setFontSize(gear, 24)
    ac.setFontSize(rpm, 24)
    ac.setFontSize(boost, 24)
    ac.setFontSize(MileageLabel, 22)
    ac.setFontSize(odomTrip, 22)
    ac.setTitle(MainWindow, "")
    ac.setTitle(OdomWindow, "")
    ac.log("Loaded!")

    return "CarInfo"


def resetAVG(*args):
    global Avg_Speed, count
    Avg_Speed = 0
    count = 0


def acUpdate(deltaT):
    global speed, gear, rpm, avg_speed, count, Avg_Speed, boost, scaleSpeed, scaleTurbo, trip, odomTrip, uconst
    global CSM, PerformanceFlag, MileageLabel, mileage, altrip, altrip1, sumTrip, MainWindow, OdomWindow
    CSM.updateStats()
    ac.setBackgroundOpacity(MainWindow, 0)
    ac.setBackgroundOpacity(OdomWindow, 0)
    if round(CSM.curr_Speed, 1) >= 1:
        Avg_Speed += round(CSM.curr_Speed, 1)
        count += 1
    if round(CSM.curr_Speed) == 0:
        Avg_Speed = 0
        count = 0
        ac.setText(avg_speed, "AVG KMH: Waiting...")
        PerformanceFlag = True
    sumTrip = altrip + altrip1
    avgSpeedTest(count, Avg_Speed, avg_speed, scaleSpeed)
    carStatsOutput(boost, gear, rpm, speed, info.static.maxRpm, scaleTurbo, scaleSpeed)
    trip, uconst, altrip1 = odometerUpdate(odomTrip, CSM.curr_dts, scaleSpeed, trip, deltaT, uconst)
    ac.setText(MileageLabel, "Mileage: {} KMs".format(round(sumTrip, 1)))


def acShutdown(*args):
    global carConfig, PATHtoOdomInfo, altrip1, altrip, sumTrip, uconst
    carConfig["CarsOdom"][ac.getCarName(0)] = str(sumTrip)
    carConfig["CarsConst"][ac.getCarName(0)] = str(uconst)
    carConfig.write(open(PATHtoOdomInfo, 'w'))
