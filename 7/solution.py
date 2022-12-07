from collections import defaultdict
import re

class DirEntry ():
    def __init__(self, parent = None, name = None, size=None):
        self.parent = parent
        self.name = name
        self.size = size
        self.total_size = 0
        self.children = {}
        if self.parent is not None:
            assert name is not None
            assert name not in parent.children
            parent.children[name] = self
            p = self.parent
        if size is not None:
            p = self.parent
            while p is not None:
                p.total_size += size
                p = p.parent

    # For debugging.
    def tree(self, depth=0):
        desc = "  "*depth + " -"
        if self.name is not None:
            desc += self.name + " "
        else:
            desc += "/ "
        if self.size is None:
            desc += f"(dir, total_size={self.total_size})"
        else:
            desc += f"(file, size={self.size})"
        print(desc)
        for name,child in self.children.items():
            if child.size is None:
                child.tree(depth+1)
        for name, child in self.children.items():
            if child.size is not None:
                child.tree(depth+1)

    def part_1(self):
        total = 0
        for name,child in self.children.items():
            if child.size is None:
                total += child.part_1()
        if self.total_size > 100000:
            return total
        else:
            return total + self.total_size

    def smallest_at_least(self, minimum):
        smallests = [child.smallest_at_least(minimum) for child in self.children.values() if child.size is None]
        smallests = [child for child in smallests if child is not None]
        if self.total_size >= minimum:
            smallests.append(self)
        if not smallests:
            return None
        best = smallests[0]
        for item in smallests[1:]:
            if item.total_size < best.total_size:
                best = item
        return best



ROOT = DirEntry()

file_regex = re.compile(r'(?P<size>\d+) (?P<name>.+)')

def parse_input() :
    global ROOT
    cur_dir = ROOT
    with open ('./input.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            if line == "$ cd /":
                cur_dir = ROOT
            elif line == "$ cd ..":
                cur_dir = cur_dir.parent
            elif line[0:4] == "$ cd":
                dest = line[5:]
                cur_dir = cur_dir.children[dest]
            elif line[0:4] == "$ ls":
                pass
            elif line[:3] == "dir":
                DirEntry(cur_dir, line[4:])
            else:
                m = file_regex.match(line)
                size = int(m.group("size"))
                assert size != 0
                name = m.group("name")
                DirEntry(cur_dir, name, size)

parse_input()

if __name__ == "__main__":
    ROOT.tree()
    print("PART 1")
    print(ROOT.part_1())
    print("PART 2")
    total_space = 70000000
    free_space = total_space - ROOT.total_size
    required_free_pace = 30000000
    min_to_free = required_free_pace - free_space
    print(ROOT.smallest_at_least(min_to_free).total_size)
