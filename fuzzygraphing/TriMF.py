class TriMF():
    def __init__(self, a, b, c, name=None):
        self.name = name
        self.a = a
        self.b = b
        self.c = c

    def _membership(self, x):
        if x <= self.a:
            return 0.0
        elif x >= self.a and x <= self.b:
            return (x - self.a) / (self.b - self.a)
        elif x >= self.b and x <= self.c:
            return (self.c - x) / (self.c - self.b)
        else:
            return 0.0
        
    def __str__(self):
        if self.name:
            return f"TriMF(name={self.name}, a={self.a}, b={self.b}, c={self.c})"
        return f"TriMF(a={self.a}, b={self.b}, c={self.c})"
    
if __name__ == "__main__":
    tri_mf = TriMF(30, 50, 70, name="Cool")
    print(tri_mf)
    print(tri_mf._membership(65))