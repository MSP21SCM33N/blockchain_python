class Car:
    # top_speed = 100 # Class instance
    # warnings = []

    def __init__(self, starting_top_speed=100): # In here was can define an instance attribute Automatically passes the self argument
        self.top_speed = starting_top_speed
        self.warnings = []

    def __repr__(self):
        print('Printing...')
        return 'Top speed: {}, Warnings: {}.'.format(self.top_speed, self.warnings)

    def drive(self): # The self keyword gives access to all the methods and attributes in the class
        print('I am driving but certainly not faster than {}'.format(self.top_speed)) #self. gives access to functions and attributes in a class
        print('Warnings: {}'.format(self.warnings))

car_1 = Car() # Calls the constructor which constructs the instance of the object
car_1.drive()

car_1.warnings.append('Cool')
car_2 = Car(200)  
print(car_2)  
car_2.drive()

car_3 = Car(300)
car_3.drive()

"""
The reason that even though we wanted to only change the instance of car 1 it changed all of the instances of cars because we have
a class instance which is attached to the class Car, which changes all instances (objects) of the car class. 
"""