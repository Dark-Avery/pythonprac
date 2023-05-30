from unittest import main, TestCase
from unittest.mock import MagicMock
from moodclient.moodclient import client
import cowsay
import cmd


class Test_Client(TestCase):
    def setUp(self):
        self.socket = MagicMock()
        self.res = []
        self.socket.send = lambda x: self.res.append(x)
        self.socket.recv = lambda x: "".encode()
        self.dungeon = client.Dungeon(self.socket)

    def test_1(self):
        self.dungeon.onecmd("up")
        self.assertEqual(self.res[0].decode(), "move up\n")

    def test_2(self):
        self.dungeon.onecmd("addmon default hello hi coords 1 1 hp 15")
        self.assertEqual(self.res[0].decode(), "addmon default hello hi coords 1 1 hp 15\n")

    def test_3(self):
        self.dungeon.onecmd("attack default with axe")
        self.assertEqual(self.res[0].decode(), "attack default 20\n")

    def test_r(self):
        self.dungeon.onecmd("attack dragon")
        self.assertEqual(self.res[0].decode(), "attack dragon 10\n")


def run_tests():
    main()
