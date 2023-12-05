import time
import tracemalloc
import sys

"""
Azhra Yashna Azka - 2106705291 - DAA C
"""

sys.setrecursionlimit(10**6)

class UnboundedKnapsack:
    def __init__(self, W, filepaths):
        self.W = W
        self.val = None
        self.wt = None
        self.filepaths = filepaths
        self.solution = None

    def read_file(self, filepath):
        with open(filepath, 'r') as f:
            self.val = eval(f.readline())
            self.wt = eval(f.readline())

    def unboundedKnapsack(self):
        dp = [0 for i in range(self.W + 1)]

        for i in range(self.W + 1):
            for j in range(len(self.wt)):
                if (self.wt[j] <= i):
                    dp[i] = max(dp[i], dp[i - self.wt[j]] + self.val[j])

        self.solution = dp[self.W]

    def find_solution(self):
        for filepath in self.filepaths:
            self.read_file(filepath)
            if filepath=="very_small.txt":
                print(f"very small dataset: {self.val} {self.wt}")

            tracemalloc.start()
            start_time = time.time()
            self.unboundedKnapsack()
            end_time = time.time()
            snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()
            runtime = (end_time - start_time) * 1000

            print('------' * 20)
            print(f'Runtime of {filepath} : '.ljust(45), f'{str(round(runtime))}'.ljust(5), '  ms')

            top_stats = snapshot.statistics('lineno')
            total = sum(stat.size for stat in top_stats)
            print(f'Total allocated size: '.ljust(45), f'{total / 1024} KiB')

            print(f'Optimal solution: ' .ljust(45), f'{self.solution}')


if __name__ == '__main__':
    filepaths = ["very_small.txt", "small.txt", "medium.txt", "large.txt"]

    unbounded_knapsack = UnboundedKnapsack(W=100, filepaths=filepaths)
    unbounded_knapsack.find_solution()
