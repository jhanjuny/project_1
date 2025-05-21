import random

def generate_random_numbers(count=10, start=1, end=100):
    """Generate a list of random integers."""
    return [random.randint(start, end) for _ in range(count)]

if __name__ == "__main__":
    numbers = generate_random_numbers()
    print("Random numbers:", numbers)
    