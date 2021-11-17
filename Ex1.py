import json
import csv
import math
import sys


class Elevator:
    """
    This class represents an elevator in some building.
    """

    def __init__(self, id: int, speed: float, minFloor: int, maxFloor: int, closeTime: float, openTime: float,
                 startTime: float, stopTime: float) -> None:
        """
        This is a constructor which creates "Elevator" object.
        :param id: The id (serial number) of the Elevator, of an 'int' type.
        :param speed: The speed of the Elevator while its moving between the call's source floor, of a 'float'
                      type. This attribute is constant (the speed of the elevator does not change)
        :param minFloor: The lowest floor the Elevator can reach (it's also the lowest floor of this Elevator's
                         building), of an 'int' type.
        :param maxFloor: The highest floor the Elevator can reach (it's also the highest floor of this Elevator's
                         building), of an 'int' type.
        :param closeTime: The time which takes to this Elevator to close its doors, of a 'float' type.
        :param openTime: The time which takes to this Elevator to open its door, if a 'float' type.
        :param startTime: The time which takes to this Elevator to start moving to its current call's source floor.
        :param stopTime: The time which takes to this Elevator to stop moving when it reach to its current
                         source floor.
        """
        self.id = id
        self.speed = speed
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.closeTime = closeTime
        self.openTime = openTime
        self.startTime = startTime
        self.stopTime = stopTime
        self.status = 0  # When the program creates an 'Elevator' object, in that exact moment the status of the
        # Elevator is 0 (means it does not move - "rest mode"). If the Elevator is moving
        # upstairs - its status is 1. And when the Elevator is moving downstairs - its status if -1.
        self.curr = 0  # This attribute gives us the current floor of the Elevator at each moment.
        self.prev = 0  # This attribute gives us the previous floor of the Elevator at each moment.

    def __str__(self) -> str:
        return f"id: {self.id}, speed:{self.speed}, minFloor:{self.minFloor}, maxFloor:{self.maxFloor}, " \
               f"closeTime:{self.closeTime}, openTime:{self.openTime}, startTime:{self.startTime}, " \
               f"stopTime:{self.stopTime}"

    def __repr__(self) -> str:
        self.__str__()


class Building:
    def __init__(self, minFloor: int = 0, maxFloor: int = 0) -> None:
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.Elevators = []

    def from_json(self, filename) -> None:
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

    def __str__(self) -> str:
        return f"minFloor: {self.minFloor},maxFloor: {self.maxFloor}, Elevators: {self.Elevators}"

    def __repr__(self) -> str:
        return self.__str__()


class Call:
    def __init__(self, time, src, dst) -> None:
        """

        :param time:
        :param src:
        :param dst:
        """
        self.elevator = 'Elevator Call'
        self.time = time
        self.src = src
        self.dst = dst
        self.stat = 3
        self.elev = 0

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
                c = Call(time=float(row[1]), src=int(row[2]), dst=int(row[3]))  # , elev=int(row[5]))
                self.calls.append(c)


def calcTime(elev, dt, call):
    curr = elev.curr
    src = call.src
    dst = call.dst
    sum = 0
    sum += (abs(src - curr) / elev.speed) + elev.closeTime + elev.startTime + elev.stopTime + elev.openTime
    sum += (abs(src - dst) / elev.speed) + elev.closeTime + elev.startTime + elev.stopTime + elev.openTime
    return sum


if __name__ == '__main__':
    building = input()
    calls = input()
    output = input()
    b = Building()
    b.from_json(building)
    r = Calls()
    r.from_csv(calls)
    call = r.calls
    elevs = b.Elevators
    allocated = 0
    dt = 0
    t = 0
    a = 0
    alloc = 0
    p = 0
    best_time = sys.float_info.max
    for i in call:
        dt = abs(i.time - t)
        if i != 0:
            if elevs[alloc].status == 1:
                elevs[alloc].curr = (elevs[alloc].speed * dt) + elevs[alloc].prev
                elevs[alloc].prev = elevs[alloc].curr
            elif elevs[alloc].status == -1:
                elevs[alloc].curr = elevs[alloc].prev - (elevs[alloc].speed * dt)
                elevs[alloc].prev = elevs[alloc].curr
        if p == 0:
            dt = 0
            p += 1
        if i.src >= b.minFloor and i.src <= b.maxFloor and i.dst >= b.minFloor and i.dst <= b.maxFloor:
            for j in elevs:
                if j.status == 1:
                    if j.curr < i.src:
                        if calcTime(j, dt, i) < best_time:
                            best_time = calcTime(j, dt, i)
                            allocated = j
                            j.status = 1
                            alloc = a
                elif j.status == -1:
                    if j.curr > i.src:
                        if calcTime(j, dt, i) < best_time:
                            best_time = calcTime(j, dt, i)
                            allocated = j
                            j.status = -1
                            alloc = a
                elif j.status == 0:
                    if calcTime(j, dt, i) < best_time:
                        best_time = calcTime(j, dt, i)
                        allocated = j
                        alloc = a
                        if i.src < j.curr:
                            j.status = -1
                        else:
                            j.status = 1
                if j.status == 1 and j.curr > i.src:
                    if i.dst < i.src:
                        j.status = -1
                    elif j.curr > i.dst:
                        j.status = 0
                elif j.status == -1 and j.curr < i.src:
                    if i.dst > i.src:
                        j.status = 1
                    elif j.curr < i.dst:
                        j.status = 0
                a += 1

            a = 0
            t = i.time
            i.elev = alloc
            best_time = sys.float_info.max

    new_calls = []
    for i in call:
        new_calls.append(i.__dict__.values())
    with open(output, 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(new_calls)
