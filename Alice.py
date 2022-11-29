import sys

if len(sys.argv) != 2:
    print("Usage: python3 Alice.py <inputfilename>")
    sys.exit()

f = open(sys.argv[1])

grid_size = int(f.readline())
properties = []

for i in range(grid_size ** 2):  # for each vertex in the graph
    properties.append(f.readline().split())

starting_vertex = None
adjacency = {}  # create adjacency dictionary

for i in range(grid_size ** 2):  # for each node, add the adjacent vertices to the dictionary
    adjacent = []  # tuples corresponding to each arrow in the maze will be appended to this list
    # each tuple is of the form:
    # (destination node: int, colour: str, d: int)
    if properties[i][2] == 'goal':
        goal_vertex = i
    if properties[i][2] == 'arrow' or properties[i][2] == 'start':
        if properties[i][2] == 'start':
            starting_vertex = i
        arrow_colour = properties[i][3]
        arrows = properties[i][4:]
        for arrow in arrows:
            if arrow == 'n':
                for j in range(int(properties[i][1])):
                    adjacent.append((i - (j + 1) * grid_size, arrow_colour, j + 1))
            elif arrow == 'ne':
                for j in range(min(int(properties[i][1]), grid_size - 1 - int(properties[i][0]))):
                    adjacent.append((i - (j + 1) * grid_size + (j + 1), arrow_colour, j + 1))
            elif arrow == 'e':
                for j in range(grid_size - 1 - int(properties[i][0])):
                    adjacent.append((i + (j + 1), arrow_colour, j + 1))
            elif arrow == 'se':
                for j in range(min(grid_size - 1 - int(properties[i][0]), grid_size - 1 - int(properties[i][1]))):
                    adjacent.append((i + (j + 1) * grid_size + (j + 1), arrow_colour, j + 1))
            elif arrow == 's':
                for j in range(grid_size - 1 - int(properties[i][1])):
                    adjacent.append((i + (j + 1) * grid_size, arrow_colour, j + 1))
            elif arrow == 'sw':
                for j in range(min(grid_size - 1 - int(properties[i][1]), int(properties[i][0]))):
                    adjacent.append((i + (j + 1) * grid_size - (j + 1), arrow_colour, j + 1))
            elif arrow == 'w':
                for j in range(int(properties[i][0])):
                    adjacent.append((i - (j + 1), arrow_colour, j + 1))
            elif arrow == 'nw':
                for j in range(min(int(properties[i][1]), int(properties[i][0]))):
                    adjacent.append((i - (j + 1) * grid_size - (j + 1), arrow_colour, j + 1))
    adjacency[i] = adjacent  # insert list into dictionary


def add_new_step_size_colour(lst):
    for _ in range(grid_size ** 2):
        lst.append('white')
    return lst


vertices_colour_by_step_size = []
add_new_step_size_colour(vertices_colour_by_step_size)


def dfs(colours, adj_dict, vertex, step_size, max_step_size, total, path):
    # colours is a list of the colours of all vertices for various step sizes
    # adj_dict is the adjacency dictionary
    # vertex is the vertex that dfs is called on (int)
    # step_size is the distance that can be travelled in the Alice Maze
    # total is the total number of steps taken

    best_path, best_total = [], 999999  # init values for best_path, best_total
    colours[(step_size - 1) * (grid_size ** 2) + vertex] = 'grey'  # set current square to grey
    total += 1  # add 1 to the total distance travelled
    path.append(vertex)  # add the current node to the path taken

    if adj_dict[vertex]:  # if there are adjacent vertices
        if adj_dict[vertex][0][1] == 'r':  # if arrows are red, increase d by 1
            step_size += 1
            if step_size > max_step_size:
                add_new_step_size_colour(colours)
                max_step_size = step_size
        if adj_dict[vertex][0][1] == 'y':  # if arrows are yellow, decrease d by 1
            step_size += -1

    if vertex == goal_vertex:  # base case of recursion
        return path, total
    else:  # recursive step
        for edge in adj_dict[vertex]:
            if edge[2] == step_size and colours[(step_size - 1) * (grid_size ** 2) + edge[0]] == 'white':  # if the arrow distance is equal to the step_size, and the square has not been accessed before at the current step_size:
                colours_copy = colours.copy()  # give each recursive call its own copy of colours so that vertices that will turn grey do not effect other recursive calls
                path_copy = path.copy()  # same as aforementioned claim
                solution = (dfs(colours_copy, adj_dict, edge[0], step_size, max_step_size, total, path_copy))
                if solution[1] < best_total:  # comparing the current best solution with the recursive solution
                    best_path, best_total = solution

    return best_path, best_total  # return the best solution


maze_solution = dfs(vertices_colour_by_step_size, adjacency, starting_vertex, 1, 1, -1, [])
if maze_solution[1] == 999999:  # if no solution was found
    print('No solution')
else:
    print(maze_solution)
