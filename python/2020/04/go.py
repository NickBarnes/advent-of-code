yr_re = re.compile('^[0-9]{4}$')

def valid_birth_year(s):
    return yr_re.match(s) and 1920 <= int(s) <= 2002

def valid_issue_year(s):
    return yr_re.match(s) and 2010 <= int(s) <= 2020

def valid_expiration_year(s):
    return yr_re.match(s) and 2020 <= int(s) <= 2030

ht_re = re.compile('^([0-9]+)(cm|in)$')

def valid_height(s):
    m = ht_re.match(s)
    return m and ((m.group(2) == 'cm' and 150 <= int(m.group(1)) <= 193) or
                  (m.group(2) == 'in' and 59 <= int(m.group(1)) <= 76))

hcl_re = re.compile('^#[0-9a-f]{6}$')

def valid_hair(s):
    return hcl_re.match(s)

ecls = set('amb blu brn gry grn hzl oth'.split())

def valid_eye(s):
    return s in ecls

pid_re = re.compile('^[0-9]{9}$')

def valid_pid(s):
    return pid_re.match(s)


validators = {'byr': valid_birth_year,
              'iyr': valid_issue_year,
              'eyr': valid_expiration_year,
              'hgt': valid_height,
              'hcl': valid_hair,
              'ecl': valid_eye,
              'pid': valid_pid,
              'cid': None}

item_re = re.compile('([a-z]+):(.*)')

def go(input):
    passports = [' '.join(s).split() for s in parse.sections(input)]
    good_keys = 0
    valid = 0
    for passport in passports:
        d = {m.group(1):m.group(2)
             for item in passport
             if (m := item_re.match(item))}

        missing = set(validators.keys()) - set(d.keys())
        if len(missing) == 0 or (len(missing) == 1 and 'cid' in missing):
            good_keys += 1
            if all(k == 'cid' or validators[k](v) for k,v in d.items()):
                valid += 1
    print("part 1 (passports with all required fields):", good_keys)
    print("part 2 (passports with all items valid):", valid)
    
    
