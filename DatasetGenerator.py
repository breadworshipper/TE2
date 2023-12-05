import random

class DatasetGenerator:
    def __init__(self, size):
        self._weights = []
        self._values = []
        self._size = size

    def generate_random(self, filename):
        with open(filename, 'w') as f:
            for i in range(self._size):
                weight = random.randint(1, 10)
                value = random.randint(1, 10)
                self._weights.append(weight)
                self._values.append(value)


            f.write(str(self._weights) + '\n')
            f.write(str(self._values) + '\n')

        assert len(self._weights) == len(self._values), "wt dan val harus sama"

if __name__ == '__main__':
    very_small_dataset_generator = DatasetGenerator(10)
    small_dataset_generator = DatasetGenerator(100)
    medium_dataset_generator = DatasetGenerator(1000)
    large_dataset_generator = DatasetGenerator(10_000)

    very_small_dataset_generator.generate_random('very_small.txt')
    small_dataset_generator.generate_random('small.txt')
    medium_dataset_generator.generate_random('medium.txt')
    large_dataset_generator.generate_random('large.txt')
