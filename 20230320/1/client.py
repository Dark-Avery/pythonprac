from cowsay import cowsay, list_cows, read_dot_cow
import shlex
import cmd
import sys
import socket


class Dungeon(cmd.Cmd):
    MONSTERS_EXT = set(list_cows())
    add_list_cows = {"jgsbat"}
    MONSTERS = MONSTERS_EXT | add_list_cows
    WEAPONS = {"sword": 10, "spear": 15, "axe": 20}
    size = (10, 10)

    def send_recv_server(self, msg):
        s.send((msg.strip() + "\n").encode())
        ans = s.recv(1024).decode().strip().replace("'", "")

        if len(t := ans.split("\n")) == 3:
            if t[2] in self.add_list_cows:
                filename = f"{t[2]}.cow"
                with open(filename, "r") as cowfile:
                    image = cowsay(t[2], cowfile=read_dot_cow(cowfile))
            else:
                image = cowsay(t[1], cow=t[2])
            print(image)
        else:
            print(ans)

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

    def do_exit(self, args):
        return True

    def do_left(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.send_recv_server("left")

    def do_right(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.send_recv_server("right")

    def do_up(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.send_recv_server("up")

    def do_down(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.send_recv_server("down")

    def do_addmon(self, args):
        try:
            params = shlex.split(args)
            name, greeting, hp, x, y = self.ParseArgs(params)
            if x >= self.size[0] or x < 0 or y >= self.size[1] or y < 0:
                raise SyntaxError
            elif name not in self.MONSTERS:
                raise NameError
            else:
                self.send_recv_server("addmon " + shlex.join(params))
        except SyntaxError:
            print("Invalid arguments")
        except NameError:
            print("Cannot add unknown monster")
        except ValueError:
            print("HP and coords should be a digit")

    def do_attack(self, args):
        match shlex.split(args):
            case [monster_name, "with", weapon]:
                if weapon in self.WEAPONS:
                    self.send_recv_server(" ".join(["attack", monster_name, str(self.WEAPONS[weapon])]))
                else:
                    print("Unknown weapon")
            case [monster_name]:
                self.send_recv_server(" ".join(["attack", monster_name, str(self.WEAPONS[weapon])]))
            case _:
                print("Wrong args for attack")

    def complete_attack(self, prefix, string, start, end):
        string = shlex.split(string)
        if len(string) < 2:
            string += [""] * (2 - len(string))
        match [prefix, string[-1], string[-2]]:
            case [prefix, "with", _] if not prefix:
                return list(Dungeon.WEAPONS.keys())
            case [prefix, _, "with"] if prefix:
                return [weapon for weapon in Dungeon.WEAPONS if weapon.startswith(prefix)]
            case [prefix, "attack", _] if not prefix:
                return list(Dungeon.MONSTERS)
            case [prefix, _, "attack"]:
                return [monster for monster in Dungeon.MONSTERS if monster.startswith(prefix)]
            case _:
                return []


def main():
    print(s.recv(1024).decode().strip())
    dungeon = Dungeon(completekey='tab')
    dungeon.cmdloop()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if len(sys.argv) > 2:
            s.connect((sys.argv[1], int(sys.argv[2])))
        else:
            s.connect((sys.argv[1], 1337))
        s.send("Connect\n".encode())
        main()
