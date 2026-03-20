class FuzzyGraph:
    def __init__(self, name, graphs=None):
        self.name = name
        self.graphs = graphs if graphs is not None else []

    def register_graph(self, graph):
        self.graphs.append(graph)

    def calculate_membership(self, x):
        results = {}
        for graph in self.graphs:
            results[graph.name] = graph._membership(x)
        return results
    
    def print_membership(self, x):
        result = self.calculate_membership(x)
        print(f"Membership results for {x} in {self.name}:")
        for name, membership in result.items():
            print(f"{membership * 100:.2f}% of {name}")

    
if __name__ == "__main__":
    from TrapMF import TrapMF
    from TriMF import TriMF
    import math

    fuzzy_graph = FuzzyGraph("Temperature Fuzzy Graph")

    trap_mf_freezing = TrapMF(0, 0, 30, 50, name="Freezing")
    tri_mf_cool = TriMF(30, 50, 70, name="Cool")
    tri_mf_warm = TriMF(50, 70, 90, name="Warm")
    trap_mf_Hot = TrapMF(70, 90, 120, math.inf, name="Hot")

    fuzzy_graph.register_graph(trap_mf_freezing)
    fuzzy_graph.register_graph(tri_mf_cool)
    fuzzy_graph.register_graph(tri_mf_warm)
    fuzzy_graph.register_graph(trap_mf_Hot)

    print(fuzzy_graph.calculate_membership(65))
    fuzzy_graph.print_membership(65)


        