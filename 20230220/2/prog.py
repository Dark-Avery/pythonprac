from cowsay import cowsay, list_cows


class Monster:
    def __init__(self, name, greeting):
        self.name = name
        self.greeting = greeting


class Player:
    def __init__(self, position):
        self.position = position


class Dungeon:
    def __init__(self, size):
        self.size = size
        self.field = [[None] * size[0] for _ in range(size[1])]

    def NewPos(self, player, x, y):
        return ((player.position[0] + x) % self.size[0],
                (player.position[1] + y) % self.size[1])

    def encounter(self, player):
        if isinstance(self.field[player.position[0]][player.position[1]], Monster):
            print(cowsay(self.field[player.position[0]][player.position[1]].greeting,
                  cow=self.field[player.position[0]][player.position[1]].name))

    def MoveMessage(self, player):
        print(f'Moved to {player.position}')

    def MoveLeft(self, player):
        player.position = self.NewPos(player, -1, 0)
        self.MoveMessage(player)
        self.encounter(player)

    def MoveRight(self, player):
        player.position = self.NewPos(player, 1, 0)
        self.MoveMessage(player)
        self.encounter(player)

    def MoveUp(self, player):
        player.position = self.NewPos(player, 0, 1)
        self.MoveMessage(player)
        self.encounter(player)

    def MoveDown(self, player):
        player.position = self.NewPos(player, 0, -1)
        self.MoveMessage(player)
        self.encounter(player)

    def play(self):
        player = Player((0, 0))
        while True:
            s = input()
            match s.split():
                case ['left']:
                    self.MoveLeft(player)
                case ['right']:
                    self.MoveRight(player)
                case ['up']:
                    self.MoveUp(player)
                case ['down']:
                    self.MoveDown(player)
                case ['addmon', name, x, y, greeting]:
                    x = int(x)
                    y = int(y)
                    if x >= self.size[0] or x < 0 or y >= self.size[1] or y < 0:
                        print("Invalid arguments")
                    elif name not in list_cows():
                        print("Cannot add unknown monster")
                    else:
                        match self.field[x][y]:
                            case Monster():
                                self.field[x][y] = Monster(name, greeting)
                                print(
                                    f"Added monster {name} to ({x}, {y}) saying {greeting}")
                                print("Replaced the old monster")
                            case _:
                                self.field[x][y] = Monster(name, greeting)
                                print(
                                    f"Added monster {name} to ({x}, {y}) saying {greeting}")
                case _:
                    print("Invalid command")


dungeon = Dungeon((10, 10))
dungeon.play()
