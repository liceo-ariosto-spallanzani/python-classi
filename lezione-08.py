import os
from random import choice

DIRECTIONS = "up", "down", "left", "right"

def clear_screen():
  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")
class Entity: 
  def __init__(self, x, y, field, graphic):
    self.x = x
    self.y = y
    self.graphic = graphic
    if field != None:
      self.add_to_field(field)

  def add_to_field(self, field):
    self.field = field
    self.field.entities.append(self)

  def move(self, direction):
    futureX = self.x
    futureY = self.y

    if direction == "up" and self.y > 0:
      futureY -= 1
    elif direction == "down" and self.y < self.field.h - 1:
      futureY += 1
    elif direction == "left" and self.x > 0:
      futureX -= 1
    elif direction == "right" and self.x < self.field.w - 1:
      futureX += 1

    if self.x == futureX and self.y == futureY:
      return

    e = self.field.get_entity_at_coords(futureX, futureY)

    if e == None:
      self.x = futureX
      self.y = futureY
    else:
      self.collide(e)

  def collide(self, entity):
    pass

  def update(self):
    pass

class Gold(Entity):
  def __init__(self, x, y, field):
    super().__init__(x, y, field, "$")
    self.value = 100

class Wall(Entity):
  def __init__(self, x, y, field):
    super().__init__(x, y, field, "#")

class Living_Entity(Entity):
  def __init__(self, x, y, name, hp, damage, field, graphic):
    super().__init__(x, y, field, graphic)
    self.name = name
    self.hp = hp
    self.max_hp = hp
    self.damage = damage

  def info(self):
    print("sono", self.name, "hp:", self.hp, "/", self.max_hp, "e mi trovo a", self.x, ",", self.y)

  def attack(self, enemy):
    if self.hp <= 0:
      print(self.name, "prova ad attaccare da morto con scarsi risultati")
    else: 
      print(self.name, "attacca", enemy.name)

      if (enemy.hp <= 0):
        print(enemy.name, "e' morto")
        self.field.entities.remove(enemy)
      else:
        enemy.hp -= self.damage

class Monster(Living_Entity):
  def __init__(self, x, y, name, field):
    super().__init__(x, y, name, 10, 5, field, "m")
    
  def collide(self, entity):
    if isinstance(entity, Player):
      self.attack(entity)
  
  def move(self):
    super().move(choice(DIRECTIONS))

  def update(self):
    super().update()
    self.move()

class Player(Living_Entity):
  def __init__(self, x, y, name, field):
    super().__init__(x, y, name, 20, 5, field, "p")
  
  def collide(self, entity):
    if isinstance(entity, Monster):
      self.attack(entity)
    elif isinstance(entity, Gold):
      self.field.score += entity.value
      self.field.entities.remove(entity)

class Field:
  def __init__(self, level_number, player):
    self.entities = []
    self.score = 0
    self.level_number = level_number
    self.player = player

  def has_gold(self):
    for e in self.entities:
      if isinstance(e, Gold):
        return True
    
    return False

  def load_level(self):
    f = open("./level" + str(self.level_number) + ".level", "r")
    rows = f.read().split("\n")
    f.close()

    self.h = len(rows)
    self.w = len(rows[0])

    for y in range(self.h):
      row = rows[y]
      for x in range(self.w):
        char = row[x]
        if char == "p":
          self.player.x = x
          self.player.y = y
          self.player.add_to_field(self)
        elif char == "#":
          Wall(x, y, self)
        elif char == "$":
          Gold(x, y, self)
        elif char == "m":
          Monster(x, y, "Monster", self)

  def get_entity_at_coords(self, x, y):
    for e in self.entities:
      if e.x == x and e.y == y:
        return e

    return None
    
  def draw(self):
    print("score:", self.score)
    for y in range(self.h):
      for x in range(self.w):
        for e in self.entities:
          if x == e.x and y == e.y:
            print("[" + e.graphic + "]", end = "")
            break    
        else:
          print("[ ]", end = "")
      print()
  
  def update(self):
    for e in self.entities:
      e.update()

class Game:
  def __init__(self, levels):
    # self.score = 0
    self.player = Player(0, 0, "Player", None)
    self.fields = []
    self.levels = levels
    for i in range(1, levels + 1):
      self.fields.append(Field(i, self.player))
    
    self.current_field = None
    self.current_level_index = -1
    self.status = "STOPPED"

  def next_level(self):
    self.status = "RUNNING"
    if self.current_level_index < self.levels - 1:
      self.current_level_index += 1
      self.current_field = self.fields[self.current_level_index]
      self.current_field.load_level()
    else:
      self.win()

  def win(self):
    clear_screen()
    self.status = "STOPPED"
    print("THE WINNER IS YOU!")

  def game_over(self):
    clear_screen()
    self.status = "STOPPED"
    print("GAME OVER!")

  def update(self):
    if self.status == "RUNNING":
      self.current_field.update()
      if self.player.hp <= 0:
        self.game_over()

      if self.current_field.has_gold() == False:
        self.next_level()
  
  def draw(self):
    if self.status == "RUNNING":
      self.current_field.draw()

game = Game(4)
game.next_level()

clear_screen()
while True:  
  game.update()
  game.draw()

  command = input("input: ").lower()
  clear_screen()

  if command == "q": break
  elif command == "w": game.player.move("up")
  elif command == "a": game.player.move("left")
  elif command == "s": game.player.move("down")
  elif command == "d": game.player.move("right")
  elif command == "z": game.next_level()