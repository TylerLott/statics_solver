import numpy as np
import math

SUPPORTS = 1
NUMBER_OF_FORCES = 1
NUMBER_OF_MOMENTS = 1


class Force:
    # direction = 'down' or 'up'
    # magnitude = float
    # angle from axis = angle in degrees from pos x, counter clockwise
    # x location is in units of length
    # list_of_Forces = list
    def __init__(self, direction, magnitude, list_of_Forces_x, angle_from_axis=0, x_location=0, y_location=0):
        self.direction = direction
        self.get_direction_sign()
        self.magnitude = magnitude
        self.angle_from_axis = angle_from_axis
        self.x_location = x_location
        self.y_location = y_location
        self.list_of_Forces_x = list_of_Forces_x
        self.create_new_force_x()
        self.x_component = self.find_x_comp()
        self.y_component = self.find_y_comp()

    def get_direction_sign(self):
        if self.direction == 'down':
            self.direction = -1
        else:
            self.direction = 1

    def create_new_force_x(self):
        self.list_of_Forces_x = self.list_of_Forces_x.append(self)
        return self.list_of_Forces_x

    def find_x_comp(self):
        x_comp = -1 * self.magnitude * np.cos(math.radians(self.angle_from_axis))
        return x_comp

    def find_y_comp(self):
        y_comp = self.direction * self.magnitude * np.sin(math.radians(self.angle_from_axis))
        return y_comp



# this is only for reactionary  or applied moments
class Moment:
    def __init__(self, direction, magnitude, x_location):
        self.direction = direction
        self.magnitude = magnitude
        self.x_location = x_location


class Force_Area:
    def __init__(self, direction, magnitude_equation, x_left, x_right):
        self.direction = direction
        self.magnitude_equation = magnitude_equation
        self.x_left = x_left
        self.x_right = x_right


class Pin_Connection:
    # reaction_x and reaction_y should be objects of Force
    def __init__(self, reaction_x, reaction_y, x_point, y_point):
        self.reaction_x = reaction_x
        self.reaction_y = reaction_y
        self.x_point = x_point
        self.y_point = y_point


class Roller_Connection:
    # reaction_y should be object of Force
    def __init__(self, reaction_y, x_point, y_point):
        self.reaction_y = reaction_y
        self.x_point = x_point
        self.y_point = y_point


class Fixed_Connection:
    # reaction_x and reaction_y should be objects of Force
    # reaction_moment should be objects of Moment
    def __init__(self, reaction_x, reaction_y, reaction_moment, x_point, y_point):
        self.reaction_x = reaction_x
        self.reaction_y = reaction_y
        self.reaction_moment = reaction_moment
        self.x_point = x_point
        self.y_point = y_point

def sum_forces_x(list_of_Forces_x):
    pass

def sum_forces_y(list_of_Forces_y):
    pass

def sum_moments_at_point(x_point, y_point, list_of_Moments, list_of_Forces, list_of_Connections):
    for object in list_of_Forces:
        if object.x_component > 0 and object.y_location > 0:
            L = object.y_location - y_point
            moment = L * object.x_component
            list_of_Moments.append(moment)
        else:
            L = object.x_location - x_point
            moment = L * object.y_component
            list_of_Moments.append(moment)

    for object in list_of_Connections:
        

    return list_of_Moments


list_of_Forces = []

list_of_Moments = []

new_force = Force('down', 40, list_of_Forces, angle_from_axis=91, x_location=6)

new_force1 = Force('down', 34, list_of_Forces, angle_from_axis=45, x_location=5)

new_force2 = Force('down', 5, list_of_Forces, angle_from_axis=45, x_location=4)
# print(new_force.x_component)
# print(new_force.y_component)
# [print(object.x_component) for object in list_of_Forces]
# [print(object.x_location) for object in list_of_Forces]
#
# sm = sum_moments_at_point(0, 0, list_of_Moments, list_of_Forces)
# print(sm)

