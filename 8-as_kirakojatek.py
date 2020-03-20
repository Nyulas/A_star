from queue import PriorityQueue
import numpy as np
from copy import copy, deepcopy


class State(object):

    def __init__(self, value, parent, start=0, goal=0, value_dict={}):

        self.children = []
        self.parent = parent
        self.value = copy(value)
        self.dist = 0

        if parent:
            self.start = parent.start
            self.goal = parent.goal
            self.path = parent.path[:]
            self.path.append(value)
            self.value_dict = value_dict
        else:
            self.path = [value]
            self.start = start
            self.goal = goal
            self.value_dict = value_dict

    def GetDistance(self):
        pass

    def CreateChildren(self):
        pass

class State_game(State):

    def __init__(self, value, parent, start=0, goal=0, value_array={}):

        super(State_game, self).__init__(value, parent, start, goal, value_array)
        self.dist = self.GetDistance()

    def GetDistance(self):

        if np.array_equal(self.value, self.goal):
            return 0
        dist = 0

        for i in range(3):
            for j in range(3):
                position = np.where(self.goal == self.value[i][j])

                # this is how we get the distance between current element
                # and the element where the current element is expected
                # Manhattan Heuristic
                distance_between = abs(i-position[0][0]) + abs(j-position[1][0])

                self.value_dict[self.value[i][j]] = [distance_between, 0]

                dist += distance_between

        return dist

        return "key doesn't exist"

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.value == other.value

    def CreateChildren(self):
        if not self.children:
            for generator in range(2):
                val = copy(self.value)
                for i in range(3):
                    for j in range(3):
                        if val[i][j] == 0:
                            if i+1>= 3:
                                dict = {
                                    '[i-1][j]': self.value_dict.get(val[i - 1][j]),
                                    '[i][j-1]': self.value_dict.get(val[i][j - 1]),
                                    '[i][j+1]': self.value_dict.get(val[i][j + 1]),
                                }
                            elif j+1>=3:
                                dict = {
                                    '[i-1][j]': self.value_dict.get(val[i - 1][j]),
                                    '[i][j-1]': self.value_dict.get(val[i][j - 1]),
                                    '[i+1][j]': self.value_dict.get(val[i + 1][j])
                                }
                            elif i-1<0:
                                    dict = {
                                        '[i][j-1]': self.value_dict.get(val[i][j - 1]),
                                        '[i][j+1]': self.value_dict.get(val[i][j + 1]),
                                        '[i+1][j]': self.value_dict.get(val[i + 1][j])
                                    }
                            elif j-1<0:
                                dict = {
                                    '[i-1][j]': self.value_dict.get(val[i - 1][j]),
                                    '[i][j+1]': self.value_dict.get(val[i][j + 1]),
                                    '[i+1][j]': self.value_dict.get(val[i + 1][j])
                                }
                            else:
                                dict = {
                                    '[i-1][j]': self.value_dict.get(val[i-1][j]),
                                    '[i][j-1]': self.value_dict.get(val[i][j-1]),
                                    '[i][j+1]': self.value_dict.get(val[i][j+1]),
                                    '[i+1][j]': self.value_dict.get(val[i+1][j])
                                }

                            lista=[]

                            for key, value in dict.items():
                                lista.append(value)

                            print(lista)
                            min_usage = min(value[1] for value in lista)
                            ertek = min(value for value in lista) #if value[0] > 0 and value[1] == min_usage)

                            print(ertek)

                            for key, value in self.value_dict.items():
                                if ertek == value:
                                    for k in range(3):
                                        for l in range(3):
                                            if val[i][j] == 0 and val[k][l] == key:
                                                seged = val[i][j]
                                                val[i][j] = val[k][l]
                                                val[k][l] = seged
                                                helper = ertek[1]
                                                helper += 1
                                                self.value_dict[val[i][j]] = [ertek[0], helper]

                                                print(val)
                                                child = State_game(val, self)
                                                self.children.append(child)



class AStar_Solver:
    def __init__(self, start, goal):
        self.path = []
        self.visitedQueue = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal
        self.value_dict = {}

    def Solve(self):

        startState = State_game(self.start, 0, self.start, self.goal, self.value_dict)

        count = 0
        self.priorityQueue.put((0, count, startState))
        while(not self.path and self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[2]
            closestChild.CreateChildren()
            self.visitedQueue.append(closestChild.value)

            for child in closestChild.children:
                if any(child.value.__eq__ for object in self.visitedQueue):
                    count += 1
                    if not child.dist:
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist, count, child))

        if not self.path:
            print("Goal of %s is not possible!" % (self.goal))

        return self.path


if __name__ == "__main__":
    start1 = np.array([[1, 4, 3], [7, 0, 6], [5, 8, 2]])
    goal1  = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    print("Starting...")

    a = AStar_Solver(start1, goal1)
    a.Solve()

    for i in range(len(a.path)):
        print("{0}) {1}".format(i, a.path[i]))