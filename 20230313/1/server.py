import shlex
import asyncio


class Player:
    def __init__(self, position):
        self.pos = position


class Monster:
    def __init__(self, name, hello_string, hp, coords):
        self.name = name
        self.msg = hello_string
        self.hp = hp
        self.coords = coords


class Dungeon:
    ways = {
        "up": (0, 1),
        "down": (0, -1),
        "right": (1, 0),
        "left": (-1, 0),
    }

    def __init__(self, size, player):
        self.size = size
        self.field = [[None] * size[0] for _ in range(size[1])]
        self.player = player

    def add_monster(self, monster):
        x, y = monster.coords
        msg = f"Added monster {monster.name} to {(x, y)} saying {monster.msg}."
        if self.field[x][y]:
            msg += "\nReplaced the old monster"
        self.field[x][y] = monster
        return msg

    def encounter(self, x, y):
        return self.field[x][y].msg, self.field[x][y].name

    def NewPos(self, way):
        x, y = Dungeon.ways[way]
        i = self.player.pos[0] = (x + self.player.pos[0]) % 10
        j = self.player.pos[1] = (y + self.player.pos[1]) % 10
        msg = [f"Moved to ({i}, {j})"]
        if self.field[i][j]:
            msg += self.encounter(i, j)
        return msg

    def attack(self, pos, name, dmg):
        msg = "No monster here"
        x, y = pos
        if monster := self.field[x][y]:
            if monster.name == name:
                dmg = min(dmg, monster.hp)
                msg = f"Attacked {monster.name}, damage {dmg} hp"
                monster.hp -= dmg
                if monster.hp == 0:
                    msg += f"\n{monster.name} died"
                    self.field[x][y] = None
                else:
                    msg += f"\n{monster.name} now has {monster.hp} hp"
            else:
                msg = f"No {name} here"
        return msg


async def echo(reader, writer):
    host, port = writer.get_extra_info("peername")
    player = Player([0, 0])
    dungeon = Dungeon((10, 10), player)

    while not reader.at_eof():
        data = await reader.readline()
        msg = shlex.split(data.decode().strip())
        ans = ""
        print(msg)
        match msg:
            case way if len(way) == 1 and way[0] in Dungeon.ways:
                ans = "\n".join(dungeon.NewPos(way[0]))
            case ["addmon", *args]:
                print("addmon")
                ans = dungeon.add_monster(
                    Monster(
                        args[0],
                        args[args.index("hello") + 1],
                        int(args[args.index("hp") + 1]),
                        (
                            int(args[args.index("coords") + 1]),
                            int(args[args.index("coords") + 2]),
                        ),
                    )
                )
            case ["attack", *args]:
                print("attack")
                ans = dungeon.attack(player.pos, args[0], int(args[1]))
            case ["Connect"]:
                ans = "<<< Welcome to Python-MUD 0.1 >>>"
            case _:
                ans = "Error"

        writer.write(ans.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
