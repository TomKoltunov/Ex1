class Elevator:

    def __init__(self, id : int, speed : float, minFloor : int, maxFloor : int, closeTime : float, openTime : float,
                       startTime : float, stopTime : float) -> None:
        self.id = id
        self.speed = speed
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.closeTime = closeTime
        self.openTime = openTime
        self.startTime = startTime
        self.stopTime = stopTime

    def __dict__(self) -> dict:
        return {"_id" : self.id, "_speed" : self.speed, "_minFloor" : self.minFloor,"_maxFloor" : self.maxFloor,
                "_closeTime" : self.closeTime, "_openTime" : self.openTime, "_startTime" : self.startTime,
                "_stopTime" : self.stopTime}
        
    def __str__(self) -> str:
        return f"_id:{self.id}, _speed:{self.speed}, _minFloor:{self.minFloor},_maxFloor:{self.maxFloor}, " \
               f"_closeTime:{self.closeTime}, _openTime:{self.openTime},_startTime:{self.startTime}, " \
               f"_stopTime:{self.stopTime}"

    def __repr__(self) -> str:
        return f"_id:{self.id}, _speed:{self.speed}, _minFloor:{self.minFloor},_maxFloor:{self.maxFloor}, " \
               f"_closeTime:{self.closeTime}, _openTime:{self.openTime},_startTime:{self.startTime}, " \
               f"_stopTime:{self.stopTime}"