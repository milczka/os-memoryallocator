from itertools import groupby

class MemoryAllocator:

    memory_map = []
    empty_blocks = {}
    last_block_allocated = -1

    def __init__(self, memory_map):
        self.memory_map = memory_map
        self.empty_blocks = self.update_empty_blocks(0)

    # helper function
    def find_next_zero(self, search_list, starting_idx):

        if(search_list[starting_idx] == 0):
            raise Exception('Cannot pass in index that contains a zero')
        for index, value in enumerate(search_list):
            if (index > starting_idx) and (value == 0):
                return index

    # helper function
    def update_empty_blocks(self, search_index):
        grouped_values = [(k, sum(1 for i in g)) for k,g in groupby(memory_map)]
        vals_with_index = {}
        absolute_index = 0
        for index, val in enumerate(grouped_values):
            vals_with_index[absolute_index] = grouped_values[index]
            absolute_index += grouped_values[index][1]

        return vals_with_index


    def best_fit_allocate(self, processID, memory_size, memory_map):

        allocate_at = -1
        # format: index, size
        available_memory_sizes = []

        for key, value in self.empty_blocks.items():
            if value[0] == 0 and value[1] >= memory_size:
                available_memory_sizes.append((key, value[1]))

        # find candidate closest to requested size
        if(len(available_memory_sizes) != 0):
            # problem - cannot be <memory_size
            allocate_at = min(range(len(available_memory_sizes)), key=lambda i: abs(available_memory_sizes[i][1]-memory_size))

        for i in range(allocate_at, allocate_at+memory_size):
            memory_map[i] = processID

        self.empty_blocks = self.update_empty_blocks(allocate_at)

        return allocate_at

    def first_fit_allocate(self, processID, memory_size, memory_map):

        if memory_size > len(memory_map):
            raise Exception('Requested memory larger than memory map')

        allocate_at = -1
        if self.last_block_allocated == -1:
            self.last_block_allocated = 0

        for key, value in self.empty_blocks.items():
            if value[0] == 0 and value[1] >= memory_size:
                allocate_at = key

        # populate map with processID
        for i in range(allocate_at, allocate_at+memory_size):
            memory_map[i] = processID

        # update empty blocks
        self.empty_blocks = self.update_empty_blocks(allocate_at)

        last_block_allocated = allocate_at
        return allocate_at

    def worst_fit_allocate(self, processID, memory_size, memory_map):
        allocate_at = -1
        available_memory_sizes = {}

        for key, value in self.empty_blocks.items():
            if value[0] == 0:
                available_memory_sizes[key] = value[1]

        # find candidate with largest block
        for key, value in available_memory_sizes.items():
            if value > allocate_at:
                allocate_at = value

        for i in range(allocate_at, allocate_at+memory_size):
            memory_map[i] = processID

        self.empty_blocks = self.update_empty_blocks(allocate_at)

        last_block_allocated = allocate_at
        return allocate_at

    def next_fit_allocate(self, processID, memory_size, memory_map, last_block_allocated):
        allocate_at = -1

        # start search from the last block allocated
        for key, value in empty_blocks:
            if key > lastBlockAllocated and value[0] == 0 and value[1] >= memory_size:
                allocate_at = key

        for i in range(allocate_at, allocate_at+memory_size):
            memory_map[i] = processID

        self.empty_blocks = self.update_empty_blocks(allocate_at)
        last_block_allocated = allocate_at

        return allocate_at
               
    def releaseMemory(self, processID):
        for index, elem in enumerate(self.memory_map):
            if elem == processID:
                memory_map[index] = 0

        self.update_empty_blocks(0)


if __name__ == '__main__':
    index = 0
    memory_map = [0, 0, 2, 2, 0, 0, 0, 0, 3, 3, 3, 0, 0, 4, 0]
    empty_blocks = {}
    MA = MemoryAllocator(memory_map)
    print(MA.memory_map)
    print(MA.empty_blocks)
    MA.first_fit_allocate(7, 3, MA.memory_map)
    print(MA.memory_map)
    print(MA.empty_blocks)

    MA.releaseMemory(7)
    print(MA.memory_map)

    # PROBLEM: overwrites existing nonzero values :(
    MA.best_fit_allocate(7, 3, MA.memory_map)
    print(MA.memory_map)

    MA.releaseMemory(7)
    print('Release memory:', MA.memory_map)

    MA.next_fit_allocate(7, 3, MA.memory_map, MA.last_block_allocated)
    print(MA.memory_map)

    MA.releaseMemory(7)
    print(MA.memory_map)

    MA.worst_fit_allocate(7, 3, MA.memory_map)
    print(MA.memory_map)
