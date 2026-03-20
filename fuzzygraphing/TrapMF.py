import math

class TrapMF:
    def __init__(self, a, b, c, d, name=None):
        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.is_not_full = True if self.a == self.b or self.d == math.inf else False

    def _membership(self, x):
        if x < self.a:
            return 0.0
        elif self.a == self.b:
            if x <= self.c:
                return 1.0
            elif self.d == float('inf') or x <= self.d:
                return (self.d - x) / (self.d - self.c) if self.d != float('inf') else 1.0
            else:
                return 0.0
        elif x <= self.b:
            return (x - self.a) / (self.b - self.a)
        elif x <= self.c:
            return 1.0
        elif self.d == float('inf'):
            return 1.0
        elif x <= self.d:
            return (self.d - x) / (self.d - self.c)
        else:
            return 0.0

    def __str__(self):
        if self.name:
            return f"TrapMF(name={self.name}, a={self.a}, b={self.b}, c={self.c}, d={self.d})"
        return f"TrapMF(a={self.a}, b={self.b}, c={self.c}, d={self.d})"
    

