import math
import time
import tracemalloc

"""
Azhra Yashna Azka - 2106705291 - DAA C
"""


class BranchAndBoundUnbounded01Knapsack:
    def __init__(self, W, filepath):
        self.W = W
        self.read_file(filepath)

    def read_file(self, filepath):
        with open(filepath, 'r') as f:
            val = eval(f.readline())
            wt = eval(f.readline())
            self.val = val
            self.wt = wt

        self.items = list(zip(val, wt))
        self.n = len(self.items)

    # Eliminate dominated items
    def filter_list(self):
        indices_to_keep = list(range(self.n))

        for current_idx in range(len(indices_to_keep) - 1):
            next_idx = current_idx + 1
            while next_idx < len(indices_to_keep):
                if self.should_remove_item(indices_to_keep[current_idx], indices_to_keep[next_idx]):
                    indices_to_keep.pop(next_idx)
                elif self.should_remove_item(indices_to_keep[next_idx], indices_to_keep[current_idx]):
                    indices_to_keep.pop(current_idx)
                    break
                else:
                    next_idx += 1

        filtered_list = [self.items[i] for i in indices_to_keep]
        return filtered_list

    def should_remove_item(self, idx_1, idx_2):
        item_1 = self.items[idx_1]
        item_2 = self.items[idx_2]
        return (
                math.floor(item_1[0] / item_1[1]) * item_1[0] >= item_2[0]
                or math.floor(item_1[1] / item_2[1]) * item_2[0] >= item_1[0]
        )

    def sort_items_decreasing(self):
        return sorted(self.items, key=lambda x: x[0] / x[1], reverse=True)

    def compute_upper_bound(self, residual_capacity, total_value, current_item_index):
        if current_item_index + 1 < self.n:
            (value_1, weight_1), (value_2, weight_2), (value_3, weight_3) = self.items[current_item_index:current_item_index + 3]

            partial_value = total_value + math.floor(residual_capacity / weight_2) * value_2
            double_residual_capacity = residual_capacity - math.floor(residual_capacity / weight_2) * weight_2
            upper_bound_1 = partial_value + math.floor(double_residual_capacity * value_3 / weight_3)

            adjusted_residual_capacity = double_residual_capacity + math.ceil(
                (1 / weight_1) * (weight_2 - double_residual_capacity)) * weight_1
            upper_bound_2 = partial_value + math.floor(
                (adjusted_residual_capacity * value_2 / weight_2) - math.ceil(
                    (1 / weight_1) * (weight_2 - double_residual_capacity)) * value_1)

            upper_bound = max(upper_bound_1, upper_bound_2)
        else:
            upper_bound = total_value

        return upper_bound

    def init_m_matrix(self):
        self.M = [[0 for i in range(self.W + 1)] for j in range(len(self.items) + 1)]

    def find_mi(self):
        min_weights = [float('inf') for _ in range(self.n)]
        for i in range(self.n):
            for idx, (v, w) in enumerate(self.items):
                if idx > i and w < min_weights[i]:
                    min_weights[i] = w

        return min_weights

    # Step 1
    def initialize(self):
        self.filter_list()
        self.init_m_matrix()
        self.items = self.sort_items_decreasing()
        self.z_topi = 0

        x = [0 for _ in range(self.n)]
        x[0] = math.floor(self.W / self.items[0][1])
        V = self.items[0][0] * x[0]
        residual_capacity = self.W - self.items[0][1] * x[0]
        upper_bound = self.compute_upper_bound(residual_capacity, V, 0)
        m = self.find_mi()

        self.develop(x, 0, V, residual_capacity, upper_bound, m)

    # Step 2
    def develop(self, x, i, V, residual_capacity, upper_bound, m):
        if residual_capacity < m[i]:
            if self.z_topi < V:
                self.z_topi = V
                if self.z_topi == upper_bound:
                    # Go to step 5 (Finish)
                    raise Exception("Optimal solution found")
            # Go to step 3 (Backtrack)
            self.backtrack(x, i, V, residual_capacity, m, upper_bound)
        else:
            min_j = self.find_min_j(residual_capacity, i)

            if (min_j < 0) or (V + self.compute_upper_bound(residual_capacity, V, min_j) <= self.z_topi):
                # Go to step 3 (Backtrack)
                self.backtrack(x, i, V, residual_capacity, m, upper_bound)

            if self.M[i][residual_capacity] >= V:
                # Got to step 3 (Backtrack)
                self.backtrack(x, i, V, residual_capacity, m, upper_bound)

            x[min_j] = math.floor(residual_capacity / self.items[min_j][1])
            V += self.items[min_j][0] * x[min_j]
            residual_capacity -= self.items[min_j][1] * x[min_j]
            self.M[i][residual_capacity] = V

    def find_max_j(self, x, i):
        return max((j for j in range(i + 1) if x[j] > 0))

    def find_min_j(self, residual_capacity, i):
        return min((j for j in range(i + 1, len(self.items)) if self.items[j][1] <= residual_capacity))

    def compute_residual_capacity_value(self, residual_capacity, i):
        return math.floor(residual_capacity * self.items[i + 1][0] / self.items[i + 1][1])

    def undo_choice(self, x, i, V, residual_capacity):
        V -= self.items[i][0] * x[i]
        residual_capacity += self.items[i][1] * x[i]
        x[i] = 0
        return V, residual_capacity, x[i]

    # Step 3
    def backtrack(self, x, i, V, residual_capacity, m, upper_bound):
        max_j = self.find_max_j(x, i)
        if max_j < 0:
            raise Exception("Optimal solution found")

        i = max_j
        x[i] -= 1
        V -= self.items[i][0]
        residual_capacity += self.items[i][1]

        if residual_capacity < m[i]:
            # Go to step 3 (Backtrack)
            self.backtrack(x, i, V, residual_capacity, m, upper_bound)

        if V + self.compute_residual_capacity_value(residual_capacity, i) <= self.z_topi:
            V, residual_capacity, x[i] = self.undo_choice(x, i, V, residual_capacity)
            # Go to step 3 (Backtrack)
            self.backtrack(x, i, V, residual_capacity, m, upper_bound)

        if residual_capacity >= m[i]:
            # Go to step 2 (Develop)
            self.develop(x, i, V, residual_capacity, upper_bound, m)

    # Step 4
    def replace_item(self, x, i, V, residual_capacity, m, upper_bound):
        j = i
        h = j + 1

        if self.z_topi >= V + self.compute_residual_capacity_value(residual_capacity, h):
            self.backtrack(x, i, V, residual_capacity, m, upper_bound)

        if self.items[h][1] >= self.items[j][1]:
            if self.should_skip_replace(h, i, V, residual_capacity):
                h += 1
                self.replace_item(x, i, V, residual_capacity, m, upper_bound)

            self.process_replace_item(x, h, V, residual_capacity, m, upper_bound)

        else:
            if self.should_continue_replace(h, i, residual_capacity, m):
                h += 1
                self.replace_item(x, i, V, residual_capacity, m, upper_bound)

            self.process_new_item(x, i, V, residual_capacity, m, upper_bound, h)

    # Helper methods
    def should_skip_replace(self, h, i, V, residual_capacity):
        return (self.items[h][1] == self.items[i][1]) or \
            (self.items[h][1] > residual_capacity) or \
            (self.z_topi >= V + self.items[h][0])

    def process_replace_item(self, x, h, V, residual_capacity, m, upper_bound):
        self.z_topi = V + self.items[h][0]
        x[h] = 1

        if self.z_topi == self.compute_upper_bound(residual_capacity, V, h):
            raise Exception("Optimal solution found")

        j = h
        h += 1
        self.replace_item(x, j, V, residual_capacity, m, upper_bound)

    def should_continue_replace(self, h, i, residual_capacity, m):
        return residual_capacity - self.items[h][1] < m[h - 1]

    def process_new_item(self, x, i, V, residual_capacity, m, upper_bound, h):
        i = h
        x[i] = math.floor(residual_capacity / self.items[i][1])
        V += self.items[i][0] * x[i]
        residual_capacity -= self.items[i][1] * x[i]

        # Go to step 2 (Develop)
        self.develop(x, i, V, residual_capacity, upper_bound, m)

    def run(self):
        try:
            self.initialize()

        except Exception as e:
            return self.z_topi

if __name__ == '__main__':
    filepaths = ["very_small.txt", "small.txt", "medium.txt", "large.txt"]
    for filepath in filepaths:
        tracemalloc.start()
        start_time = time.time()
        unbounded_knapsack = BranchAndBoundUnbounded01Knapsack(W=100, filepath=filepath)
        print(unbounded_knapsack.run())
        end_time = time.time()
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        top_stats = snapshot.statistics('lineno')
        total = sum(stat.size for stat in top_stats)
        runtime = (end_time - start_time) * 1000
        print('------' * 20)
        print(f'Runtime of {filepath} : '.ljust(45), f'{str(round(runtime))}'.ljust(5), '  ms')
        print(f'Total allocated size: '.ljust(45), f'{total / 1024} KiB')
