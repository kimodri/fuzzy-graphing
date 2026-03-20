if x < self.a:                          # ← Same as formula: x ≤ a → 0
    return 0.0                          #   (changed to strict < so x=a falls
                                        #    into the next branch correctly)

elif self.a == self.b:                  # ← SPECIAL CASE: left-shoulder (a==b)
    if x <= self.c:                     #   Skip the rising edge entirely,
        return 1.0                      #   plateau starts immediately at a
    elif self.d == float('inf') ...     #   Also handles inf on the falling side
        return 1.0                      #   (plateau extends forever)
    ...                                 #   Otherwise normal falling edge

elif x <= self.b:                       # ← Formula: (x−a)/(b−a)
    return (x - self.a) / (self.b - self.a)

elif x <= self.c:                       # ← Formula: 1
    return 1.0

elif self.d == float('inf'):            # ← SPECIAL CASE: right-shoulder (d=inf)
    return 1.0                          #   Plateau never falls off

elif x <= self.d:                       # ← Formula: (d−x)/(d−c)
    return (self.d - x) / (self.d - self.c)

else:                                   # ← Formula: d ≤ x → 0
    return 0.0
