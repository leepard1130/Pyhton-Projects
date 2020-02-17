def score(filename):
    lines = {}
    f = open (filename, 'r')
    for i, line in enumerate(f) :
        lines[i] = line.strip()
    f.close()
    return lines
   
