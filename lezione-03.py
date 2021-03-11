class Entity: 
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def move(self, direction):
    if direction == "up":
      self.y -= 1
    elif direction == "down":
      self.y += 1
    elif direction == "left":
      self.x -= 1
    elif direction == "right":
      self.x += 1

class Monster(Entity):
  def __init__(self, x, y, name, damage):
    super().__init__(x, y)
    self.name = name
    self.hp = 10
    self.damage = damage

  def info(self):
    print("sono", self.name, "hp:", self.hp, "/10", "e mi trovo a", self.x, ",", self.y)

  def attack(self, enemy):
    if self.hp <= 0:
      print(self.name, "prova ad attaccare da morto con scarsi risultati")
    else: 
      print(self.name, "attacca", enemy.name)

      if (enemy.hp <= 0):
        print(enemy.name, "e' morto")
      else:
        enemy.hp -= self.damage

class Field:
  def __init__(self):
    self.w = 5
    self.h = 5
    self.entities = []

  def draw(self):
    for y in range(self.h):
      for x in range(self.w):
        for e in self.entities:
          if x == e.x and y == e.y:
            print("[x]", end = "")
            break    
        else:
          print("[ ]", end = "")
      print()

field = Field()
m = Monster(2, 2, "Pino", 10)
field.entities.append(m)
field.entities.append( Monster(3, 3, "Pino", 10))

field.draw()
m.move("up")
print()
field.draw()