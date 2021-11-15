import json
import csv
import math
import sys


class Elevator:
    def __init__(self, id: int, speed: float, minFloor: int, maxFloor: int, closeTime: float, openTime: float,
                 startTime: float, stopTime: float) -> None:
        self.id = id
        self.speed = speed
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.closeTime = closeTime
        self.openTime = openTime
        self.startTime = startTime
        self.stopTime = stopTime
        self.status = 0
        self.curr = 0
        self.q = []

    def __repr__(self):
        return f"id: {self.id}, speed:{self.speed}, minFloor:{self.minFloor}, maxFloor:{self.maxFloor}, closeTime:{self.closeTime}, openTime:{self.openTime}, startTime:{self.startTime}, stopTime:{self.stopTime}"


class Building:
    def __init__(self, minFloor: int = 0, maxFloor: int = 0):
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.Elevators = []

    def from_json(self, filename):

        try:
            with open(filename, "r+") as f:
                elev = []
                my_d = json.load(f)
                self.maxFloor = my_d["_maxFloor"]
                self.minFloor = my_d["_minFloor"]
                e = my_d["_elevators"]
                for v in e:
                    elevator = Elevator(id=v["_id"], speed=v["_speed"], minFloor=v["_minFloor"],
                                        maxFloor=v["_maxFloor"], closeTime=v["_closeTime"], openTime=v["_openTime"],
                                        startTime=v["_startTime"], stopTime=v["_stopTime"])
                    elev.append(elevator)
                self.Elevators = elev
        except IOError as e:
            print(e)

    def __repr__(self):
        return f"minFloor: {self.minFloor},maxFloor: {self.maxFloor}, Elevators: {self.Elevators}"


class Call:
    def __init__(self, time, src, dst, elev) -> None:
        self.time = time
        self.src = src
        self.dst = dst
        self.elev = elev

    def __str__(self) -> str:
        return f"Time:{self.time} Src:{self.src} Dst:{self.dst} Elev:{self.elev}"

    def __repr__(self) -> str:
        return self.__str__()


class Calls:
    def __init__(self) -> None:
        self.calls = []

    def from_csv(self, filename) -> None:
        with open(filename) as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                c = Call(time=row[1], src=row[2], dst=row[3], elev=row[5])
                self.calls.append(c)


def calcTime(elev, dt, call):
    curr = elev.curr
    src = call.src
    dst = call.dst
    sum = 0
    sum += (math.abs(src - curr) / elev.speed) + elev.closeTime + elev.startTime + elev.stopTime + elev.openTime
    sum += (math.abs(src - dst) / elev.speed) + elev.closeTime + elev.startTime + elev.stopTime + elev.openTime
    return sum


if __name__ == '__main__':
    building = input()
    calls = input()

    b = Building()
    b.from_json(building)
    call = Calls()
    call.from_csv(calls)
    elevs = b.Elevators
    allocated = 0
    dt = 0
    t = 0
    best_time = sys.float_info.max
    for i in call:
        dt=t-call[i].time
        if i==0:
            dt=0
        for j in elevs:
            if elevs[j].status == 1:
                if elevs[j].curr < call[i].src:
                    if calcTime(elevs[j], dt, call[i]) < best_time:
                        best_time = calcTime(elevs[j], dt, call[i])
                        allocated = j
                        elevs[j].status = 1
            elif elevs[j].status == -1:
                if elevs[j].curr > call[i].src:
                    if calcTime(elevs[j], dt, call[i]) < best_time:
                        best_time = calcTime(elevs[j], dt, call[i])
                        allocated = j
                        elevs[j].status = -1
            elif elevs[j].status == 0:
                if calcTime(elevs[j], dt, call[i]) < best_time:
                    best_time = calcTime(elevs[j], dt, call[i])
                    allocated = j
                    if call[i].src < elevs[j].curr:
                        elevs[j].status = -1
                    else:
                        elevs[j].status = 1
            t=call[i].time


# with open("Calls_a.csv") as file:
#     csvreader = csv.reader(file)
#     for row in csvreader:
#         c = Call(time=row[1], src=row[2], dst=row[3], elev=row[5])
#         Kriot.append(c)
# print(Kriot)
