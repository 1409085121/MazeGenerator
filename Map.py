from random import shuffle, uniform
from Node import *
from Connection import Connection


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.nodeList = []
        self.connectionList = []

        self.nodeList = []
        self.connectionList = []
        for y in range(self.height):
            for x in range(self.width):
                self.nodeList.append(Node(x, y))

    def get_node(self, x, y):
        return self.nodeList[x + y * self.width]

    def new_connection(self, node1, node2):
        if not abs(node1.x - node2.x) + abs(node1.y - node2.y) == 1:
            print(abs(node1.x - node2.x) + abs(node1.y - node2.y))
            raise ValueError("Nodes do not intersect")

        connection = Connection(self)
        connection.bind(node1, node2)
        self.connectionList.append(connection)
        node1.bind(connection, node2)
        node2.bind(connection, node1)

    def new_invisible_connection(self, node1, node2):
        connection = Connection(self, False)
        connection.bind(node1, node2)
        self.connectionList.append(connection)
        node1.bind(connection, node2)
        node2.bind(connection, node1)

    def get_nodes(self, node: Node):
        """
        Gets the nodes that are adjacent and do not have a connection to them, takes one at random and returns
        Used to obtain the nodes required for the next step of the walk()
        """
        CandidateNodeList = []
        if not node.connections[0] and node.y > 1:
            node1 = self.get_node(node.x, node.y-1)
            if not node1.visited:
                CandidateNodeList.append(node1)
        if not node.connections[2] and node.y < self.height-2:
            node1 = self.get_node(node.x, node.y+1)
            if not node1.visited:
                CandidateNodeList.append(node1)
        if not node.connections[1] and node.x < self.width-2:
            node1 = self.get_node(node.x+1, node.y)
            if not node1.visited:
                CandidateNodeList.append(node1)
        if not node.connections[3] and node.x > 1:
            node1 = self.get_node(node.x-1, node.y)
            if not node1.visited:
                CandidateNodeList.append(node1)
        return CandidateNodeList

    def generate_maze(self, root_node_probability=0.05, initialize=True):
        # Initialize the map and get ready for the next build
        if initialize:
            self.nodeList = []
            self.connectionList = []
            for y in range(self.height):
                for x in range(self.width):
                    self.nodeList.append(Node(x, y))
        self.generate_border()

        for x in range(self.width):
            for y in range(self.height):
                print(self.get_node(x, y).connections_count, end=" ")
            print()

        # Start with a linear walk from the edge,
        # dividing the map into several areas
        step_limit = self.width+self.height
        self.linear_walk(self.get_node(int(self.width*uniform(0.1, 0.9)), 0), step_limit)
        self.linear_walk(self.get_node(int(self.width*uniform(0.1, 0.9)), self.height-1), step_limit)
        self.linear_walk(self.get_node(0, int(self.height*uniform(0.1, 0.9))), step_limit)
        self.linear_walk(self.get_node(self.width-1, int(self.height*uniform(0.1, 0.9))), step_limit)
        for x in range(self.width):
            if uniform(0, 1) < root_node_probability:
                self.linear_walk(self.get_node(x, 0), step_limit)
            if uniform(0, 1) < root_node_probability:
                self.linear_walk(self.get_node(x, self.height-1), step_limit)
        for y in range(self.height):
            if uniform(0, 1) < root_node_probability:
                self.linear_walk(self.get_node(0, y), step_limit)
            if uniform(0, 1) < root_node_probability:
                self.linear_walk(self.get_node(self.width-1, y), step_limit)

        # Generate branches on the backbone basis
        # Randomly iterate through the nodes and find the node that can generate branches
        node_list = self.nodeList.copy()
        shuffle(node_list)
        for node in node_list:
            if node.visited:
                self.recursion_walk(node, branchCD_limit=0)
        for x in range(1, self.width-1):
            node1 = self.get_node(x, 0)
            node2 = self.get_node(x, self.height-1)
            self.recursion_walk(node1, branchCD_limit=0)
            self.recursion_walk(node2, branchCD_limit=0)
        for y in range(1, self.height-1):
            node1 = self.get_node(0, y)
            node2 = self.get_node(self.width-1, y)
            self.recursion_walk(node1, branchCD_limit=0)
            self.recursion_walk(node2, branchCD_limit=0)

    def linear_walk(self, node: Node, step_limit=-1):
        """
        Generate linear connections
        Set the number of steps to a negative number so that the connection can be extended infinitely
        node: the node where walking started
        step_limit: Maximum step limit
        """
        node.visited = True
        while True:
            CandidateNodeList = self.get_nodes(node)
            shuffle(CandidateNodeList)

            if step_limit == 0:
                break
            elif len(CandidateNodeList) == 0:
                break

            node2 = CandidateNodeList[0]
            self.new_connection(node, node2)
            node2.visited = True
            step_limit -= 1
            node = node2

    def recursion_walk(self, node: Node, branchCD_limit=5, branching_probability=1):
        """
        Generate tree-like connections, recursively
        node: the node where walking started
        branchCD_limit: After one branch is generated, the number of nodes that need to pass before the next branch can be generated.
        """
        node.visited = True
        branchCD = branchCD_limit
        while True:
            CandidateNodeList = self.get_nodes(node)
            shuffle(CandidateNodeList)

            if len(CandidateNodeList) == 0:
                break
            elif len(CandidateNodeList) > 1 and branchCD <= 0:
                if uniform(0, 1) < branching_probability:
                    branchCD = branchCD_limit
                    node3 = CandidateNodeList[1]
                    node3.visited = True
                    self.new_connection(node, node3)
                    self.recursion_walk(node3, branchCD_limit, branching_probability)

            node2 = CandidateNodeList[0]
            if node2.visited:
                break
            self.new_connection(node, node2)
            node2.visited = True
            branchCD -= 1
            node = node2

    def generate_border(self):
        for i in range(self.height - 1):
            node1 = self.get_node(0, i)
            node2 = self.get_node(0, i + 1)
            self.new_connection(node1, node2)

        for i in range(self.height - 1):
            node1 = self.get_node(self.width - 1, i)
            node2 = self.get_node(self.width - 1, i + 1)
            self.new_connection(node1, node2)

        for i in range(1, self.width - 1):
            node1 = self.get_node(i, 0)
            node2 = self.get_node(i + 1, 0)
            self.new_connection(node1, node2)

        for i in range(self.width - 2):
            node1 = self.get_node(i, self.height - 1)
            node2 = self.get_node(i + 1, self.height - 1)
            self.new_connection(node1, node2)

        return self
