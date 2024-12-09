def go(input):
    disk_map = [int(c) for c in input.strip()]

    files = deque() # location, length, index
    spaces = deque() # location, length
    offset = 0
    for i, l in enumerate(disk_map):
        if i % 2 == 0: # file
            files.append((offset, l, i // 2))
        else:
            spaces.append((offset, l))
        offset += l
        
    moved = []
    space_location, space_size = spaces.popleft() # space we are currently filling
    file_location, file_len, file_index = files.pop() # file we want to relocate
    while files:
        # take the left-hand file
        moved.append(files.popleft())
        while True: # move some number of files
            # how much to move
            take = min(file_len, space_size)
            moved.append((space_location, take, file_index))
            file_len -= take
            if file_len == 0:
                if not files:
                    break
                # next file
                file_location, file_len, file_index = files.pop() # file we want to relocate
            if take == space_size:
                # next space
                space_location, space_size = spaces.popleft() # space we are currently filling
                break
            else:
                space_size -= take
                space_location += take
    moved.append((file_location, file_len, file_index))
    
    sum = 0
    for loc, length, index in moved:
        for j in range(length):
           sum += (loc+j)*index 
    print("part 1 (checksum if fragmenting files):", sum)

    # part 2
    files = [] # location, length, index
    spaces = [] # location, length

    # Invariant: for all space sizes sz, the size of the first
    # first_space[sz] spaces is *less than* sz. This is an
    # optimization really, and might not be worth the effort, but
    # should turn a badly-conditioned problem from N^2 to N.log(N).
    first_space = defaultdict(int) # length -> index of first place to look

    offset = 0
    max_space = 0
    max_entry = 0
    for i, l in enumerate(disk_map):
        if l > max_entry:
            max_entry = l
        if i % 2 == 0: # file
            files.append((offset, l, i // 2))
        else:
            if l and l not in first_space:
                first_space[l] = len(spaces)
            spaces.append((offset, l))
            if l > max_space:
                max_space = l
        offset += l

    # Make first_space monotonic.
    for sz in range(max_space, 1, -1):
        if first_space[sz-1] > first_space[sz]:
            first_space[sz-1] = first_space[sz]

    # Move files
    moved = []
    for file in files[::-1]:
        file_off, file_len, file_index = file

        i = first_space[file_len]
        while i < file_index and spaces[i][1] < file_len:
            # skip spaces which have become too small
            i += 1
        if i < file_index:
            # Move to this space
            space_off, space_len = spaces[i]
            moved.append((space_off, file_len, file_index))

            # residue
            new_space = space_len - file_len # can be zero, we don't care.
            spaces[i] = (space_off + file_len, new_space)
        else: # can't move; i == file_index
            moved.append(file)

        # update lookup table; there's no point looking before i
        # for a space of size file_len or larger.
        sz = file_len
        while sz <= max_entry and i > first_space[sz]:
            first_space[sz] = i
            sz += 1

    sum = 0
    for loc, length, index in moved:
        for j in range(length):
           sum += (loc+j)*index 
    print("part 2 (checksum if not fragmenting files):", sum)
