from cowsay import cowsay, list_cows, read_dot_cow
import shlex
import cmd


class Monster:
    def __init__(self, name, greeting, hp):
        self.hp = hp
        self.name = name
        self.greeting = greeting


class Player:
    def __init__(self, position):
        self.position = position


class Dungeon(cmd.Cmd):
    MONSTER_EXT = set(list_cows())
    add_list_cows = {"jgsbat"}
    MONSTERS = MONSTER_EXT | add_list_cows
    player = Player((0, 0))
    WEAPONS = {"sword": 10, "spear": 15, "axe": 20}

    def __init__(self, size, *args, **kwarks):
        self.size = size
        self.field = [[None] * size[0] for _ in range(size[1])]
        super().__init__(*args, **kwarks)

    def NewPos(self, player, x, y):
        return ((player.position[0] + x) % self.size[0],
                (player.position[1] + y) % self.size[1])

    def do_exit(self, args):
        return True

    def display_monster(self, monster):
        image = None
        if monster.name in self.MONSTER_EXT:
            image = cowsay(monster.greeting, cow=monster.name)
        if monster.name in self.add_list_cows:
            filename = f"{monster.name}.cow"
            with open(filename, "r") as cowfile:
                image = cowsay(monster.greeting, cowfile=read_dot_cow(cowfile))
        print(image)

    def isMonster(self):
        coords = self.player.position
        return isinstance(self.field[coords[0]][coords[1]], Monster)

    def encounter(self):
        if self.isMonster():
            coords = self.player.position
            self.display_monster(self.field[coords[0]][coords[1]])

    def MoveMessage(self, player):
        print(f'Moved to {player.position}')

    def do_left(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.player.position = self.NewPos(self.player, -1, 0)
        self.MoveMessage(self.player)
        self.encounter()

    def do_right(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.player.position = self.NewPos(self.player, 1, 0)
        self.MoveMessage(self.player)
        self.encounter()

    def do_up(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.player.position = self.NewPos(self.player, 0, 1)
        self.MoveMessage(self.player)
        self.encounter()

    def do_down(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.player.position = self.NewPos(self.player, 0, -1)
        self.MoveMessage(self.player)
        self.encounter()

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

    def do_addmon(self, args):
        try:
            params = shlex.split(args)
            name, greeting, hp, x, y = self.ParseArgs(params)
            if x >= self.size[0] or x < 0 or y >= self.size[1] or y < 0:
                raise SyntaxError
            elif name not in self.MONSTERS:
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

    def Attack(self, coords, damage):
        monster = self.field[coords[0]][coords[1]]
        dmg = min(damage, monster.hp)
        print(f"Attacked {monster.name}, damage {dmg} hp")
        monster.hp -= dmg
        if monster.hp == 0:
            print(f"{monster.name} died")
            self.field[coords[0]][coords[1]] = None
        else:
            print(f"{monster.name} now has {monster.hp}")

    def do_attack(self, args):
        if not self.isMonster():
            print("No monster here")
            return
        coords = self.player.position
        match shlex.split(args):
            case []:
                self.Attack(coords, self.WEAPONS['sword'])
            case ["with", weapon] if weapon in self.WEAPONS:
                self.Attack(coords, self.WEAPONS[weapon])
            case ["with", _]:
                print("Unknown weapon")
            case _:
                print("Wrong args for attack")

    def complete_attack(self, prefix, string, start, end):
        string = shlex.split(string)
        if len(string) < 2:
            string += [""] * (2 - len(string))
        match [prefix, string[-1], string[-2]]:
            case [prefix, "with", _]:
                return list(Dungeon.WEAPONS.keys())
            case _:
                return []


def main():
    print("<<< Welcome to Python-MUD 0.1 >>>")
    dungeon = Dungeon((10, 10), completekey='tab')
    dungeon.cmdloop()


if __name__ == '__main__':
    main()
