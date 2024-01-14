from random import randint, uniform, choice

class Results:
    """
    Telsonic MPX Methods for Result Evaluation and Generation.
    """
    def __init__(self):
        """
        Initializes the Results class with predefined Ok result ranges.
        """
        self.recipes = ("RECIPE1", "RECIPE2", "RECIPE3")
        self.ok_force_range = (1400, 1500)
        self.ok_power_range = (800, 900)
        self.ok_distance_range = (0.75, 0.90)
        self.count = 0

    def evaluate_results(self, force, power, distance):
        """
        Evaluates if the given results are Ok or Bad.

        Parameters:
        - force (int): Force value.
        - power (int): Power value.
        - distance (float): Distance value.

        Returns:
        - ok (int): 1 if the results are Ok, 0 otherwise.
        - bad (int): 1 if the results are Bad, 0 otherwise.
        """
        force_status = 1 if self.ok_force_range[0] <= force <= self.ok_force_range[1] else 0
        power_status = 1 if self.ok_power_range[0] <= power <= self.ok_power_range[1] else 0
        distance_status = 1 if self.ok_distance_range[0] <= distance <= self.ok_distance_range[1] else 0

        ok = 1 if force_status == 1 and power_status == 1 and distance_status == 1 else 0
        bad = 1 if not ok else 0

        return ok, bad

    def generate_random_results(self):
        """
        Generates random results for force, power, and distance.

        Returns:
        - random_force (int): Random force value.
        - random_power (int): Random power value.
        - random_distance (float): Random distance value.
        - ok (int): 1 if the generated results are Ok, 0 otherwise.
        - bad (int): 1 if the generated results are Bad, 0 otherwise.
        - count (int): Total count of generated results.
        - random_recipe (string): Random recipe.
        """
        random_force = randint(1390, 1510)
        random_power = randint(790, 910)
        random_distance = uniform(0.74, 0.91)
        random_recipe = choice(self.recipes)
        self.count += 1

        ok, bad = self.evaluate_results(random_force, random_power, random_distance)
        
        return random_force, random_power, random_distance, ok, bad, random_recipe, self.count