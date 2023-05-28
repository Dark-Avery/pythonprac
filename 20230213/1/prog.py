import os
import sys
import glob
import zlib


def show_commit(commit):
	commit_file = os.path.join(".git/objects", commit[0:2], commit[2:])
	with open(commit_file, "rb") as f:
		data = zlib.decompress(f.read())
	tree = b"\n".join(data.split(b"\n")[0:1]).decode().split("tree")[1].strip()
	parent = b"\n".join(data.split(b"\n")[1:2]).decode().split("parent")[1].strip()
	print(f"TREE for commit {commit}")
	return tree, parent

def show_tree(tree):
	tree_file = os.path.join(".git/objects", tree[0:2], tree[2:])
	with open(tree_file, "rb") as f:
		data = zlib.decompress(f.read())
	header, _, body = data.partition(b'\x00')
	while body:
		treeobj, _, tail = body.partition(b"\x00")
		tmode, tname = treeobj.split()
		num, body = tail[:20], tail[20:]
		obj_type = "tree" if list(glob.iglob(os.path.join(".git/objects", num.hex()[0:2], num.hex()[2:]))) else "blob"
		print(f"{obj_type} {num.hex()}\t{tname.decode()}")


def in_objs(hash):
	return len(list(glob.iglob(os.path.join(".git/objects", hash[0:2], hash[2:]))))


if len(sys.argv) == 1:
	for file in glob.iglob(".git/refs/heads/*"):
		print(file.split(os.sep)[-1])
else:
	file = glob.iglob(os.path.join(".git/refs/heads", sys.argv[1])).__next__()
	with open(file, "r") as f:
		parent = f.read().split()[0]

	while in_objs(parent):
		tree, parent = show_commit(parent)
		show_tree(tree)
