from priority_queue import PriorityQueue


class Uncolorable(RuntimeError):
    def __init__(self, data, *args):
        super(Uncolorable, self).__init__("Node %s could not be colored." % data, *args)
        self.data = data


class Graph:
    """A class that provides an adjacency list representation of a graph

    nodes: Dictionary mapping data to it's node
    """

    def __init__(self):
        self.nodes = {}

    def insert(self, data, color_first=False):
        if data not in self.nodes:
            self.nodes[data] = Node(data)
        if color_first:
            self.nodes[data].priority = 1

    def remove(self, data):
        if data in self.nodes:
            for node in self.nodes.values():
                try:
                    node.neighbors.remove(data)
                except KeyError:
                    pass
            del self.nodes[data]

    def insert_colored(self, data, color):
        if data not in self.nodes:
            self.nodes[data] = Node(data)
        self.nodes[data].clearable = False
        self.nodes[data].color = color

    def add_edge(self, data1, data2):
        """Creates a undirected edge between nodes associated with each element in datas
        """

        # remove duplicates (so we don't have loops, rendering the graph uncolorable)
        if data1 == data2:
            return

        self.insert(data1)
        self.insert(data2)
        self.nodes[data1].neighbors.add(self.nodes[data2])
        self.nodes[data2].neighbors.add(self.nodes[data1])

    def color(self, colors, generate_color=None):
        # type: (list) -> ()

        def saturation(node):
            # type: (Node) -> int
            for neighbor in node.neighbors:
                node.neighbor_colors.add(neighbor.color)
            return len(node.neighbor_colors)

        def priority(node):
            # TODO: Figure out why on earth negating saturation takes longer
            return node.priority, saturation(node)

        w = PriorityQueue(priority)
        for node in self.nodes.values():
            node.neighbor_colors = set()
            if node.color is None:
                w.insert(node)
        while w:
            u = w.pop()
            try:
                u.color = next(c for c in colors if c not in u.neighbor_colors)
                for neighbor in u.neighbors:
                    if neighbor.color is None:
                        neighbor.neighbor_colors.add(u.color)
                        # TODO: Figure out why on earth negating saturation takes longer
                        w.insert(neighbor, (neighbor.priority, len(neighbor.neighbor_colors)))
            except StopIteration:
                # Happens if all colors are taken
                if generate_color is not None:
                    colors.append(generate_color())
                    w.insert(u)
                    continue
                else:
                    raise Uncolorable(u.data)

    def color_of(self, data):
        return self.nodes[data].color

    def __str__(self):
        strings = []
        for node in self.nodes.values():
            strings.append(str(node) + " -> {" + str(", ").join(
                map(str, node.neighbors)) + "}")
        return "\n".join(strings)


class Node:
    def __init__(self, data):
        self.data = data
        self.color = None
        self.neighbors = set()
        self.clearable = True
        self.priority = 2

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return "(d=%s, c=%s)" % (self.data, self.color)

    def __repr__(self):
        return str(self)

    # Needed for `node in nodes` notation
    def __hash__(self):
        # Since the hash is the same as the data,
        return hash(self.data)
