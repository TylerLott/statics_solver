import numpy as np
from numpy.linalg import inv
import math

SUPPORTS = 1
NUMBER_OF_FORCES = 1
NUMBER_OF_MOMENTS = 1

class Member:
    def __init__(self, x_start, y_start, list_of_Members, x_end=0, y_end=0, angle_from_axis=0, length=0):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.angle_from_axis = angle_from_axis
        self.length = length
        self.list_of_Members = list_of_Members

        self.create_member()

    def create_member(self):
        if self.angle_from_axis == 0 and self.length == 0:
            member = [[self.x_start, self.y_start], [self.x_end, self.y_end]]
            self.list_of_Members.append(member)
        elif self.x_end == 0 and self.y_end == 0:
            x_end = self.length * np.cos(np.radians(self.angle_from_axis))
            y_end = self.length * np.sin(np.radians(self.angle_from_axis))
            member = [[self.x_start, self.y_start], [x_end, y_end]]
            self.list_of_Members.append(member)

        return self.list_of_Members


class Force:
    # direction = 'down' or 'up'
    # magnitude = float
    # angle from axis = angle in degrees from pos x, counter clockwise
    # x location is in units of length
    # list_of_Forces = list
    def __init__(self, direction, magnitude, list_of_Forces, list_of_Members, angle_from_axis=0, x_location=0, y_location=0):
        self.direction = direction
        self.magnitude = magnitude
        self.angle_from_axis = angle_from_axis
        self.x_location = x_location
        self.y_location = y_location
        self.list_of_Forces = list_of_Forces
        self.list_of_Members = list_of_Members

        self.get_direction_sign()
        self.create_new_force_x()

    def get_angle(self):
        return self.angle_from_axis

    def get_x_location(self):
        return self.x_location

    def get_y_location(self):
        return self.y_location

    def get_magnitude(self):
        return self.magnitude

    def get_direction_sign(self):
        if self.direction == 'down':
            self.direction = -1
        else:
            self.direction = 1

    # finds the distance between the point of the force and the member, only creates the force if the distance is 0
    def find_on_member(self):
        for i in self.list_of_Members:
            line_point1_x = self.list_of_Members[0][0][0]
            line_point1_y = self.list_of_Members[0][0][1]
            line_point2_x = self.list_of_Members[0][1][0]
            line_point2_y = self.list_of_Members[0][1][1]

            a_vec = [self.x_location - line_point1_x, self.y_location - line_point1_y]
            b_vec = [line_point2_x - line_point1_x, line_point2_y - line_point1_y]
            if cross_products_2d(a_vec, b_vec) == 0:
                return True
        return False

    def create_new_force_x(self):
        if self.find_on_member() == True:
            self.list_of_Forces = self.list_of_Forces.append(self)
            return self.list_of_Forces
        else:
            return 'force at x = ', self.x_location, ' and y = ', self.y_location, 'does not act on any member'

    def find_x_comp(self):
        x_comp = -1 * np.cos(math.radians(self.angle_from_axis))
        return x_comp

    def find_y_comp(self):
        y_comp = self.direction * np.sin(math.radians(self.angle_from_axis))
        return y_comp


# this is only for reactionary  or applied moments
class Moment:
    # + is counter-clockwise, - is clockwise
    def __init__(self, direction, magnitude, x_location, y_location, list_of_Moments):
        self.direction = direction
        self.magnitude = magnitude
        self.list_of_Moments = list_of_Moments
        self.x_location = x_location
        self.y_location = y_location

        self.find_mag_with_dir()
        self.create_new_moment()

    def get_direction(self):
        if self.direction == '-':
            return 'clock-wise'
        if self.direction == '+':
            return 'counter clock-wise'

    def get_x_location(self):
        return self.x_location

    def get_y_location(self):
        return self.y_location

    def create_new_moment(self):
        self.list_of_Moments = self.list_of_Moments.append(self)
        return self.list_of_Moments

    def get_magnitude(self):
        return self.magnitude

    def find_mag_with_dir(self):
        if self.direction == '-':
            self.magnitude = -1 * self.magnitude
        return self.magnitude


class Force_Area:
    def __init__(self, direction, magnitude_equation, x_left, x_right):
        self.direction = direction
        self.magnitude_equation = magnitude_equation
        self.x_left = x_left
        self.x_right = x_right


class Pin_Connection:
    # reaction_x and reaction_y should be objects of Force
    def __init__(self, reaction_x, reaction_y, list_of_Forces, list_of_Members, x_point=0, y_point=0):
        self.reaction_x = reaction_x
        self.reaction_y = reaction_y
        self.x_point = x_point
        self.y_point = y_point

        force_x = Force('up', self.reaction_x, list_of_Forces, list_of_Members, x_location=self.x_point,
                        y_location=self.y_point, angle_from_axis=0)

        force_y = Force('up', self.reaction_y, list_of_Forces, list_of_Members, x_location=self.x_point,
                        y_location=self.y_point, angle_from_axis=90)



class Roller_Connection:
    # reaction_y should be object of Force
    def __init__(self, reaction_y, list_of_Forces, list_of_Members, x_point=0, y_point=0):
        self.reaction_y = reaction_y
        self.x_point = x_point
        self.y_point = y_point

        force_y = Force('up', self.reaction_y, list_of_Forces, list_of_Members, x_location=self.x_point,
                        y_location=self.y_point, angle_from_axis=90)


class Fixed_Connection:
    # reaction_x and reaction_y should be objects of Force
    # reaction_moment should be objects of Moment
    def __init__(self, reaction_x, reaction_y, reaction_moment, list_of_Moments, list_of_Members, x_point=0, y_point=0):
        self.reaction_x = reaction_x
        self.reaction_y = reaction_y
        self.reaction_moment = reaction_moment
        self.x_point = x_point
        self.y_point = y_point

        force_x = Force('up', self.reaction_x, list_of_Forces, list_of_Members, x_location=self.x_point,
                        y_location=self.y_point, angle_from_axis=0)

        force_y = Force('up', self.reaction_y, list_of_Forces, list_of_Members, x_location=self.x_point,
                        y_location=self.y_point, angle_from_axis=90)

        moment = Moment('+', self.reaction_moment, x_point, y_point, list_of_Moments)

def cross_products_2d(a_vector, b_vector):
    cross = a_vector[0] * b_vector[1] - a_vector[1] * b_vector[0]
    return cross



def sum_forces_x(list_of_Forces):
    sum_x = 0
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_magnitude() == 'find':
            continue
        else:
            sum_x += list_of_Forces[i].get_magnitude() * list_of_Forces[i].find_x_comp()
    return -sum_x


def sum_forces_y(list_of_Forces):
    sum_y = 0
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_magnitude() == 'find':
            continue
        else:
            sum_y += list_of_Forces[i].get_magnitude() * list_of_Forces[i].find_y_comp()
    return -sum_y


def sum_moments_at_point(x_point, y_point, list_of_Forces, list_of_Moments):
    sum_m = 0
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_magnitude() == 'find':
            continue
        else:
            if list_of_Forces[i].find_x_comp() >= .001 and list_of_Forces[i].find_y_comp() >= .001:
                sum_m += ((list_of_Forces[i].find_x_comp() * list_of_Forces[i].get_magnitude())
                          * (list_of_Forces[i].get_x_location() - x_point))
            elif list_of_Forces[i].find_x_comp() <= .001:
                sum_m += ((list_of_Forces[i].find_y_comp() * list_of_Forces[i].get_magnitude())
                          * (list_of_Forces[i].get_x_location() - x_point))
            elif list_of_Forces[i].find_y_comp() <= .001:
                sum_m += ((list_of_Forces[i].find_x_comp() * list_of_Forces[i].get_magnitude())
                          * (list_of_Forces[i].get_y_location() - y_point))
    for i in range(len(list_of_Moments)):
        if list_of_Moments[i].get_magnitude() == 'find':
            continue
        else:
            sum_m += list_of_Moments[i].find_mag_with_dir()

    return -sum_m


def forces_x(list_of_Forces):
    list_of_forces_x = []
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_magnitude() != 'find':
            list_of_forces_x.append(0)
        else:
            value = list_of_Forces[i].find_x_comp()
            list_of_forces_x.append(value)

    return list_of_forces_x


def forces_y(list_of_Forces):
    list_of_forces_y = []
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_magnitude() != 'find':
            list_of_forces_y.append(0)
            continue
        else:
            value = list_of_Forces[i].find_y_comp()
            list_of_forces_y.append(value)

    return list_of_forces_y


def moment_eq_at_point(x_location, y_location, list_of_Forces, list_of_Moments):
    list_of_moments = []
    for i in range(len(list_of_Forces)):
        if list_of_Forces[i].get_x_location() == x_location and list_of_Forces[i].get_y_location() == y_location:
            list_of_moments.append(0)
            continue
        elif list_of_Forces[i].get_magnitude() != 'find':
            list_of_moments.append(0)
            continue
        elif list_of_Forces[i].get_magnitude() == 'find':
            if list_of_Forces[i].find_x_comp() <= .001 and list_of_Forces[i].find_y_comp() <= 0.001:
                value = list_of_Forces[i].find_x_comp() * (list_of_Forces[i].get_y_location() - y_location)
                list_of_moments.append(value)
                continue
            elif list_of_Forces[i].find_x_comp() <= 0.001:
                value = list_of_Forces[i].find_y_comp() * (list_of_Forces[i].get_x_location() - x_location)
                list_of_moments.append(value)
                continue
            elif list_of_Forces[i].find_y_comp() <= 0.001:
                value = list_of_Forces[i].find_x_comp() * (list_of_Forces[i].get_y_location() - y_location)
                list_of_moments.append(value)
                continue
    for i in range(len(list_of_Moments)):
        if list_of_Moments[i].get_magnitude() != 'find':
            list_of_moments.append(0)
            continue
        elif list_of_Moments[i]:
            # assumes unknown moments are going counter-clockwise
            list_of_moments.append(1)
    return list_of_moments


def find_a_matrix(list_of_Forces, list_of_Moments):

    x = forces_x(list_of_Forces)
    y = forces_y(list_of_Forces)

    for i in range(len(list_of_Moments)):
        x.append(0)
        y.append(0)
    a_matrix = [x, y]

    for i in range(len(list_of_Forces)):
        new_moment_eq = moment_eq_at_point(list_of_Forces[i].get_x_location(),
                                           list_of_Forces[i].get_y_location(),
                                           list_of_Forces,
                                           list_of_Moments)
        a_matrix.append(new_moment_eq)

    return a_matrix


def find_b_matrix(list_of_Forces, list_of_Moments):
    b_matrix = [[sum_forces_x(list_of_Forces)], [sum_forces_y(list_of_Forces)]]

    moment_locations = []

    for i in range(len(list_of_Forces)):
        new_moment_sum = [sum_moments_at_point(list_of_Forces[i].get_x_location(),
                                               list_of_Forces[i].get_y_location(),
                                               list_of_Forces,
                                               list_of_Moments)]
        current_location = (list_of_Forces[i].get_x_location(), list_of_Forces[i].get_y_location())

        b_matrix.append(new_moment_sum)
        moment_locations.append((list_of_Forces[i].get_x_location(), list_of_Forces[i].get_y_location()))

    return b_matrix


def solve(a_matrix, b_matrix):

    # creates a new matrix with out any zero equations
    index = []
    new_a_matrix = []
    for i in range(len(a_matrix)):
        for ii in range(len(a_matrix[i])):
            # print(a_matrix[i][ii])
            if abs(a_matrix[i][ii]) > .001:
                index.append(i)
                new_a_matrix.append(a_matrix[i])
                break

    # creates new b matrix to match a matrix
    new_b_matrix = []
    for i in index:
        new_b_matrix.append(b_matrix[i])

    # creates an equation with no repeat equations
    index_2 = []
    new_a_matrix_2 = []
    for i in range(len(new_a_matrix)):
        if new_a_matrix[i] not in new_a_matrix_2:
            index_2.append(i)
            new_a_matrix_2.append(new_a_matrix[i])

    # creates new b matrix to match a matrix again
    new_b_matrix_2 = []
    for i in index_2:
        new_b_matrix_2.append(new_b_matrix[i])

    # gets rid of any empty columns
    empty_columns = []
    for i in range(len(new_a_matrix_2[0])):
        counter = 0
        for ii in range(1, len(new_a_matrix_2)):
            x = ii - 1
            if new_a_matrix_2[ii][i] == new_a_matrix_2[x][i]:
                counter += 1
                if counter == len(new_a_matrix_2) - 1:
                    empty_columns.append(i)

    for i in sorted(empty_columns, reverse=True):
        for ii in range(len(new_a_matrix_2)):
            for iii in range(len(new_a_matrix_2[ii])):
                new_a_matrix_2[ii].pop(i)
                break

    # reshapes to be square
    new_a_matrix_3 = []
    new_b_matrix_3 = []
    for i in range(len(new_a_matrix_2[0])):
        new_a_matrix_3.append(new_a_matrix_2[i])
        new_b_matrix_3.append(new_b_matrix_2[i])

    list_of_answers = np.matmul(inv(new_a_matrix_3), new_b_matrix_3)
    return list_of_answers


list_of_Members = []
list_of_Forces = []
list_of_Moments = []
list_of_unknown = []

new_member = Member(0, 0, list_of_Members, x_end=100, y_end=0)

new_force = Force('down', 300, list_of_Forces, list_of_Members, angle_from_axis=90, x_location=50, y_location=0)
#
# new_force1 = Force('up', 90, list_of_Forces, list_of_Members, angle_from_axis=90, x_location=2)
#
new_force4 = Force('down', 80, list_of_Forces, list_of_Members, angle_from_axis=90, x_location=20)
#
# new_force2 = Force('up', 'find', list_of_Forces, list_of_Members, angle_from_axis=90, x_location=2)
#
new_connection = Roller_Connection('find', list_of_Forces, list_of_Members, x_point=100)

new_connection_2 = Pin_Connection('find', 'find', list_of_Forces, list_of_Members, x_point=0, y_point=0)

for i in list_of_Forces:
    if i.magnitude == 'find':
        list_of_unknown.append(['force located at: (' + str(i.get_x_location()) + ', ' + str(i.get_y_location()) +
                                ') in direction ' + str(i.get_angle()) + ' degrees from member'])

for i in list_of_Moments:
    if i.magnitude == 'find':
        list_of_unknown.append(['moment located at (' + str(i.get_x_location()) + ', ' + str(i.get_y_location()) +
                                ') in ' + str(i.get_direction())])

# print(list_of_unknown)

b = find_b_matrix(list_of_Forces, list_of_Moments)
a = find_a_matrix(list_of_Forces, list_of_Moments)

list_of_answers = solve(a,b)

for i in range(len(list_of_unknown)):
    print(list_of_unknown[i], list_of_answers[i])



