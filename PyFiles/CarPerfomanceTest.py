import ac


def avgSpeedTest(count, speed, avg_window, scaleSpeed):
    try:
        if scaleSpeed == 1:
            ac.setText(avg_window, "AVG KM/H: {}".format(round(speed / count, 1)))
        else:
            ac.setText(avg_window, "AVG MP/H: {}".format(round(speed / count, 1)))
    except ZeroDivisionError:
        pass
