VALUE_DURING_EXEC = [1]
PIXELS = []

def part_1():
    with open('./input.txt') as f:
        lines = f.read().splitlines()
        for l in lines:
            val = VALUE_DURING_EXEC[-1]
            if l == 'noop':
                VALUE_DURING_EXEC.append(val)
            else:
                input = int(l[5:])
                VALUE_DURING_EXEC.append(val)
                VALUE_DURING_EXEC.append(val+input)
    #print(VALUE_DURING_EXEC)
    sum = 0
    for i in range(20,len(VALUE_DURING_EXEC),40):
        print(i*VALUE_DURING_EXEC[i-1])
        sum += i*VALUE_DURING_EXEC[i-1]
    print(sum)
    # for i in range(len(VALUE_DURING_EXEC)):
    #     print(f"{i} {VALUE_DURING_EXEC[i]}")

def part_2():
    for i in range(0, len(VALUE_DURING_EXEC)):
        sprite_center = VALUE_DURING_EXEC[i]
        pos = i % 40
        if sprite_center-1 <= pos and sprite_center+1 >= pos:
            PIXELS.append('#')
        else:
            PIXELS.append('.')
    for i in range(0,len(PIXELS),40):
        print("".join(PIXELS[i:i+40]))

part_1()
part_2()