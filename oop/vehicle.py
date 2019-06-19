class Vehicle:

    def __init__(self, starting_top_speed=100): # In here was can define an instance attribute Automatically passes the self argument
        self.top_speed = starting_top_speed
        self.__warnings = [] #private attribute
        
    def __repr__(self):
        print('Printing...')
        return 'Top speed: {}, Warnings: {}.'.format(self.top_speed, len(self.__warnings))

    def add_warning(self, warning_text): # Self is always passed for class methods
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)

    def get_warnings(self):
        return self.__warnings

    def drive(self): # The self keyword gives access to all the methods and attributes in the class
        print('I am driving but certainly not faster than {}'.format(self.top_speed)) #self. gives access to functions and attributes in a class
        print('Warnings: {}'.format(self.__warnings))
