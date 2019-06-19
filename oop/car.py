from vehicle import Vehicle
class Car(Vehicle): # The class we want to inherit from

    # top_speed = 100 # Class instance
    # warnings = []
    def brag(self):
        print('Look how cool my car is! ')

car_1 = Car() # Calls the constructor which constructs the instance of the object
car_1.drive() # == car.drive(car_1)

car_1.add_warning('New Warning')
#car_1.__warnings.append([])
print(car_1)
print(car_1.get_warnings())

car_2 = Car(200)  
print(car_2)  
car_2.drive()

car_3 = Car(300)
car_3.drive()

"""
The reason that even though we wanted to only change the instance of car 1 it changed all of the instances of cars because we have
a class instance which is attached to the class Car, which changes all instances (objects) of the car class. 
"""