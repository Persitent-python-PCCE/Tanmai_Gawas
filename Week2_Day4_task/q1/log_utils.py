def parse_line(line):
    parts = line.split(" ", 3)
    level = parts[2]
    message = parts[3]
    return (level, message)

def read_logs(path):
    entries = []
    with open(path, "r") as file:
        for line in file:
            entries.append(parse_line(line))

    return entries

