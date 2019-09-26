# !/usr/bin/python2
import sys
import math
import numpy

V = {}  # dictionary to store int: numpy array
E = []
temporary_edges = []  # to save all edges temporarily.
list_of_commands = []  # this variable is used to store all the user input commands
street_coords = {}  # to save street and coordinates in dictionary
list_of_intersection = []  # used to save end points of intersecting lines
value_intersect = {}  # KEy and all end points of intersecting lines as list of points

# Classes
class point(object):

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return '(' + pp(self.x) + ', ' + pp(self.y) + ')'


def pp(x):

    if isinstance(x, float):
        if x.is_integer():
            return str(int(x))
        else:
            return "{0:.2f}".format(x)
    return str(x)


# Functions

def reading_input_line(street_line, V, E, list_of_commands, street_coords):
    # checks format of input and throws error if not in proper format
    input_command = street_line[0]
    if input_command not in ['a', 'c', 'r', 'g']:
        print "Error: please enter a valid command"
        return False

    if street_line.count("(") != street_line.count(")"):
        print "Error: format is incorrect"
        return False

    if input_command == 'g':
        list_of_commands.append(street_line)
        return True
    street_name = street_line[street_line.find("\"") + 1:street_line.rfind("\"")].lower()

    if (street_name == '') or (street_line.count("\"") != 2):
        print "Error: Please enter a valid street name "
        return False
    
    if input_command == 'a':
        if street_name in street_coords.keys():
            print "Error: I'm afraid, street already exists. Please enter different street"
            return False
        
    if input_command == 'c':
        if street_name not in street_coords.keys():
            print "Error: 'c' or 'r' specified for a street that does not exist."
            return False

    # if input is not in any of the above cases
    # take and split input into street name and coordinates

    coordinates = []
    bkup_str_line = street_line
    if input_command in ['a', 'c']:
        street_line = street_line[street_line.find("("):]
        while street_line.count(")") != 0:
            random_variable = street_line[street_line.find("(") + 1:street_line.find(")")].split(",")
            random_variable = map(float, random_variable)
            coordinates.append(point(random_variable[0], random_variable[1]))
            street_line = street_line[street_line.find(")") + 1:]
            street_coords[street_name] = coordinates

    list_of_commands.append(bkup_str_line)

    if input_command == 'r':
        if street_name in street_coords.keys():
            del street_coords[street_name]
        else:
            print "Error: OOPS! street name isn't there"
    return True


def dict_key(val):
    for k in V.keys():
        if (V[k].x == val.x) and (V[k].y == val.y):
            return k
    return False


def add_element_to_V(V, key, element):
    # adding V dictionary with element
    is_it_there = check_element_present(V, element)
    if not is_it_there:
        V[key] = element
        return True
    return False


def remove_entry_from_list(list_, p):
    for i in range(0, len(list_)):
        if (p.x == list_[i].x) and (p.y == list_[i].y):
            del list_[i]
            break
    return True


def check_element_present(dict_, element):
    
    # It checks if element present in dictionary and return true if it does

    for k in dict_.keys():
        if (dict_[k].x == element.x) and (dict_[k].y == element.y):
            return True
    return False


def add_edge_fxn(E, p1_key, p2_key):
    # it checks if (a,b) = (b,a)
    if (p1_key == 0) or (p2_key == 0):
        return False

    ex_p = point(p1_key, p2_key)
    for e in E:
        if ((e.x == p1_key) and (e.y == p2_key)) or ((e.y == p1_key) and (e.x == p2_key)):
            return False
    E.append(ex_p)
    return True


def isSamePoint(p1, p2):
    # checks is p1 and p2 are the same points or not
    if (p1.x == p2.x) and (p1.y == p2.y):
        return True
    return False


def isIntersectionPoint(p1):
    if p1 in value_intersect.values():
        return True
    return False


def isSameStreet(p1, p2):
    # checks if p1 and p2 lie on same street
    str_coor_keys = street_coords.keys()
    for k in str_coor_keys:
        if (p1 in street_coords[k]) and (p2 in street_coords[k]):
            return True
    return False


def edge_generate(E, temporary_edges):
    del E[:]
    del temporary_edges[:]
    for l in list_of_intersection:
        add_edge_fxn(temporary_edges, dict_key(l[0]), dict_key(l[1]))
        add_edge_fxn(temporary_edges, dict_key(l[0]), dict_key(l[2]))
        add_edge_fxn(temporary_edges, dict_key(l[0]), dict_key(l[3]))
        add_edge_fxn(temporary_edges, dict_key(l[0]), dict_key(l[4]))

    extra_edges = []  # edges that would be removed
    for i in range(0, len(temporary_edges) - 1):
        p1 = V[int(temporary_edges[i].x)]
        p2 = V[int(temporary_edges[i].y)]
        for j in range(i + 1, len(temporary_edges)):
            p3 = V[int(temporary_edges[j].x)]
            p4 = V[int(temporary_edges[j].y)]
            edge_created = intersection_of_edges(p1, p2, p3, p4)
            if edge_created == "correctly detected":
                extra_edges.append(temporary_edges[i])
                extra_edges.append(temporary_edges[j])

    # lets remove extra_edges
    for e in extra_edges:
        remove_entry_from_list(E, e)
    return True


def vertex_generate():
    value_intersect.clear()
    V.clear()
    del list_of_intersection[:]
    str_coor_keys = street_coords.keys()
    for i in range(0, len(str_coor_keys)):
        for a in range(0, len(street_coords[str_coor_keys[i]]) - 1):
            # selecting coordinates two at a time from first street
            p1 = street_coords[str_coor_keys[i]][a]
            p2 = street_coords[str_coor_keys[i]][a + 1]
            for j in range(i + 1, len(str_coor_keys)):
                # selecting coordinates two at a time from second street
                for b in range(0, len(street_coords[str_coor_keys[j]]) - 1):
                    # selecting coordinates two at a time from second street
                    p3 = street_coords[str_coor_keys[j]][b]
                    p4 = street_coords[str_coor_keys[j]][b + 1]
                    point_of_intersection(p1, p2, p3, p4)

    return True


def draw_graph():
    print "V = {"
    for k in V.keys():
        print "  " + str(k) + ":  (" + str(round(V[k].x, 2)) + "," + str(round(V[k].y, 2)) + ")"
    print "}"

    print "E = {"
    for e in E:
        print "  <" + str(int(e.x)) + "," + str(int(e.y)) + ">"
    print "}"

#  Intersection

def intersection_of_edges(p1, p2, p3, p4):
    # check intersection of two lines and add vertex in global variable V
    # Point should be in the format p1 = (x,y)
    det_tol = 0.00000001

    # For the first line segment
    a1, b1 = p1.x, p1.y
    a2, b2 = p2.x, p2.y
    Ax = a2 - a1
    Ay = b2 - b1

    # For the second line segment
    a3, b3 = p3.x, p3.y
    a4, b4 = p4.x, p4.y
    Bx = a4 - a3
    By = b4 - b3

    determinant = (-Ax * By + Ay * Bx)
    if math.fabs(determinant) < det_tol:
        # check if line segments are collinear
        a_b = ((p1.y - p2.y) * (p4.x - p3.x)) - ((p1.x - p3.x) * (p4.y - p3.y))
        a_c = ((p2.x - p1.x) * (p4.y - p3.y)) - ((p1.y - p3.y) * (p4.x - p3.x))
        d_b = ((p1.y - p3.y) * (p2.x - p1.x)) - ((p1.x - p3.x) * (p2.y - p1.y))
        d_c = ((p2.x - p1.x) * (p4.y - p3.y)) - ((p2.y - p1.y) * (p4.x - p3.x))

        try:
            r = a_b / a_c
        except:
            r = 100
        try:
            s = d_b / d_c
        except ZeroDivisionError:
            s = 100

        if a_c != 0 or a_b != 0:
            # adding edges to E from temporary_edges
            add_edge_fxn(E, dict_key(p1), dict_key(p2))
            add_edge_fxn(E, dict_key(p3), dict_key(p4))
            return False

        # First check for maximum length between combination of points that are collinear
        len_p1p2_e1 = math.hypot(p1.x - p2.x, p1.y - p2.y)
        len_p3p4_e2 = math.hypot(p3.x - p4.x, p3.y - p4.y)
        len_p1p3 = math.hypot(p1.x - p3.x, p1.y - p3.y)
        len_p4p2 = math.hypot(p4.x - p2.x, p4.y - p2.y)
        len_p1p4 = math.hypot(p1.x - p4.x, p1.y - p4.y)
        len_p3p2 = math.hypot(p3.x - p2.x, p3.y - p2.y)

        length_maximum = 0
        ep1, ep2 = 0, 0
        center_point1, center_point2 = 0, 0
        l_list = [len_p1p2_e1, len_p3p4_e2, len_p1p3, len_p4p2, len_p1p4, len_p3p2]  # in same order
        end_points_list = [[p1, p2], [p3, p4], [p1, p3], [p4, p2], [p1, p4], [p3, p2]]
        center_points_list = [[p3, p4], [p2, p1], [p4, p2], [p3, p1], [p3, p2], [p1, p4]]
        for i in range(0, len(l_list)):
            if l_list[i] > length_maximum:
                length_maximum = l_list[i]
                ep1, ep2 = end_points_list[i][0], end_points_list[i][1]
                center_point1, center_point2 = center_points_list[i][0], center_points_list[i][1]

        distance_from_center_points = math.hypot(center_point1.x - center_point2.x, center_point1.y - center_point2.y)
        distance_from_end_points = math.hypot(ep1.x - ep2.x, ep1.y - ep2.y)
        if (distance_from_center_points > 0) and (distance_from_end_points < (len_p1p2_e1 + len_p3p4_e2)):
            if (distance_from_end_points == len_p1p2_e1) or (distance_from_end_points == len_p3p4_e2):
                return False
            add_edge_fxn(E, dict_key(center_point1), dict_key(center_point2))
            return "correctly detected"

    else:
        # as lines are not parallel, adding edges from temporary_edges to E
        add_edge_fxn(E, dict_key(p1), dict_key(p2))
        add_edge_fxn(E, dict_key(p3), dict_key(p4))
    return True


def point_of_intersection(p1, p2, p3, p4):
    # Find if two lines intersect. If yes, add it in the globally defined V variable.
    det_tol = 0.00000001

    # For the first line segment
    a1, b1 = p1.x, p1.y
    a2, b2 = p2.x, p2.y
    Ax = a2 - a1
    Ay = b2 - b1

    # For the second line segment
    a3, b3 = p3.x, p3.y
    a4, b4 = p4.x, p4.y
    Bx = a4 - a3
    By = b4 - b3

    determinant = (-Ax * By + Ay * Bx)

    if math.fabs(determinant) < det_tol:
        a_b = ((p1.y - p2.y) * (p4.x - p3.x)) - ((p1.x - p3.x) * (p4.y - p3.y))
        a_c = ((p2.x - p1.x) * (p4.y - p3.y)) - ((p1.y - p3.y) * (p4.x - p3.x))
        d_b = ((p1.y - p3.y) * (p2.x - p1.x)) - ((p1.x - p3.x) * (p2.y - p1.y))
        d_c = ((p2.x - p1.x) * (p4.y - p3.y)) - ((p2.y - p1.y) * (p4.x - p3.x))

        try:
            r = a_b / a_c
        except:
            r = 100

        try:
            s = d_b / d_c
        except ZeroDivisionError:
            s = 100

        if a_c != 0 or a_b != 0:
            return False

        # add all the vertex to V
        add_element_to_V(V, int(len(V) + 1), p1)
        add_element_to_V(V, int(len(V) + 1), p2)
        add_element_to_V(V, int(len(V) + 1), p3)
        add_element_to_V(V, int(len(V) + 1), p4)

    else:
        det_inv = 1.0 / determinant
        s_m1 = det_inv * (-By * (a3 - a1) + Bx * (b3 - b1))
        s_m2 = det_inv * (-Ay * (a3 - a1) + Ax * (b3 - b1))

        int_x = (a1 + s_m1 * Ax + a3 + s_m2 * Bx) / 2.0
        int_y = (b1 + s_m1 * Ay + b3 + s_m2 * By) / 2.0
        dist1 = math.hypot(abs(a1 - int_x), abs(b1 - int_y))
        dist2 = math.hypot(abs(a2 - int_x), abs(b2 - int_y))
        dist3 = math.hypot(abs(a2 - a1), abs(b2 - b1))
        dist4 = math.hypot(abs(a3 - int_x), abs(b3 - int_y))
        dist5 = math.hypot(abs(a4 - int_x), abs(b4 - int_y))
        dist6 = math.hypot(abs(a4 - a3), abs(b4 - b3))

        if (round(dist6, 2) == round(dist5 + dist4, 2)) and (round(dist3, 2) == round(dist2 + dist1, 2)):
            ex_p = point(int_x, int_y)
            # adding intersection point
            add_element_to_V(V, int(len(V) + 1), ex_p)
            add_element_to_V(value_intersect, int(len(V)), ex_p)
            # adding the intersection into another dictionary
            add_element_to_V(V, int(len(V) + 1), p1)
            add_element_to_V(V, int(len(V) + 1), p2)
            add_element_to_V(V, int(len(V) + 1), p3)
            add_element_to_V(V, int(len(V) + 1), p4)
            # adding all the edges with the intersection
            list_of_intersection.append([ex_p, p1, p2, p3, p4])
        else:
            return False

    return True

# Main


def main():
    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        success = reading_input_line(line, V, E, list_of_commands, street_coords)

        if success:
            if line[0] == 'g':
                draw_graph()
            else:
                # input is one among a,r,c
                vertex_generate()
                edge_generate(E, temporary_edges)

    print 'Finished. Not reading anymore'
    sys.exit(0)


if __name__ == '__main__':
    main()

