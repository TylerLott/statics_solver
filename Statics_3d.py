import numpy as np
from numpy.linalg import inv
import math


class Member:

    def __init__(self, x_s, y_s, z_s, x_e, y_e, z_e):
        self.x_start = x_s
        self.y_start = y_s
        self.z_start = z_s
        self.x_end = x_e
        self.y_end = y_e
        self.z_end = z_e

    def start_point(self):
        x = self.x_start
        y = self.y_start
        z = self.z_start

        return [x, y, z]

    def end_point(self):
        x = self.x_end
        y = self.y_end
        z = self.z_end

        return [x, y, z]

    def line_vec(self):
        i = self.x_end - self.x_start
        j = self.y_end - self.y_start
        k = self.z_end - self.z_start

        return [i, j, k]

    def find_length(self):
        i = self.x_end - self.x_start
        j = self.y_end - self.y_start
        k = self.z_end - self.z_start
        sq = i ** 2 + j ** 2 + k ** 2
        length = np.sqrt(sq)

        return length


# find if force is on a line by finding its distance from the

# create a Member class that the forces must act on
# might be a better option to restrict this with the UI
# if you create a member class you could potentially do frame and machines though

class ForceGen:
    # this class is used to generate the forces for the problem
    # as it creates the forces it puts them into a list
    # this list is used by all of the sum and equation methods
    forces = []

    def __init__(self, x, y, z, i, j, k):
        self.x = Force(x, y, z, i, j, k)
        self.forces.append(self.x)
        self.ret()

    def ret(self):
        return self.x


class Force:

    def __init__(self, x, y, z, i, j, k):
        self.x = x
        self.y = y
        self.z = z
        self.i = i
        self.j = j
        self.k = k

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_i(self):
        return self.i

    def get_j(self):
        return self.j

    def get_k(self):
        return self.k


class MomentGen:
    # this class is used to generate the forces for the problem
    # as it creates the forces it puts them into a list
    # this list is used by all of the sum and equation methods
    moments = []

    def __init__(self, x, y, z, a, b, c):
        self.x = Moment(x, y, z, a, b, c)
        self.moments.append(self.x)
        self.ret()

    def ret(self):
        return self.x


class Moment:

    def __init__(self, x, y, z, a, b, c):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_a(self):
        return self.a

    def get_b(self):
        return self.b

    def get_c(self):
        return self.c


class ForceAreaGen:
    # this class is used to generate the forces for the problem
    # as it creates the forces it puts them into a list
    # this list is used by all of the sum and equation methods
    forceAreas = []

    def __init__(self, x, y, z, a, b, c):
        self.x = ForceArea(x, y, z, a, b, c)
        self.forceAreas.append(self.x)
        self.ret()

    def ret(self):
        return self.x


class ForceArea:
    # This takes a force area and outputs an equivalent point force in order to be able to calculate the forces for the
    # unknown forces and moments in the model input by the user.

    def __init__(self, x_1, y_1, z_1, x_2, y_2, z_2, i_1, j_1, k_1, i_2, j_2, k_2):
        self.x_1 = x_1
        self.y_1 = y_1
        self.z_1 = z_1
        self.x_2 = x_2
        self.y_2 = y_2
        self.z_2 = z_2
        self.i_1 = i_1
        self.j_1 = j_1
        self.k_1 = k_1
        self.i_2 = i_2
        self.j_2 = j_2
        self.k_2 = k_2
        self.point_force_eqi()

    def point_force_eqi(self):
        x_avg = self.x_2 - self.x_1
        y_avg = self.y_2 - self.y_1
        z_avg = self.z_2 - self.z_1

        i_avg = self.i_2 - self.i_1
        j_avg = self.j_2 - self.j_1
        k_avg = self.k_2 - self.k_1

        ForceGen(x_avg, y_avg, z_avg, i_avg, j_avg, k_avg)

    


# define classes for all of the support types
# Rigid, Ball-joint, Simple, Bearing, Hinge
class Support:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rigid(self):
        ForceGen(self.x, self.y, self.z, 'unk', 0, 0)
        ForceGen(self.x, self.y, self.z, 0, 'unk', 0)
        ForceGen(self.x, self.y, self.z, 0, 0, 'unk')
        MomentGen(self.x, self.y, self.z, 'unk', 0, 0)
        MomentGen(self.x, self.y, self.z, 0, 'unk', 0)
        MomentGen(self.x, self.y, self.z, 0, 0, 'unk')

    def balljoint(self):
        ForceGen(self.x, self.y, self.z, 'unk', 0, 0)
        ForceGen(self.x, self.y, self.z, 0, 'unk', 0)
        ForceGen(self.x, self.y, self.z, 0, 0, 'unk')

    def simple_x(self):
        ForceGen(self.x, self.y, self.z, 'unk', 0, 0)

    def simple_y(self):
        ForceGen(self.x, self.y, self.z, 0, 'unk', 0)

    def simple_z(self):
        ForceGen(self.x, self.y, self.z, 0, 0, 'unk')

    def bearing_x(self):
        ForceGen(self.x, self.y, self.z, 0, 'unk', 0)
        ForceGen(self.x, self.y, self.z, 0, 0, 'unk')
        MomentGen(self.x, self.y, self.z, 0, 'unk', 0)
        MomentGen(self.x, self.y, self.z, 0, 0, 'unk')

    def bearing_y(self):
        ForceGen(self.x, self.y, self.z, 'unk', 0, 0)
        ForceGen(self.x, self.y, self.z, 0, 0, 'unk')
        MomentGen(self.x, self.y, self.z, 'unk', 0, 0)
        MomentGen(self.x, self.y, self.z, 0, 0, 'unk')

    def bearing_z(self):
        ForceGen(self.x, self.y, self.z, 'unk', 0, 0)
        ForceGen(self.x, self.y, self.z, 0, 'unk', 0)
        MomentGen(self.x, self.y, self.z, 'unk', 0, 0)
        MomentGen(self.x, self.y, self.z, 0, 'unk', 0)

    def hinge_x(self):
        ForceGen(self.x, self.y, self.z, 'unk', 0, 0)
        ForceGen(self.x, self.y, self.z, 0, 'unk', 0)
        ForceGen(self.x, self.y, self.z, 0, 0, 'unk')
        MomentGen(self.x, self.y, self.z, 0, 'unk', 0)
        MomentGen(self.x, self.y, self.z, 0, 0, 'unk')

    def hinge_y(self):
        ForceGen(self.x, self.y, self.z, 'unk', 0, 0)
        ForceGen(self.x, self.y, self.z, 0, 'unk', 0)
        ForceGen(self.x, self.y, self.z, 0, 0, 'unk')
        MomentGen(self.x, self.y, self.z, 'unk', 0, 0)
        MomentGen(self.x, self.y, self.z, 0, 0, 'unk')

    def hinge_z(self):
        ForceGen(self.x, self.y, self.z, 'unk', 0, 0)
        ForceGen(self.x, self.y, self.z, 0, 'unk', 0)
        ForceGen(self.x, self.y, self.z, 0, 0, 'unk')
        MomentGen(self.x, self.y, self.z, 'unk', 0, 0)
        MomentGen(self.x, self.y, self.z, 0, 'unk', 0)


def sum_x():
    sum_i = 0
    for instance in ForceGen.forces:
        if instance.get_i() != 'unk':
            sum_i += instance.get_i()
    return -sum_i
    # get all the <i> components of the force vectors and add them
    # if the force is 'unk' then it passes


def sum_y():
    sum_j = 0
    for instance in ForceGen.forces:
        if instance.get_j() != 'unk':
            sum_j += instance.get_j()
    return -sum_j
    # get all the <j> components of the force vectors and add them
    # if the force is 'unk' then it passes


def sum_z():
    sum_k = 0
    for instance in ForceGen.forces:
        if instance.get_k() != 'unk':
            sum_k += instance.get_k()
    return -sum_k
    # get all the <k> components of the force vectors and add them
    # if the force is 'unk' then it passes


def sum_moments():
    # get distance from the point moment is taken at to each of the other forces
    # calculate the moment by using the cross product of the position vector and the force vector
    # this gives the moment about each axis <a,b,c>
    # add all a's, b's, and c's including those from the Moments to find the sum about each axis at that point
    # if the force is 'unk' then it passes
    # returns a list of lists formatted:
    # [[sum_a_point1, sum_b_point1, sum_c_point1], [sum_a_point2, sum_b_point2, sum_c_point2], ... ]
    sums_m = []
    for instance in ForceGen.forces:
        point = []
        sum_a = 0
        sum_b = 0
        sum_c = 0
        for compare in ForceGen.forces:
            x = compare.get_x() - instance.get_x()
            y = compare.get_y() - instance.get_y()
            z = compare.get_z() - instance.get_z()
            if compare.get_i() == 'unk':
                i = 0
            else:
                i = compare.get_i()
            if compare.get_j() == 'unk':
                j = 0
            else:
                j = compare.get_j()
            if compare.get_k() == 'unk':
                k = 0
            else:
                k = compare.get_k()
            a = [x, y, z]
            b = [i, j, k]
            moments = cross_vec(a, b)
            sum_a += -moments[0]
            sum_b += -moments[1]
            sum_c += -moments[2]
        for compare in MomentGen.moments:
            if compare.get_a() != 'unk':
                sum_a += -compare.get_a()
            if compare.get_b() != 'unk':
                sum_b += -compare.get_b()
            if compare.get_c() != 'unk':
                sum_c += -compare.get_c()
        point.append(sum_a)
        point.append(sum_b)
        point.append(sum_c)
        sums_m.append(point)
    return sums_m


def eq_x():
    # finds all of the <i> components that are labeled 'unk'
    # puts a 1 in their place then moves on
    eq_i = []
    for instance in ForceGen.forces:
        if instance.get_i() != 'unk':
            eq_i.append(0)
            eq_i.append(0)
            eq_i.append(0)
        elif instance.get_i() == 'unk':
            eq_i.append(1)
            eq_i.append(0)
            eq_i.append(0)
    # adds zeros for moments in total matrix
    for number in range(len(MomentGen.moments)):
        eq_i.append(0)
        eq_i.append(0)
        eq_i.append(0)

    return eq_i


def eq_y():
    # finds all of the <j> components that are labeled 'unk'
    # puts a 1 in their place then moves on
    eq_j = []
    for instance in ForceGen.forces:
        if instance.get_j() != 'unk':
            eq_j.append(0)
            eq_j.append(0)
            eq_j.append(0)
        elif instance.get_j() == 'unk':
            eq_j.append(0)
            eq_j.append(1)
            eq_j.append(0)
    # adds zeros for moments in total matrix
    for number in range(len(MomentGen.moments)):
        eq_j.append(0)
        eq_j.append(0)
        eq_j.append(0)
    return eq_j


def eq_z():
    # finds all of the <k> components that are labeled 'unk'
    # puts a 1 in their place then moves on
    eq_k = []
    for instance in ForceGen.forces:
        if instance.get_k() != 'unk':
            eq_k.append(0)
            eq_k.append(0)
            eq_k.append(0)
        elif instance.get_k() == 'unk':
            eq_k.append(0)
            eq_k.append(0)
            eq_k.append(1)
    # adds zeros for moments in total matrix
    for number in range(len(MomentGen.moments)):
        eq_k.append(0)
        eq_k.append(0)
        eq_k.append(0)
    return eq_k


def eq_moment():
    # finds all crosses of positional vectors and 'unk' forces
    # places each 'unk' force with distance into the correct position of the matrix row
    # gives a list that contains points
    # each point contains a list of moments
    # each moment contains component forces that make up that moment, and the pure moments
    eqs_m = []
    for instance in ForceGen.forces:
        eq_a = []
        eq_b = []
        eq_c = []
        for compare in ForceGen.forces:
            x = compare.get_x() - instance.get_x()
            y = compare.get_y() - instance.get_y()
            z = compare.get_z() - instance.get_z()
            i = compare.get_i()
            j = compare.get_j()
            k = compare.get_k()
            a = [x, y, z]
            b = [i, j, k]
            moments = cross_vec_unk(a, b)
            # gives a, b, and c that are all 3 dimensional vectors
            for comp in range(len(moments[0])):
                eq_a.append(moments[0][comp])
            for comp in range(len(moments[1])):
                eq_b.append(moments[1][comp])
            for comp in range(len(moments[2])):
                eq_c.append(moments[2][comp])
        point = [eq_a, eq_b, eq_c]

        for compare in MomentGen.moments:
            if compare.get_a() == 'unk':
                point[0].append(1)
                point[1].append(0)
                point[2].append(0)
            else:
                point[0].append(0)
                point[1].append(0)
                point[2].append(0)
            if compare.get_b() == 'unk':
                point[0].append(0)
                point[1].append(1)
                point[2].append(0)
            else:
                point[0].append(0)
                point[1].append(0)
                point[2].append(0)
            if compare.get_c() == 'unk':
                point[0].append(0)
                point[1].append(0)
                point[2].append(1)
            else:
                point[0].append(0)
                point[1].append(0)
                point[2].append(0)
            # eq_a should look like[1i, 1j, 1k, 2i, 2j, 2k, ... , 1ma, 1mb, 1mc, 2ma, 2mb, 2mc, ... ]
        eqs_m.append(point)
    return eqs_m


def on_member(line_pt_1, line_pt_2, point_x, point_y, point_z):
    # line start point
    x_1 = line_pt_1[0]
    y_1 = line_pt_1[1]
    z_1 = line_pt_1[2]

    # line end point
    x_2 = line_pt_2[0]
    y_2 = line_pt_2[1]
    z_2 = line_pt_2[2]

    # |A cross B| / |A|

    A = [x_2 - x_1, y_2 - y_1, z_2 - z_1]
    B = [x_1 - point_x, y_1 - point_y, z_1 - point_z]

    cross = cross_vec(A, B)

    mag_1 = 0
    mag_2 = 0

    for num in range(len(cross)):
        cross[num] = cross[num] ** 2
        B[num] = B[num] ** 2
        mag_1 += cross[num]
        mag_2 += B[num]

    distance = mag_1 / mag_2

    # distance from each of the points of a member
    dist_1 = [x_1 - point_x, y_1 - point_y, z_1 - point_z]
    dist_2 = [x_2 - point_x, y_2 - point_y, z_2 - point_z]

    mag_d_1 = 0
    mag_d_2 = 0

    for num in range(len(dist_1)):
        dist_1[num] = dist_1[num] ** 2
        dist_2[num] = dist_2[num] ** 2
        mag_d_1 += dist_1[num]
        mag_d_2 += dist_2[num]

    between_points = False
    if mag_d_2 >= 0 >= mag_d_1 or mag_d_1 >= 0 >= mag_d_2:
        between_points = True

    if between_points is True and distance < .001:
        return True
    else:
        return False


def cross_vec(vec_a, vec_b):
    # vector a should be the position vector in <x,y,z> form
    # vector b should be the force vector in <i,j,k> form
    # gives return vector with <a, b, c> , the moments in each axis
    a = (vec_a[1] * vec_b[2]) - (vec_a[2] * vec_b[1])
    b = (vec_a[0] * vec_b[2]) - (vec_a[2] * vec_b[0])
    c = (vec_a[0] * vec_b[1]) - (vec_a[1] * vec_b[0])
    return [a, b, c]


def cross_vec_unk(vec_a, vec_b):
    # gives <a,b,c> each in <i,j,k> format
    # ex. a = <i,j,k>
    a_i = 0

    # a components
    if vec_b[1] == 'unk':
        a_j = -vec_a[2]
    else:
        a_j = 0

    if vec_b[2] == 'unk':
        a_k = vec_a[1]
    else:
        a_k = 0

    # b components
    if vec_b[0] == 'unk':
        b_i = -vec_a[2]
    else:
        b_i = 0

    b_j = 0

    if vec_b[2] == 'unk':
        b_k = vec_a[0]
    else:
        b_k = 0

    # c components
    if vec_b[0] == 'unk':
        c_i = -vec_a[1]
    else:
        c_i = 0

    if vec_b[1] == 'unk':
        c_j = vec_a[0]
    else:
        c_j = 0

    c_k = 0

    a = [a_i, a_j, a_k]
    b = [b_i, b_j, b_k]
    c = [c_i, c_j, c_k]

    return [a, b, c]


def all_eqs():
    #
    all_eqs_ = []
    all_eqs_.append(eq_x())
    all_eqs_.append(eq_y())
    all_eqs_.append(eq_z())
    for points in eq_moment():
        for equation in points:
            all_eqs_.append(equation)
    return all_eqs_


def all_sums():
    # gets all sums of equations and puts them in a list starting with forces in x, y, z then moving onto the moments
    all_sums_ = []
    all_sums_.append(sum_x())
    all_sums_.append(sum_y())
    all_sums_.append(sum_z())
    for points in sum_moments():
        for sums in points:
            all_sums_.append(sums)
    return all_sums_


def format_matrix(a_matrix, b_matrix):
    # removes any rows that are all zeros
    zero_rows = []
    for row in range(len(a_matrix)):
        counter = 0
        for number in a_matrix[row]:
            if abs(number) < .0001:
                counter += 1
            if counter == len(a_matrix[row]):
                zero_rows.append(row)
    for index in sorted(zero_rows, reverse=True):
        a_matrix.pop(index)
        b_matrix.pop(index)

    # removes any columns containing all zeros
    zero_columns = []
    for column_index in range(len(a_matrix[0])):
        counter = 0
        for row_index in range(1, len(a_matrix)):
            row_index_2 = row_index - 1
            if a_matrix[row_index][column_index] == a_matrix[row_index_2][column_index]:
                counter += 1
                if counter == len(a_matrix) - 1:
                    zero_columns.append(column_index)
    for column_index in sorted(zero_columns, reverse=True):
        for rows in range(len(a_matrix)):
            a_matrix[rows].pop(column_index)

    # formats the remaining matrix to the same height as width
    # create list numbered zero to the number of columns
    # if the index for the row is not in that list then pop that index for both a and b matrix
    column_counter = 0
    for row in range(1):
        for columns in range(len(a_matrix[0])):
            column_counter += 1
    for row in reversed(range(column_counter, len(a_matrix))):
        a_matrix.pop(row)
        b_matrix.pop(row)

    return a_matrix, b_matrix


def solve():
    matrix = format_matrix(all_eqs(), all_sums())
    a_matrix = matrix[0]
    b_matrix = matrix[1]
    list_of_answers = np.matmul(inv(a_matrix), b_matrix)
    return list_of_answers


def convert_angle_mag_input():
    pass


# create a force area class
    # takes:
        # start x,y,z
        # end x,y,z
        # start i,j,k
        # end i,j,k
        # or just a function for the change in x,y,z
    # finds center of mass of the forces and converts to a point force for the static analysis

# create a shear and Bending moment between any two points
    # takes:
        # start x,y,z
        # end x,y,z
    # finds:
        # all forces along the line using distance from line linear algebra formula
        # all force areas along the line using distance from line to the converted point force, then uses the equation for
        # the change in the force to find the shear and bending moment at any point on the bar
        # all the forces at the start and end points of the member
    # gives:
        # i,j,k for the shear force at any point between the start and end
        # a,b,c bending moments at any point between the start and end

# create a method to find the eigenvalues of the a matrix to determine if its determinant

# create method to determine if a point at the end of the member has 2 connections to the other point on that member
# if it does then it cant be done because its some sort of truss or frame
# if it doesnt then sum the forces on each side of the member by comparing the points to the points of all other members
# also sum all of the moments
# use those moments and forces as acting on that point of the member
# find all forces between the members and use them in the shear and moment calculations
# to get the shear and moment calculations select a number of points between the points to calculate the magnitudes

# create a method that removes any moments that are cancelled out by bearing or hinge forces at different points


# output answers in angles and degrees


def main():
    # forces
    ForceGen(0, 0, 0, 'unk', 'unk', 'unk')
    ForceGen(.5, 4, 0, 60, -40, 57)
    ForceGen(1, 0, 0, 8, -190, 10)

    # moments
    MomentGen(0, 0, 0, 'unk', 'unk','unk')

    # solve
    print(solve())


if __name__ == "__main__":
    main()
