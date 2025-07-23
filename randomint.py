import random

class UniqueRandomIntGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "min_value": ("INT", {"default": 1, "min": -1000000, "max": 1000000}),
                "max_value": ("INT", {"default": 10, "min": -1000000, "max": 1000000}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1})
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("random1", "random2", "random3", "random4", "random5")
    FUNCTION = "generate_random_integers"
    CATEGORY = "utils"

    def generate_random_integers(self, min_value, max_value, seed):
        if max_value - min_value + 1 < 5:
            raise ValueError("Range too small for 5 unique numbers")
        
        # Use the provided seed to initialize the random number generator
        random.seed(seed)
        
        # Generate a new random sample
        return random.sample(range(min_value, max_value + 1), 5)

NODE_CLASS_MAPPINGS = {
    "UniqueRandomIntGenerator": UniqueRandomIntGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UniqueRandomIntGenerator": "Unique RandomInt Generator"
}
