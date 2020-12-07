import intcode as ic


def read_file():
    with open('input') as f:
        lines = f.readlines()
    return lines


def parse_lines(lines):
    passports = []
    passport = None
    for line in lines:
        if line.strip() == '':
            # print('---')
            passports.append(passport)
            passport = {}
            continue

        line = line.split(' ')
        line = list(map(str.strip, line))

        if passport is None:
            passport = {}

        for kv in line:
            key, value = kv.split(':')
            passport[key] = value
    passports.append(passport)
    return passports


def passport_is_valid(passport: dict, validate=False):
    keys = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
    for key in keys:
        if key not in passport:
            return False
        if validate:
            value: str = passport[key]
            if key == 'byr' and not 1920 <= int(value) <= 2002:
                return False
            elif key == 'iyr' and not 2010 <= int(value) <= 2020:
                return False
            elif key == 'eyr' and not 2020 <= int(value) <= 2030:
                return False
            elif key == 'hgt':
                unit = value[-2:]
                if unit == 'cm' and not 150 <= int(value[:-2]) <= 193:
                    return False
                elif unit == 'in' and not 59 <= int(value[:-2]) <= 76:
                    return False
                elif unit not in ('cm', 'in'):
                    return False
            elif key == 'hcl':
                if not value.startswith('#') or len(value) != 7:
                    return False
                else:
                    try:
                        int(value[1:], base=16)
                    except TypeError:
                        return False
            elif key == 'ecl':
                if value not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
                    return False
            elif key == 'pid':
                if len(value) != 9:
                    return False
                try:
                    int(value)
                except TypeError:
                    return False
    return True


def count_valid_passports(passports):
    return (sum(1 for p in passports if passport_is_valid(p)),
            sum(1 for p in passports if passport_is_valid(p, True)))


lines = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""".split('\n')

tester = ic.Tester("")

passports = parse_lines(lines)
tester.test_value(count_valid_passports(passports), (2, 2))

lines = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007""".split('\n')

passports = parse_lines(lines)
tester.test_value(count_valid_passports(passports), (4, 0))

lines = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
""".split('\n')

passports = parse_lines(lines)
tester.test_value(count_valid_passports(passports), (4, 4))

lines = read_file()
passports = parse_lines(lines)
valid_passports = count_valid_passports(passports)
tester.test_value(valid_passports, (182, 109), 'solution to exercise 1=%s and 2=%s')
