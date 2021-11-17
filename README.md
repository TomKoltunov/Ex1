# Ex1 - The python project 

Given the following data: the number of readings of the elevator, the number of floors on which the reading was performed,
The target floors and the source and speed of each elevator was built algorithm according to the same data.
The placement is done as follows:
Given a call that contains a source, destination and time we will check for each elevator in the building the following data:
1. Does the elevator go up, down or not in reading.
2. Is the source of the call above / below the current position of the elevator.
3. What is the current location of the elevator.
4. How long will it take for the elevator to make the call.
Elevator number i is checked if and only if the source floor of the reading is above / below the current position of the elevator and also the status of the elevator is updated accordingly (1 for upward movement, 1 for downward movement).
The status of the elevator is determined by the floor number to which the elevator is placed: if the floor is above the current location of the elevator, the status will be 1, if below the current location of the elevator the status will be -1, otherwise the status will be 0.
The current location of the elevator is calculated relative to the source floor of the reading, the calculation is done as follows: src-dt 
​​* ElevatorSpeed ​​where src is the source floor, dt is the length of time elapsed from the previous reading and ElevatorSpeed ​​is the elevator speed.
The calculation of the time to perform the reading of the elevator is calculated as follows:
Total time = Door closing time + Door opening time + start time + Stop time + Time it will take for the elevator to get from the current location to the source + Time it will take the elevator to get from the source to the destination.
