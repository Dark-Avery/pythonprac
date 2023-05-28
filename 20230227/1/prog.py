from cowsay import cowsay, list_cows, read_dot_cow
import shlex


class Monster:
    def __init__(self, name, greeting, hp):
        self.hp = hp
        self.name = name
        self.greeting = greeting


class Player:
    def __init__(self, position):
        self.position = position


class Dungeon:
    add_list_cows = {"jgsbat"}

    def __init__(self, size):
        self.size = size
        self.field = [[None] * size[0] for _ in range(size[1])]

    def NewPos(self, player, x, y):
        return ((player.position[0] + x) % self.size[0],
                (player.position[1] + y) % self.size[1])

    def display_monster(self, monster):
        image = None
        if monster.name in list_cows():
            image = cowsay(monster.greeting, cow=monster.name)
        if monster.name in Dungeon.add_list_cows:
            filename = f"{monster.name}.cow"
            with open(filename, "r") as cowfile:
                image = cowsay(monster.greeting, cowfile=read_dot_cow(cowfile))
        print(image)

    def encounter(self, player):
        if isinstance(self.field[player.position[0]][player.position[1]], Monster):
            self.display_monster(self.field[player.position[0]][player.position[1]])

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

    def ParseArgs(self, args: list[str]):
        if len(args) != 8 or "hello" not in args or "hp" not in args or "coords" not in args:
            raise SyntaxError
        monster_name = args[0]
        keywords = args[1:]
        while keywords:
            match keywords:
                case ["hello", greeting, *_]:
                    monster_greeting = greeting
                    keywords = keywords[2:]
                case ["hp", hp, *_]:
                    if not hp.isdigit():
                        raise ValueError
                    monster_hp = int(hp)
                    keywords = keywords[2:]
                case ["coords", x, y, *_]:
                    if not x.isdigit() or not y.isdigit():
                        raise ValueError
                    monster_x = int(x)
                    monster_y = int(y)
                    keywords = keywords[3:]
                case _:
                    raise SyntaxError
        return monster_name, monster_greeting, monster_hp, monster_x, monster_y

    def play(self):
        player = Player((0, 0))
        while s := input():
            match shlex.split(s):
                case ['left']:
                    self.MoveLeft(player)
                case ['right']:
                    self.MoveRight(player)
                case ['up']:
                    self.MoveUp(player)
                case ['down']:
                    self.MoveDown(player)
                case ['addmon', *args]:
                    try:
                        name, greeting, hp, x, y = self.ParseArgs(args)
                        if x >= self.size[0] or x < 0 or y >= self.size[1] or y < 0:
                            raise SyntaxError
                        elif name not in list_cows() and name not in self.add_list_cows:
                            raise NameError
                        else:
                            match self.field[x][y]:
                                case Monster():
                                    self.field[x][y] = Monster(name, greeting, hp)
                                    print(
                                        f"Added monster {name} to ({x}, {y}) saying {greeting}")
                                    print("Replaced the old monster")
                                case _:
                                    self.field[x][y] = Monster(name, greeting, hp)
                                    print(
                                        f"Added monster {name} to ({x}, {y}) saying {greeting}")
                    except SyntaxError:
                        print("Invalid arguments")
                    except NameError:
                        print("Cannot add unknown monster")
                    except ValueError:
                        print("HP and coords should be a digit")
                case _:
                    print("Invalid command")


def main():
    print("<<< Welcome to Python-MUD 0.1 >>>")
    dungeon = Dungeon((10, 10))
    dungeon.play()


if __name__ == '__main__':
    main()
