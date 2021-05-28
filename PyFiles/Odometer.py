import ac
import acsys

slips = 0


def odometerUpdate(trip_label, dts, units, trip, delt, uconst):
    global slips
    trip += delt * dts / 3.6
    gs = ac.getCarState(0, acsys.CS.SpeedKMH)
    if uconst == 1.0 and gs > 50:
        slips = ac.getCarState(0, acsys.CS.SlipRatio)
        try:
            uconst = gs / dts * (1 + (slips[2] + slips[3]) / 2.0)
        except ZeroDivisionError:
            return trip, 1, 0
    current_trip = round((units * uconst * trip) / 1000, 1)
    if units == 1:
        ac.setText(trip_label, "Session trip: {} KMs".format(current_trip))
    else:
        ac.setText(trip_label, "Session trip: {} Miles".format(current_trip))
    return trip, uconst, current_trip
