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
            self.nodes[data].priority = 2

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

    def add_edge(self, *datas):
        """Creates a undirected edge between nodes associated with each element in datas
        """

        # remove duplicates (so we don't have loops, rendering the graph uncolorable)
        datas = set(datas)

        for missing_data in datas - set(self.nodes):
            self.insert(missing_data)
        else:
            # Add each node associated with each data element given to each others
            # set of neighbors
            for data in datas:
                self.nodes[data].neighbors |= set(map(lambda d: self.nodes[d], datas - {data}))

    def remove_colors(self):
        for node in self.nodes.values():
            if node.clearable:
                node.color = None

    def color(self, colors):
        # type: (list) -> ()

        def saturation(node):
            # type: (Node) -> int
            seen_colors = set()
            sat = 0
            for neighbor in node.neighbors:
                if neighbor.color not in seen_colors:
                    sat += 1
                    seen_colors.add(neighbor.color)
            return sat

        def priority(node):
            return node.priority, saturation(node)

        w = set(node for node in self.nodes.values() if node.color is None)
        while w:
            u = max(w, key=priority)
            adj_colors = map(lambda n: n.color, u.neighbors)
            try:
                u.color = next(c for c in colors if c not in adj_colors)
            except StopIteration:
                # Happens if all colors are taken
                raise Uncolorable(u.data)
            w -= {u}

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
        self.priority = 1

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return "(d=%s, c=%s)" % (self.data, self.color)

    # Needed for `node in nodes` notation
    def __hash__(self):
        # Since the hash is the same as the data,
        return hash(self.data)
