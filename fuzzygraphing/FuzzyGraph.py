class FuzzyGraph:
    def __init__(self, name, graphs=None):
        self.name = name
        self.graphs = graphs if graphs is not None else []

    def register_graph(self, graph):
        self.graphs.append(graph)

    def __str__(self):
        graph_strs = "\n  ".join(str(graph) for graph in self.graphs)
        return f"FuzzyGraph(name={self.name}, graphs=[\n  {graph_strs}\n])"




        