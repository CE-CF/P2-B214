import os
import subprocess  # For executing a shell command


class DroneChecker:
    def __init__(self, host):
        self.host = host
        self.host_ip = self.host.split(".")
        self.ip_range = 252

    def ping(self, prange):
        alive = []
        rangeFrom = prange[0]
        rangeTo = prange[1]
        print(
            "Pinging all hosts on {0}.{1}-{2}".format(
                self.host, rangeFrom, rangeTo
            )
        )

        with open(os.devnull, "wb") as limbo:
            for n in range(rangeFrom, rangeTo):
                ip = "{0}.{1}".format(self.host, n)
                result = subprocess.Popen(
                    ["ping", "-n", "1", "-w", "100", ip],
                    stdout=limbo,
                    stderr=limbo,
                ).wait()
                if result:
                    print(ip + " inactive")
                else:
                    print(ip + " active")
                    alive.append(ip)

        return alive

    def activeDronePacketAdd(self, ActiveDrones, state=None, lat =None, long = None):
        droneName = "RelayBoxDrone"
        outputList = []
        outputString = ""

        for x in range(len(ActiveDrones)):
            outputList.append(
                "{0}{1}:{2}".format(droneName, (x + 1), ActiveDrones[x])
            )

        CMDSTATE = "CMD:ADD_DRONE;STATE:{0};LAT:{1};LONG:{2};".format(state, lat, long)
        outputString = CMDSTATE + (";".join(outputList)) + ";"

        return outputString

    def activeDronePacketUpdate(self, ActiveDrones, state=None, lat =None, long = None):
        droneName = "RelayBoxDrone"
        outputList = []
        outputString = ""

        for x in range(len(ActiveDrones)):
            outputList.append(
                "{0}{1}:{2}".format(droneName, (x + 1), ActiveDrones[x])
            )

        CMDSTATE = "CMD:UPDATE_DRONE;STATE:{0};LAT:{1};LONG:{2};".format(state, lat, long)
        outputString = CMDSTATE + (";".join(outputList)) + ";"

        return outputString
