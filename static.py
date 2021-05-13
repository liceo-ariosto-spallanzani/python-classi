class Monster:
  def __init__(self, name):
    self.name = name

  def say_hello(self, target):
    print("Hi", target, "I'm", self.name)

m = Monster("Pippo")
m.say_hello("Pluto")

Monster.say_hello(m, "Pippo")

class Formulas:
  pi = 3.14

  def rect_area(b, h):
    return b * h