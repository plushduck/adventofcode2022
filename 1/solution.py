from functools import reduce
from typing import List

def cal_per_elf_reducer(output: List[int], val: str) -> List[int]:
    if val == "":
        output.append(0)
    else:
        output[-1] += int(val)
    return output

class CalorieManifest:

    def __init__(self, filename: str):
        with open(filename) as f:
            self.itemized_cals = f.read().splitlines()
            self.cals_per_elf = reduce(cal_per_elf_reducer, self.itemized_cals, [0])

if __name__ == "__main__":
    manifest = CalorieManifest("./input.txt")

    sorted_cals_per_elf = manifest.cals_per_elf.copy()
    sorted_cals_per_elf.sort(reverse=True)

    print(f"Most calories per inventory = {sorted_cals_per_elf[:3]}")
    print(f"Total = {sum(sorted_cals_per_elf[:3])}")
