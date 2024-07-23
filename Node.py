from Connection import Connection
from random import choice


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.connections = [False, False, False, False]
        self.connections_count = 0
        self.connectionList = []

    def bind(self, connection: Connection, otherNode):
        self.connectionList.append(connection)
        self.connections_count += 1
        if otherNode.y < self.y:
            self.connections[0] = True
        elif otherNode.x < self.x:
            self.connections[3] = True
        elif otherNode.y > self.y:
            self.connections[2] = True
        elif otherNode.x > self.x:
            self.connections[1] = True
        return self

    def get_spare_node(self, map):
        """
        Gets the nodes that are adjacent and do not have a connection to them, takes one at random and returns
        Used to obtain the nodes required for the next step of the walk()
        """
        CandidateNodeList = []
        if not self.connections[0] and self.y > 1:
            CandidateNodeList.append(map.get_node(self.x, self.y-1))
        if not self.connections[3] and self.x > 1:
            CandidateNodeList.append(map.get_node(self.x-1, self.y))
        if not self.connections[2] and self.y < map.height-2:
            CandidateNodeList.append(map.get_node(self.x, self.y+1))
        if not self.connections[1] and self.x < map.width-2:
            CandidateNodeList.append(map.get_node(self.x+1, self.y))

        if len(CandidateNodeList) == 0:
            print(self.connections_count, self.connections)
            return None
        return choice(CandidateNodeList)
