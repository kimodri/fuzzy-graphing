import math

class TrapMF:
    def __init__(self, a, b, c, d, name=None):
        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.points = [self.a, self.b, self.c, self.d]
   
    def __str__(self):
        if self.name:
            return f"TrapMF(name={self.name}, a={self.a}, b={self.b}, c={self.c}, d={self.d})"
        return f"TrapMF(a={self.a}, b={self.b}, c={self.c}, d={self.d})"
    
if __name__ == "__main__":
    trap_mf = TrapMF((0, 1), (50, 1), (70, 0), (100, 0), name="Warm")
    print(trap_mf)
