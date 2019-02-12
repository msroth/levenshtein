"""
=====================================================================
NAME:       LD.py  (C) 2018, 2019

PURPOSE:    Calculate the Levenshtein Distance (LD) between two strings.
            The LD is the minimum numbers of edits (insert, delete, or
            substitute) to transform one string into another.

            The code calculates the LD and the minimum cost path (MCP)
            through the LD matrix.  The MCP dictates the step-by-step
            edits to make the transformation.  The code also shows the
            transformation of the source string into the target.

            This code is for educational and demonstration purposes
            only to help anyone interested understand the algorithm and
            the inner workings of the transformations.  If you really
            need to use Levenshtein distances in your code, use the
            Levenshtein Python library.

AUTHOR:     MSRoth

LAST UPDATE:  2019-02-12 -- fixed bug in working string insert operation
                         -- added calculation for Levenshtein similarity ratio

USAGE:      >python LD.py

OUTPUT:
            Final Distance Matrix:
               #  f  l  a  w
            # [0, 1, 2, 3, 4]
            l [1, 1, 1, 2, 3]
            a [2, 2, 2, 1, 2]
            w [3, 3, 3, 2, 1]
            n [4, 4, 4, 3, 2]

            Minimum Path Matrix:
               #  f  l  a  w
            # [0, 1,  ,  ,  ]
            l [ ,  , 1,  ,  ]
            a [ ,  ,  , 1,  ]
            w [ ,  ,  ,  , 1]
            n [ ,  ,  ,  , 2]

            Final Operations Matrix:
               #  f  l  a  w
            # [0, I,  ,  ,  ]
            l [ ,  , S,  ,  ]
            a [ ,  ,  , S,  ]
            w [ ,  ,  ,  , S]
            n [ ,  ,  ,  , D]

            Sequential Edits:
            lawn
            flawn <- insert 'f' (0)
            flawn <- substitute 'l' (1)
            flawn <- substitute 'a' (2)
            flawn <- substitute 'w' (3)
            flaw <- delete 'n' (4)

            Levenshtein Distance (LD) between 'lawn' and 'flaw' is: 2

COMMENTS:
            - The cost of each edit is fixed at 1.  Radically different
              results are obtained if this changes.
            - www.python-course.eu/levenshtein_distance.php
            - www.let.rug.nl/kleiweg/lev/
            - web.stanford.edu/class/cs124/lec/med.pdf
            - stackoverflow.com/questions/5849139/levenshtein-distance-inferring-the-edit-operations-from-the-matrix
            - https://www.datacamp.com/community/tutorials/fuzzy-string-python

=====================================================================
"""
# global constants
_string1 = "lawn"
_string2 = "flaw"
_del_cost = 1
_ins_cost = 1
_sub_cost = 1
_debug = 1


def get_user_input():
    """
    Get input from user.

    :return: str:source, str:target, int:debug
    """

    # note:  input forced to lower case.  Case effects LD calculations
    string1 = input("Enter first word (source) [" + str(_string1) + "]: ").strip().lower()
    if not string1:
        string1 = _string1
    string2 = input("Enter second word (target) [" + str(_string2) + "]: ").strip().lower()
    if not string2:
        string2 = _string2
    debug = input("Enter level of output (0, 1, 2) [" + str(_debug) + "]: ").strip()
    if not debug:
        debug = _debug
    if int(debug) > 2:
        debug = 2
    if int(debug) < 0:
        debug = 0

    return string1, string2, int(debug),


def print_matrix(s, t, m, p=2):
    """
    Print the matrix with the target string on top and the source
    string down the side.

    :param s: source string
    :param t: target string
    :param m: matrix to print (list of lists)
    :param p: padding factor, defaults to 2

    :return: str:output
    """
    rows = len(m)
    cols = len(m[0])
    output = "  "

    # print target word across top of matrix
    output += " #" + " " * p
    for i in range(cols - 1):
        output += str(t[i]) + " " * p
    output += "\n"

    # print source word vertically before each row
    for r in range(rows):
        if r > 0:
            output += str(s[r - 1]) + " ["
        else:
            output += "# ["

        # print matrix rows
        for c in range(cols):
            output += str(m[r][c])

            if c == cols - 1:
                output += "]\n"
            else:
                output += ", "

    print(output)
    return output


def find_min_path(s, t, dist):
    """
    Find minimum path through cost matrix, working backwards from (r,c) -> (0,0).
    Populate a sparse matrix with the cost values representing the min path.

    :param s: source string
    :param t: target string
    :param dist: LD matrix (list of lists)

    :return: list of lists:sparse_matrix

        For each "backward" step, consider the 3 cells directly adjacent to the current
        cell   (in the left, top or left+top directions)

        1.
        If the value in the diagonal cell is smaller or equal to the
        values found in the other two cells
        AND
        If this is same or 1 minus the value of the current cell then
        add a SUBSTITUTION operation

        2.
        Elseif the value in the cell to the left is smaller or equal to the value of
        the cell above current cell then add an INSERTION

        3.
        Else take the cell above, add a DELETION operation
    """

    rows = len(dist) - 1
    cols = len(dist[0]) - 1
    col = cols
    row = rows
    pos_str = "Position: (row={} col={}) -> (row={} col={})"
    cst_str = "Cost: {}"
    prev_row = row
    prev_col = col

    # init sparse path matrix
    sparse_path = [[" " for x in range(cols + 1)] for x in range(rows + 1)]
    sparse_path[0][0] = "0"

    # start with operation at (rows, cols) and work backwards
    sparse_path[rows][cols] = dist[rows][cols]

    if verbose == 2:
        print()
        print("Initial Minimum Path Matrix:")
        print_matrix(s, t, sparse_path)

    while True:

        # bail out if we are in the corner
        if row == 0 and col == 0:
            break

        # if we are not at a matrix boundary
        if row != 0 and col != 0:  # if at left edge or top row, cannot move diagonally

            # diagonal
            if (dist[row - 1][col - 1] == min(dist[row - 1][col],
                                              dist[row][col - 1],
                                              dist[row - 1][col - 1])) and (dist[row - 1][col - 1] == dist[row][col] or dist[row - 1][col - 1] == dist[row][col] - 1):
                sparse_path[row - 1][col - 1] = dist[row - 1][col - 1]
                temp_cost = dist[row - 1][col - 1]

                # move current cell
                prev_row = row
                prev_col = col
                if col > 0:
                    col -= 1
                if row > 0:
                    row -= 1

                if verbose == 2:
                    print(pos_str.format(str(prev_row), str(prev_col), str(row), str(col)))
                    print(cst_str.format(temp_cost))
                    print()

            # left
            elif dist[row][col - 1] <= dist[row][col]:
                sparse_path[row][col - 1] = dist[row][col - 1]
                temp_cost = dist[row][col - 1]

                # move current cell
                prev_row = row
                prev_col = col
                if col > 0:
                    col -= 1

                if verbose == 2:
                    print(pos_str.format(str(prev_row), str(prev_col), str(row), str(col)))
                    print(cst_str.format(temp_cost))
                    print()

            # above
            else:
                sparse_path[row - 1][col] = dist[row - 1][col]
                temp_cost = dist[row - 1][col]

                # move current cell
                prev_row = row
                prev_col = col
                if row > 0:
                    row -= 1

                if verbose == 2:
                    print(pos_str.format(str(prev_row), str(prev_col), str(row), str(col)))
                    print(cst_str.format(temp_cost))
                    print()

        # if at matrix edge, can only move up
        elif col == 0:
            # above
            sparse_path[row - 1][col] = dist[row - 1][col]
            temp_cost = dist[row - 1][col]

            # move current cell
            prev_row = row
            prev_col = col
            if row > 0:
                row -= 1

            if verbose == 2:
                print(pos_str.format(str(prev_row), str(prev_col), str(row), str(col)))
                print(cst_str.format(temp_cost))
                print()

        # must be at row boundary, can only move left
        else:
            # left
            if dist[row][col - 1] <= dist[row][col]:
                sparse_path[row][col - 1] = dist[row][col - 1]
            temp_cost = dist[row][col - 1]

            # move current cell
            prev_row = row
            prev_col = col
            if col > 0:
                col -= 1

            if verbose == 2:
                print(pos_str.format(str(prev_row), str(prev_col), str(row), str(col)))
                print(cst_str.format(temp_cost))
                print()

        # print matrix
        if verbose == 2:
            print_matrix(s, t, sparse_path)

    return sparse_path


def build_ops_matrix_and_ws(s, t, min_m):
    """
    Build a sparse matrix containing the operations associated with each
    cost in the min path matrix.  At the same time, manipulates the source
    and target strings to demonstrate edits.

    :param s: source string
    :param t: target string
    :param min_m: sparse min cost matrix

    :return: list:edits, list of lists:ops

        This logic works from (0,0) -> (rows,cols) looking for values in
        adjacent cells as it traverses the min cost matrix.  When it finds
        values, it updates the ops matrix with the edit operation that
        produced the cost.

    """

    # init edit vars
    working_string = s
    edits = [s]

    rows = len(min_m) - 1
    cols = len(min_m[0]) - 1

    # init ops matrix with spaces in each cell, except (0,0)
    ops = [[" " for x in range(cols + 1)] for x in range(rows + 1)]
    ops[0][0] = "0"

    col = 0
    row = 0

    while True:

        # bail out if we are in the corner
        if row == rows and col == cols:
            break

        # we are not at a matrix boundary
        if row != rows and col != cols:

            # down - delete
            if str(min_m[row + 1][col]).strip() != "":
                ops[row + 1][col] = "D"

                # manipulate working string with implied edit ops
                if col == 0:
                    working_string = working_string[1:]
                elif col == cols:
                    working_string = working_string[:col]
                else:
                    working_string = working_string[:col] + working_string[col + 1:]
                edits.append(working_string + " <- delete '" + str(s[row]) + "' pos: " + str(col))

                # move current cell
                if row < rows:
                    row += 1

            # right - insert
            elif str(min_m[row][col + 1]).strip() != "":
                ops[row][col + 1] = "I"

                # manipulate working string with implied edit ops
                if col == 0:
                    working_string = str(t[col]) + working_string
                elif col == cols:
                    working_string = working_string + str(t[col])
                else:
                    working_string = working_string[:row - 1] + str(t[col]) + working_string[row - 1:]
                edits.append(working_string + " <- insert '" + str(t[col]) + "' pos: " + str(col))

                # move current cell
                if col < cols:
                    col += 1

            # diagonal - sub
            else:
                ops[row + 1][col + 1] = "S"

                # manipulate working string with implied edit ops
                if col == cols:
                    working_string = working_string[:row] + str(t[col])
                else:
                    working_string = working_string[:col] + str(t[col]) + working_string[col + 1:]
                edits.append(working_string + " <- substitute '" + str(t[col]) + "' pos: " + str(col))

                # move current cell
                if row < rows:
                    row += 1
                if col < cols:
                    col += 1

        # if at matrix edge, can only move down
        elif col == cols:
            # down - delete
            if str(min_m[row + 1][col]).strip() != "":
                ops[row + 1][col] = "D"

                # manipulate working string with implied edit ops
                if row == 0:
                    working_string = working_string[1:]
                elif col == cols:
                    working_string = working_string[:col]
                else:
                    working_string = working_string[:row] + working_string[row + 1:]
                edits.append(working_string + " <- delete '" + str(s[row]) + "' pos: " + str(col))

                # update current cell
                if row < rows:
                    row += 1

        # must be at row boundary, can only move right
        else:
            # right - insert
            if str(min_m[row][col + 1]).strip() != "":
                ops[row][col + 1] = "I"

                # manipulate working string with implied edit ops
                if col == 0:
                    working_string = str(t[col]) + working_string
                elif col == cols:
                    working_string = working_string + str(t[col])
                else:
                    working_string = working_string[:row] + str(t[col]) + working_string[row:]
                edits.append(working_string + " <- insert '" + str(t[col]) + "' pos: " + str(col))

                # update current cell
                if col < cols:
                    col += 1

    return edits, ops


def find_ld(s, t, c=(1, 1, 1)):
    """
    This code calculates the LD cost matrix.  Most of this code was adopted from
    www.python-course.eu/levenshtein_distance.php.

    :param s: source string
    :param t: target string
    :param c: cost tuple [delete, insert, sub]

    :return: int:ld, list of lists:dist

        ldist is the Levenshtein distance between the strings s and t.
        For all i and j, dist[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t

        costs: a tuple or a list with three integers (d, i, s)
               where d defines the costs for a deletion
                     i defines the costs for an insertion and
                     s defines the costs for a substitution

        a horizontal move is an insertion of a letter from the 't string'
        a vertical move is a deletion of a letter from the 's string'
        a diagonal move is either:
            a no-operation (both letters at respective positions are the same)
            a substitution (letters at respective positions are distinct)
    """

    # output string templates
    pos_str = "Position: row={} col={}"
    let_str = "Letters: {} -> {}"
    op_str = "Operation: {}, Cost: {}"
    cst_str = "  {} ({},{}) cost: {}  value: {}"

    # keep the shape of the matrix consistent.  The algorithm is symmetric
    if len(s) < len(t):
        return find_ld(t, s)

    # null inputs
    if len(t) == 0:
        return len(s), []

    rows = len(s) + 1
    cols = len(t) + 1
    row = rows
    col = cols

    # get costs from input tuple
    d_cost, i_cost, s_cost = c

    # setup blank matrices to hold distances and operations
    dist = [[0 for x in range(cols)] for x in range(rows)]

    # setup delete costs
    for row in range(1, rows):
        dist[row][0] = row * d_cost

    # setup insert costs
    for col in range(1, cols):
        dist[0][col] = col * i_cost

    # print initial matrix
    if verbose == 2:
        print()
        print("Initial Matrix:")
        print_matrix(s, t, dist)

    for col in range(1, cols):
        for row in range(1, rows):

            if verbose == 2:
                print(pos_str.format(str(row), str(col)))
                print(let_str.format(str(s[row - 1]), str(t[col - 1])))

            # determine costs
            del_cost = dist[row - 1][col] + d_cost
            if verbose == 2:
                print(cst_str.format("delete", str(row - 1), str(col), str(d_cost), str(del_cost)))

            ins_cost = dist[row][col - 1] + i_cost
            if verbose == 2:
                print(cst_str.format("insert", str(row), str(col - 1), str(i_cost), str(ins_cost)))

            # sub cost could be 0 if letters are the same
            if s[row - 1] == t[col - 1]:
                sub_cost = dist[row - 1][col - 1] + 0
                if verbose == 2:
                    print(cst_str.format("substitute (no change)", str(row - 1), str(col - 1), "0", str(sub_cost)))
            else:
                sub_cost = dist[row - 1][col - 1] + s_cost
                if verbose == 2:
                    print(cst_str.format("substitute", str(row - 1), str(col - 1), str(s_cost), str(sub_cost)))

            # determine least costly operation
            if del_cost == min(del_cost, ins_cost, sub_cost):
                dist[row][col] = del_cost

            elif ins_cost == min(del_cost, ins_cost, sub_cost):
                dist[row][col] = ins_cost

            else:
                # sub_cost == min(del_cost, ins_cost, sub_cost):
                dist[row][col] = sub_cost

            # print matrix every iteration is verbose output is on
            if verbose == 2:
                print(op_str)
                print()
                print_matrix(s, t, dist)

    return dist[row][col], dist


def calc_ratio(s,t):

    # when calculating the ratio the cost of a sub=2 (it is a delete + insert)
    dist, m = find_ld(s, t, [1, 1, 2])
    ratio = ((len(s) + len(t)) - dist) / (len(s) + len(t))
    return ratio


# #### MAIN ####
print()
print("Demonstrate computation of Levenshtein Distance (LD) between two words.")
print("Determine the minimum number of edits to transform source word into target word.")
print("For example, how many substitutions, insertions, or deletions are required to")
print("turn 'house' into 'home'?  (Answer: 2), or Democrat into Republican (Answer: 8).")
print()
print("The default cost for all edit operations is 1.")
print()
print("Debug:  0 = return only the LD")
print("        1 = return LD plus distance, minimum path, and operations matrices")
print("        2 = return all intermediate matrices and computations (i.e., lots of output")
print()
print("Other fun examples:")
print("  abc       -> xyz  LD: 3")
print("  kitten    -> sitting  LD: 3")
print("  intention -> execution  LD: 5")
print("  manahaton -> manhattan  LD 3")
print("  00101010  -> 110110  LD: 3")
print()

# get user inputs
source, target, verbose = get_user_input()

# setup the costs tuple
costs = [int(_del_cost), int(_ins_cost), int(_sub_cost)]

# keep shape of matrix consistent
if len(source) < len(target):
    temp = source
    source = target
    target = temp
    print("* switching source and target words to maintain matrix shape *")

# calculate Levenshtein distance
ld, dist_m = find_ld(source, target, costs)

# calculate the Levenshtein similarity ratio
# ((len(s) + len(t)) - LD) / (len(s) + len(t))
lev_ratio = calc_ratio(source, target)

# print results
if verbose > 0:

    # navigate results matrix to find minimum path
    min_m = find_min_path(source, target, dist_m)

    # build operations matrix
    ws, ops_m = build_ops_matrix_and_ws(source, target, min_m)

    print()
    print("***** FINAL RESULTS *****")
    print()
    print("Final Distance Matrix:")
    print_matrix(source, target, dist_m)
    print()

    print("Minimum Path Matrix: ")
    print_matrix(source, target, min_m)
    print()

    print("Final Operations Matrix:")
    print_matrix(source, target, ops_m)
    print()

    print("Sequential Edits:")
    for s in ws:
        print(s)

print()
print("Levenshtein Distance (LD) between '" + source + "' and '" + target + "' is: " + str(ld))
print("Levenshtein similarity ratio is: " + str(lev_ratio))
print()

# <>< #
