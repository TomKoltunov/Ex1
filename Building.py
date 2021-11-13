import json
import Elevator

class Building:
    def __init__(self, minFloor : int, maxFloor : int, elevators : list) -> None:
        self.min_floor = minFloor
        self.max_floor = maxFloor
        self.elevators =[]

    def __repr__(self) -> str:
        return f"_minFloor:{self.min_floor},\n_maxFloor:{self.max_floor},\n"

    def from_json(self, file_name : str) -> None:
        try:
            with open(file_name, "r") as f:
                building_dict = json.load(fp = f)
                self.min_floor = building_dict["_minFloor"]
                self.max_floor = building_dict["_maxFloor"]
                self.elevators = building_dict["_elevators"]
                for i in f
                    self.elevators[i]=Elevator()

        except IOError as e:
            print(e)