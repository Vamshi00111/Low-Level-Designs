
'''
Question To Ask:
Floors ?
Vehicle Types and Sizes?
Payment System?

Assumptions:
- Multiple Floors
- Car - 1 Spot, Limos - 2 Consecutive Spots and Semi Trucks - 3 Consecutive Spots
- Payment System where a driver can make a booking for a spot, 
    But will be charged after he leaves based on no. of hours
    Driver's amount due will be updated
- Driver will be assigned a next available spot in the lowest floor, where all the spots are in a row

LLD:
Vehicle Class - And multiple type of vehicles inherit from this class - Limo, Car, Semi-Truck
        - Size : no.of spots it occupies

Driver Class - 
        - charge(): Will charge the driver, based on the time he leaves - will increment his amount_due for now
        in drivers's member variable for amount_due


ParkingFloor - 
        - spots: List of spots
        - park_vehicle(): Will park the vehicle in the next available spot
        - free_spot(): Will free the spot, and call charge() method of the driver
        - get_next_available_spot(): Will return the next available spot
        - add_spot(): Will add a spot to the floor

ParkingGarage -
        - floors: List of floors
        - park_vehicle(): Will park the vehicle in the next available spot
        - free_spot(): Will free the spot, and call charge() method of the driver
        - get_next_available_spot(): Will return the next available spot
        - add_spot(): Will add a spot to the floor
        - get_next_available_spot(): Will return the next available spot

ParkingSystem -
        - park_vehicle(Driver): Will park the vehicle in the next available spot
        - free_spot(): Will free the spot, and call charge() method of the driver
        - Has parkingGarage, Hourly rate, and a timeParked HashMap

Why Seprate ParkingGarage and ParkingSystem?

Single Responsibility Principle:
    ParkingGarage: Manages the physical infrastructure.
    ParkingSystem: Handles operational logic, billing, and interactions with drivers.

Scalability: If you have multiple parking garages, a single ParkingSystem can manage all of them, 
enabling features like load balancing or centralized billing.

Maintainability: By keeping the ParkingGarage and ParkingSystem independent, changes in one
(e.g., adding more floors or spots) don't directly impact the other.

We have to make the code more modular and scalable, so that it can be easily extended in the future.
        
'''

from datetime import datetime

class Vehicle:
    def __init__(self, size):
        self._size = size # Use private variable to ensure encapsulation, validation can be added here

    @property # Can call the getter without paranthesis - @property - To make the code more cleaner
    def size(self):
        return self._size

class Car(Vehicle):
    def __init__(self):
        super().__init__(size=1)

class Limo(Vehicle):
    def __init__(self):
        super().__init__(size=2)

class SemiTruck(Vehicle):
    def __init__(self):
        super().__init__(size=3)

class Driver: # Driver with a single vehicle for now
    def __init__(self, id, vehicle):
        self._id = id
        self._vehicle = vehicle
        self._amount_due = 0

    @property
    def id(self):
        return self._id
    
    @property
    def vehicle(self):
        return self._vehicle

    @property
    def amount_due(self):
        return self._amount_due

    def charge(self, amount):
        self._amount_due += amount

class ParkingFloor:
    def __init__(self, spot_count= 10):
        self._spots = [0]*spot_count
        self._vehicle_map = {} # vehicle_id -> [l, r] - left and right spots occupied by the vehicle

    def park_vehicle(self, vehicle):
        size = vehicle.size
        l, r = 0, 0
        while r < len(self._spots):
            # Reset the left pointer if the spot is occupied
            if self._spots[r] != 0:
                l = r + 1
            elif r-l+1 == size:
                for i in range(l, r+1):
                    self._spots[i] = 1
                self._vehicle_map[vehicle] = [l, r]
                return True

            r += 1
        
        return False

    def remove_vehicle(self, vehicle):
        l, r = self._vehicle_map[vehicle]
        for i in range(l, r+1):
            self._spots[i] = 0
        del self._vehicle_map[vehicle]

    @property
    def get_parking_spots(self):
        return self._spots
    
    def get_vehicle_spot(self, vehicle):
        return self._vehicle_map[vehicle]

# Comprises Multiple Parking Floors, Acts as a wrapper around Parking Floor
# Physical Structure of the Parking Lot - without associating with the driver and billing
class ParkingGarage:
    def __init__(self, floor_count, spots_per_floor):
        self._floors = [ParkingFloor(spots_per_floor) for _ in range(floor_count)] # Use Parking Floor Clas in this

    # Wrapper functions around parking floor functions
    def park_vehicle(self, vehicle):
        for floor in self._floors:
            if floor.park_vehicle(vehicle):
                return True
        return False

    def remove_vehicle(self, vehicle):
        for floor in self._floors:
            if vehicle in floor._vehicle_map:
                floor.remove_vehicle(vehicle)
                return True
        return False
        
# Parking System - Will have a parking garage, hourly rate, and a time parked map
# Manages the entire parking garage and the payment system
class ParkingSystem:
    def __init__(self, parkingGarage, hourly_rate):
        self._parking_garage = parkingGarage
        self._hourly_rate = hourly_rate
        self._time_parked_map = {} # Map driver_id -> time_parked

    @property
    def parking_garage(self):
        return self._parking_garage

    @property
    def hourly_rate(self):
        return self._hourly_rate

    @property
    def time_parked_map(self):
        return self._time_parked_map

    def park_vehicle(self, driver):
        if self.parking_garage.park_vehicle(driver.vehicle):
            self.time_parked_map[driver.id] = datetime.now().hour # Gives int 0-23 based on the current hour
            return True
        return False
    
    # Assumption: Driver will not stay for more than 24 hours, or use can also pass the datetime object
    def remove_vehicle(self, driver):
        if driver.id in self.time_parked_map:
            time_parked = self.time_parked_map[driver.id]
            hours_parked = datetime.now().hour - time_parked
            driver.charge(hours_parked*self.hourly_rate)
            self.parking_garage.remove_vehicle(driver.vehicle)
            del self.time_parked_map[driver.id]
            return True
        return False
        

# Example Usage
if __name__ == "__main__":
    parkingGarage = ParkingGarage(3, 2)
    parkingSystem = ParkingSystem(parkingGarage, 5)

    driver1 = Driver(1, Car())
    driver2 = Driver(2, Limo())
    driver3 = Driver(3, SemiTruck())

    print(parkingSystem.park_vehicle(driver1)) # True
    print(parkingSystem.park_vehicle(driver2)) # True
    print(parkingSystem.park_vehicle(driver3)) # False

    print(parkingSystem.remove_vehicle(driver1)) # True
    print(parkingSystem.remove_vehicle(driver2)) # True
    print(parkingSystem.remove_vehicle(driver3)) # False
