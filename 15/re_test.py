import re

regex = r"Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+).*"

test_str = "Sensor at x=2, y=18: closest beacon is at x=-2, y=15"

parse_regex = re.compile(regex)
m = parse_regex.match(test_str)
print(m.group('sx'))
print(m.group('sy'))

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.