from cowsay import cowsay, list_cows, read_dot_cow
import shlex
import cmd
import sys
import socket
import threading
import readline
from io import StringIO


cust_mstr = read_dot_cow(
    StringIO(
        """
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC
"""
    )
)


class Dungeon(cmd.Cmd):
    MONSTERS_EXT = set(list_cows())
    add_list_cows = {"jgsbat"}
    MONSTERS = MONSTERS_EXT | add_list_cows
    WEAPONS = {"sword": 10, "spear": 15, "axe": 20}
    size = (10, 10)
    prompt = ">> "

    def __init__(self, s, **kwargs):
        super().__init__(**kwargs)
        self.s = s

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

    def do_quit(self, args):
        self.s.send("quit\n".encode())
        self.onecmd("exit")

    def do_left(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.s.send(("move left\n").encode())

    def do_right(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.s.send(("move right\n").encode())

    def do_up(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.s.send(("move up\n").encode())

    def do_down(self, args):
        if len(args) > 0:
            print("Wrong argemunts")
            return
        self.s.send(("move down\n").encode())

    def do_addmon(self, args):
        try:
            params = shlex.split(args)
            name, greeting, hp, x, y = self.ParseArgs(params)
            if x >= self.size[0] or x < 0 or y >= self.size[1] or y < 0:
                raise SyntaxError
            elif name not in self.MONSTERS:
                raise NameError
            else:
                msg = "addmon " + shlex.join(params)
                self.s.send((msg.strip().lower() + "\n").encode())
        except SyntaxError:
            print("Invalid arguments")
        except NameError:
            print("Cannot add unknown monster")
        except ValueError:
            print("HP and coords should be a digit")

    def do_sayall(self, args):
        """
        Sends a message to all players.

        :param message: (str) The text of the message to send.

        :return: None
        """
        message = "sayall " + args + "\n"
        self.s.send(message.encode())

    def do_attack(self, args):
        match shlex.split(args):
            case [monster_name, "with", weapon]:
                if weapon in self.WEAPONS:
                    self.s.send(
                        (" ".join(["attack", monster_name, str(self.WEAPONS[weapon])]) + "\n").encode()
                    )
                else:
                    print("Unknown weapon")
            case [monster_name]:
                self.s.send(
                        (" ".join(["attack", monster_name, str(self.WEAPONS["sword"])]) + "\n").encode()
                    )
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


def get_reponse(s, cmdline):
    while True:
        ans = s.recv(2048).decode()
        if ans:
            if ans.strip() == "Goodbye":
                break

            print(ans)
            print(
                f"\n{cmdline.prompt}{readline.get_line_buffer()}",
                end="",
                flush=True,
            )


def start(s):
    print("<<< Welcome to Python-MUD 0.1 >>>")
    print("Active session:")
    msg = s.recv(1024).decode()
    print(msg)
    if "exists" in msg:
        return

    cmdline = Dungeon(s)
    gm = threading.Thread(target=get_reponse, args=(s, cmdline))
    gm.start()
    Dungeon(s, completekey='tab').cmdloop()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 1337))
        s.send(f"{sys.argv[1]}\n".encode())
        main(s)
