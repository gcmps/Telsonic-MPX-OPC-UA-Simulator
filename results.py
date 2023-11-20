from random import randint, uniform

ok_force_range = (1400, 1500)
ok_power_range = (800, 900)
ok_distance_range = (0.75, 0.90)
count = 0

def evaluate_parameters(force, power, distance):
    force_status = 1 if ok_force_range[0] <= force <= ok_force_range[1] else 0
    power_status = 1 if ok_power_range[0] <= power <= ok_power_range[1] else 0
    distance_status = 1 if ok_distance_range[0] <= distance <= ok_distance_range[1] else 0

    if force_status == 1 and power_status == 1 and distance_status == 1:
        ok = 1
        bad = 0
    else:
        ok = 0
        bad = 1

    return ok, bad

def generate_random_values():
    global count
    random_force = randint(1390, 1510)
    random_power = randint(790, 910)
    random_distance = uniform(0.74, 0.91)
    count += 1

    ok, bad = evaluate_parameters(random_force, random_power, random_distance)
    
    return random_force, random_power, random_distance, ok, bad, count