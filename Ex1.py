import json
import csv


class Elevator:
    def __init__(self, id: int, speed: float, minFloor: int, maxFloor: int, closeTime: float, openTime: float,
                 startTime: float, stopTime: float) -> None:
        self._id = id
        self._speed = speed
        self._minFloor = minFloor
        self._maxFloor = maxFloor
        self._closeTime = closeTime
        self._openTime = openTime
        self._startTime = startTime
        self._stopTime = stopTime

    def __repr__(self):
        return f"id: {self._id}, speed:{self._speed}, minFloor:{self._minFloor}, maxFloor:{self._maxFloor}, closeTime:{self._closeTime}, openTime:{self._openTime}, startTime:{self._startTime}, stopTime:{self._stopTime}"


class Building:
    def __init__(self, minFloor: int = 0, maxFloor: int = 0):
        self._minFloor = minFloor
        self._maxFloor = maxFloor
        self._Elevators = []

    def from_json(self, filename):

        try:
            with open(filename, "r+") as f:
                elev = []
                my_d = json.load(f)
                self._maxFloor = my_d["_maxFloor"]
                self._minFloor = my_d["_minFloor"]
                e = my_d["_elevators"]
                for v in e:
                    elevator = Elevator(id=v["_id"], speed=v["_speed"], minFloor=v["_minFloor"],
                                        maxFloor=v["_maxFloor"], closeTime=v["_closeTime"], openTime=v["_openTime"],
                                        startTime=v["_startTime"], stopTime=v["_stopTime"])
                    elev.append(elevator)
                self._Elevators = elev
        except IOError as e:
            print(e)

    def __repr__(self):
        return f"minFloor: {self._minFloor},maxFloor: {self._maxFloor}, Elevators: {self._Elevators}"


class Call:
    def __init__(self, time, src, dst, elev) -> None:
        self._time = time
        self._src = src
        self._dst = dst
        self._elev = elev

    def __str__(self) -> str:
        return f"Time:{self._time} Src:{self._src} Dst:{self._dst} Elev:{self._elev}"

    def __repr__(self) -> str:
        return self.__str__()

class Calls:
    def __init__(self):
        self._calls = []

    def from_csv(self, filename):
        with open(filename) as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                c = Call(time=row[1], src=row[2], dst=row[3], elev=row[5])
                self._calls.append(c)

if __name__ == '__main__':
    #building = input()
    # calls = input()
    # output = input()
    Kriot = []
    with open("Calls_a.csv") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            c = Call(time=row[1], src=row[2], dst=row[3], elev=row[5])
            Kriot.append(c)
    print(Kriot)