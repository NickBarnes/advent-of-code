def transform(subject, loops = None, target = None):
    v = 1
    i = 0
    while True:
        v *= subject
        v = v % 20201227
        i += 1
        if i == loops:
            return v
        if v == target:
            return i

def go(input):
    lines = parse.lines(input)
    card_public_key = int(lines[0])
    door_public_key = int(lines[1])
    # explicitly told to use trial-and-error
    card_loop_size = transform(7, target = card_public_key)
    door_loop_size = transform(7, target = door_public_key)
    key = transform(card_public_key, loops = door_loop_size)
    assert key == transform(door_public_key, loops = card_loop_size)
    print("part 1 (encryption key):", key)

