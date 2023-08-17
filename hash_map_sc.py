# Description:  This is an implementation of a Hashmap using singly linked lists. It includes the following functions: put()
# get(), remove(), contains_key(), clear(), empty_buckets(), resize_table(), table_load(), get_keys() and a find_mode() function

from include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        method updates the key/value pair in the hash map
        """
        if self.table_load() >= 1:
            self.resize_table(self.get_capacity()*2)

        index = self._hash_function(key) % self.get_capacity()

        sLlLength = self._buckets[index].length()
        sLList = self._buckets.get_at_index(index)

        # if no nodes in list, insert key/value pair
        if sLlLength == 0:
            sLList.insert(key, value)
            self._size += 1
        # if key exists, replace value
        elif sLList.contains(key):
            sLList.remove(key)
            sLList.insert(key, value)
        else:
            sLList.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        method returns the number of empty buckets in the hash table
        """
        numEmptyBuckets = 0
        for i in range(self._buckets.length()):
            if self._buckets[i].length() == 0:
                numEmptyBuckets += 1
        return numEmptyBuckets

    def table_load(self) -> float:
        """
        method returns the current hash table load factor
        """
        return self.get_size()/self.get_capacity()

    def clear(self) -> None:
        """
        method clears the contents of the hash map
        """
        curCapacity = self.get_capacity()
        curFunction = self._hash_function
        curSize = self.get_size()

        for i in range(curCapacity):
            if self._buckets[i].length() > 0:
                self._buckets[i] = LinkedList()

        self._size = 0


    def resize_table(self, new_capacity: int) -> None:
        """
        method changes the capacity of the internal hash table
        """
        if new_capacity >= 1:
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

            old_capacity = self.get_capacity()
            newArr = DynamicArray()

            newLoad = self.get_size() / new_capacity

            if newLoad > 1:
                while newLoad > 1:
                    new_capacity *= 2
                    new_capacity = self._next_prime(new_capacity)
                    newLoad = self.get_size() / new_capacity

            for i in range(new_capacity):
                newArr.append(LinkedList())

            for i in range(old_capacity):
                bucket = self._buckets.pop()
                for node in bucket:
                    if bucket.length()>0:
                        key = node.key
                        value = node.value
                        newIndex = self._hash_function(key) % new_capacity

                        newArr[newIndex].insert(key, value)


            self._capacity = new_capacity
            self._buckets = newArr

    def get(self, key: str):
        """
        method returns the value associated with the given key
        """

        index = self._hash_function(key) % self.get_capacity()

        if self._buckets[index].length() > 0:
            cur = self._buckets[index].contains(key)
            if cur:
                for i in range(self._buckets[index].length()):
                    if key == cur.key:
                        return cur.value
                    else:
                        cur = cur.next


    def contains_key(self, key: str) -> bool:
        """
        method returns True if the given key is in the hash map, otherwise it returns False
        """
        index = self._hash_function(key) % self.get_capacity()
        if self._buckets[index].length() != 0:
            if self._buckets[index].contains(key):
                return True
        return False

    def remove(self, key: str) -> None:
        """
        method removes the given key and its associated value from the hash map
        """
        index = self._hash_function(key) % self.get_capacity()
        if self._buckets[index].length() > 0:
            for key_val in self._buckets[index]:
                if key == key_val.key:
                    self._buckets[index].remove(key)
                    self._size -= 1
                    return


    def get_keys_and_values(self) -> DynamicArray:
        """
        method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash ma
        """

        newArr = DynamicArray()
        for i in range(self._buckets.length()):
            if self._buckets[i].length() > 0:
                for node in self._buckets.get_at_index(i):
                    newArr.append((node.key, node.value))
        return newArr





def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    return a tuple containing a dynamic array comprising the mode and an integer that represents the highest frequency
    """

    map = HashMap(da.length())
    maxKey = DynamicArray()
    maxVal = 1
    for i in range(da.length()):
        if map.contains_key(da[i]):
            val = map.get(da[i])
            val += 1
            map.put(da[i], val)
            if max(val, maxVal) >= maxVal:
                if maxVal < val:
                    maxVal = val
        else:
            map.put(da[i], 1)

    maxKeyVal = map.get_keys_and_values()
    for i in range(maxKeyVal.length()):
        if maxKeyVal.get_at_index(i)[1] == maxVal:
            maxKey.append(maxKeyVal.get_at_index(i)[0])


    return maxKey, maxVal


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":


    """print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())"""

    """print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())"""

    """ print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))"""

    """print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))"""

    """print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")"""

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        #["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        #["one", "two", "three", "four", "five"],
        #["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"],
        #['-66', '192', '192', '192', '564', '564', '-96', '791', '995', '-228'],
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
