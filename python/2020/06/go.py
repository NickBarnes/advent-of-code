# Template for AoC daily solution. To add to imports, see
# util/__init__.py.

def go(input):
    anyone = 0
    everyone = 0
    for group in parse.sections(input):
        all_questions_answered_yes_in_group = set(''.join(group))
        anyone += len(all_questions_answered_yes_in_group)
        everyone += len(set.intersection(*(set(l) for l in group)))
    print(f"part 1 (number of questions to which anyone in a group said yes): {anyone}")
    print(f"part 2 (number of questions to which everyone in a group said yes): {everyone}")
