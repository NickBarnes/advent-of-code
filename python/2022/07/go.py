# Directories and files

# I bet this could be done with dicts and lists pretty easily but hey.

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def total(self):
        return self.size

    # handy utility method for debugging
    def ls(self,indent):
        print(f"{indent}{self.name:20}{self.size}")

class Dir:
    def __init__(self, name, parent):
        self.contents = {}
        self.name = name
        self.parent = parent
    
    def total(self):
        return sum(x.total() for x in self.contents.values())
    
    # handy utility method for debugging
    def ls(self, indent=''):
        print(f"{indent}{self.name}:")
        for c in self.contents.values():
            c.ls(indent+'  ')

def go(input):
    root = Dir('/', None)
    pwd = root
    dirs = [] # accumulate all dirs so we can search later.
    for l in parse.lines(input):
        if l[0] == '$': # command
            cmd = l.split() # $, cd/ls, cd-target
            if cmd[1] == 'cd':
                if cmd[2] == '/':
                    pwd = root
                elif cmd[2] == '..':
                    pwd = pwd.parent
                else:
                    pwd = pwd.contents[cmd[2]]
            else: # ls: do nothing; contents handled below
                pass
        else: # ls contents line
            s,f = l.split()
            if f in pwd.contents: # already got this
                continue
            if s == 'dir': # sub-directory
                d = Dir(f, pwd)
                dirs.append(d)
                pwd.contents[f] = d
            else: # file
                pwd.contents[f] = File(f, int(s))

    total_of_small_dirs = sum(t for d in dirs if (t := d.total()) < 100000)
    print(f"part 1 (total of small dirs): {total_of_small_dirs}")
    
    space_avail = 70000000 - root.total()
    to_free = 30000000 - space_avail
    # slow but I don't care
    best_dir = min((d for d in dirs if d.total() >= to_free), key=lambda d:d.total())
    print(f"part 2 (size of best dir to delete): {best_dir.total()}")
