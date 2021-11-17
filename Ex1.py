import json
import csv
import math
import sys


class Elevator:
    """
    This class represents an elevator in some Building.
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
        :param stopTime: The time which takes to this Elevator to stop moving when it reach its current
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
        """
        This method works on just one Elevator.
        :return: Given Elevator's str.
        """
        return f"id: {self.id}, speed:{self.speed}, minFloor:{self.minFloor}, maxFloor:{self.maxFloor}, " \
               f"closeTime:{self.closeTime}, openTime:{self.openTime}, startTime:{self.startTime}, " \
               f"stopTime:{self.stopTime}"

    def __repr__(self) -> str:
        """
        This method works on one or more (list of) Elevator. This method uses '__str()__' method which appears above it.
        :return: Given Elevators'es strs.
        """
        self.__str__()


class Building:
    """
    This class represents a building.
    """

    def __init__(self, minFloor: int = 0, maxFloor: int = 0) -> None:
        """
        This is a constructor which creates "Building" object.
        :param minFloor: The lowest floor of the given building.
        :param maxFloor: The highest floor of the given building.
        :param Elevators: The constructor creates list of its elevators. Each elevator is a type of 'Elevator'.
        """
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.Elevators = []

    def from_json(self, filename) -> None:
        """
        This method achieves str which represents some Building's json file. The method turns the json object into a
        dict. It eventually loads the json's data. Raises 'IOError' if the 'filename' json does not exist ib the IDE.
        :param filename: That is a str which holds a name of some Building's json.
        :return: Nothing.
        """
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
        """
        This method works on just one Building.
        :return: Given Building's str.
        """
        return f"minFloor: {self.minFloor},maxFloor: {self.maxFloor}, Elevators: {self.Elevators}"

    def __repr__(self) -> str:
        """
        This method works on one or more (list of) Building. This method uses '__str()__' method which appears above it.
        :return: Given Buildings'es strs.
        """
        return self.__str__()


class Call:
    """
    This class represents a call to some Elevator in some Building.
    """

    def __init__(self, time, src, dst) -> None:
        """
        This is a constructor which creates "Call" object.
        :param time: The exact second from the start of the 'run simulator' in which the Call was "created".
        :param src: The floor from which the Call was "called" (basically 'source floor' of the  given Call)
        :param dst: The floor to which the floor was "sent" (basically "destination floor" of the given Call)
        """
        self.elevator = 'Elevator Call'
        self.time = time
        self.src = src
        self.dst = dst
        self.stat = 3  # The status of the Elevator (not in use)
        self.elev = 0  # First location of each Elevator.

    def __str__(self) -> str:
        """
        This method works on just one Call.
        :return: Given Call's str.
        :return:
        """
        return f"Time:{self.time} Src:{self.src} Dst:{self.dst} Elev:{self.elev}"

    def __repr__(self) -> str:
        """
        This method works on one or more (list of) Call. This method uses '__str()__' method which appears above it.
        :return: Given Calls'es strs.
        """
        return self.__str__()


class Calls:
    """
    This class represents list of calls to some Elevators in some Building.
    """

    def __init__(self) -> None:
        """
        This is a constructor which creates "Calls" object.
        :param calls: The constructor creates list of its calls.
        """
        self.calls = []

    def from_csv(self, filename) -> None:
        """
        This method achieves str which represents some Calls'es csv file. It eventually loads the csv's data.
        :param filename: That is a str which holds a name of some Calls'es csv.
        :return: Nothing.
        """
        with open(filename) as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                c = Call(time=float(row[1]), src=int(row[2]), dst=int(row[3]))
                self.calls.append(c)


def calcTime(elev, call):
    """
    :param elev: The current Elevator.
    :param call: The current Call
    :return: The time which takes to 'elev' to complete its 'call'.
    """
    curr = elev.curr
    src = call.src
    dst = call.dst
    sum = 0
    sum += (abs(src - curr) / elev.speed) + elev.closeTime + elev.startTime + elev.stopTime + elev.openTime
    sum += (abs(src - dst) / elev.speed) + elev.closeTime + elev.startTime + elev.stopTime + elev.openTime
    return sum


if __name__ == '__main__':

    # The main algorithm

    building = input()
    calls = input()
    output = input()
    b = Building()  # The given building.
    b.from_json(building)  # Loading the building from json file.
    r = Calls()  # Empty objects of calls.
    r.from_csv(calls)  # Load the calls to the object.
    call = r.calls  # List that contains the calls.
    elevs = b.Elevators  # List that contains the elevators.
    allocated = 0  # Allocation index.
    dt = 0
    t = 0  # Previous t (for dt calculation).
    a = 0  # Elevators counter.
    alloc = 0  # Allocated elevator.
    p = 0  # Helper for i=0 case.
    best_time = sys.float_info.max  # Fastest time to complete a call.
    for i in call:
        dt = abs(i.time - t)
        """
            Calculating the current position of the allocated elevator by cases:
            If the elevator is going up, its current position is the previous position + dt*v.
            Else, if the elevator is going down, its current position is the previous position - dt*v.
            Otherwise, the elevator doesn't has any calls and it isn't moving.
            
        """
        if i != 0:
            if elevs[alloc].status == 1:
                elevs[alloc].curr = (elevs[alloc].speed * dt) + elevs[alloc].prev
                elevs[alloc].prev = elevs[alloc].curr
            elif elevs[alloc].status == -1:
                elevs[alloc].curr = elevs[alloc].prev - (elevs[alloc].speed * dt)
                elevs[alloc].prev = elevs[alloc].curr
        if p == 0:  # Temporary for the case of the first call, doesn't calculate the dt.
            dt = 0
            p += 1
        if i.src >= b.minFloor and i.src <= b.maxFloor and i.dst >= b.minFloor and i.dst <= b.maxFloor:
            """
                Allocation of elevators by 3 cases:
                Case 1: the elevator is going up and the src is grater than the current position of the elevator.
                Case 2: the elevator is going down and the src is less than the current position of the elevator.
                Case 3: the elevator isn't allocated.
                In every case, if the time that takes to the current elevator is less than the other's time,
                change the best time to the current time and change the allocated elevator to the current elevator.
            """
            for j in elevs:
                if j.status == 1:
                    if j.curr < i.src:
                        if calcTime(j, i) < best_time:
                            best_time = calcTime(j, i)
                            allocated = j
                            j.status = 1
                            alloc = a
                elif j.status == -1:
                    if j.curr > i.src:
                        if calcTime(j, i) < best_time:
                            best_time = calcTime(j, i)
                            allocated = j
                            j.status = -1
                            alloc = a
                elif j.status == 0:
                    if calcTime(j, i) < best_time:
                        best_time = calcTime(j, i)
                        allocated = j
                        alloc = a
                        if i.src < j.curr:
                            j.status = -1
                        else:
                            j.status = 1
                """
                    Updating the status of the elevator.
                """
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
    """
        Copying the calls (with the allocations of the elevators) to the output file.
    """
    new_calls = []
    for i in call:
        new_calls.append(i.__dict__.values())
    with open(output, 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(new_calls)
