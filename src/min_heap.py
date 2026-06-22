class MinHeap:
    def __init__(self, key = lambda x: x, first_element = None):
        self.heap = list()
        self.key = key
        if first_element:
            self.heap.append(first_element)

    def len(self) -> int:
        return len(self.heap)

    def element(self, i: int):
        return self.key(self.heap[i])
    
    def insert(self, element):
        self.heap.append(element)
        i = self.len() - 1
        while i > 0 and self.element(i) < self.element((i - 1) // 2):
            self.heap[i], self.heap[(i - 1) // 2] = self.heap[(i - 1) // 2], self.heap[i]
            i = (i - 1) // 2

    def pop(self):
        if self.len() == 0:
            return None
        
        if self.len() == 1:
            return self.heap.pop()
        
        i = 0
        minimum = self.heap[0]
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        self.heap.pop()

        while (i * 2) + 1 < self.len():
            minor = (i * 2) + 1
            if (i * 2) + 2 < self.len() and self.element((i * 2) + 2) < self.element(minor):
                minor += 1
            if self.element(minor) < self.element(i):
                self.heap[minor], self.heap[i] = self.heap[i], self.heap[minor]
            else:
                break
            i = minor
        return minimum

if __name__ == "__main__":
    print("Test with 1 element")
    heap = MinHeap(first_element = 3)
    print(f"{heap.pop()}, {heap.len()}")
    
    print("Test with 2 elements")
    heap = MinHeap(first_element = 3)
    heap.insert(2)
    print(f"{heap.pop()}, {heap.len()}")
    print(f"{heap.pop()}, {heap.len()}")

    print("Test with 3 elements")
    heap = MinHeap(first_element = 3)
    heap.insert(2)
    heap.insert(-5)
    print(f"{heap.pop()}, {heap.len()}")
    print(f"{heap.pop()}, {heap.len()}")
    print(f"{heap.pop()}, {heap.len()}")

    print("Test with 4 elements")
    heap = MinHeap(first_element = 3)
    heap.insert(2)
    heap.insert(-5)
    heap.insert(4)
    print(f"{heap.pop()}, {heap.len()}")
    print(f"{heap.pop()}, {heap.len()}")
    print(f"{heap.pop()}, {heap.len()}")
    print(f"{heap.pop()}, {heap.len()}")

    
