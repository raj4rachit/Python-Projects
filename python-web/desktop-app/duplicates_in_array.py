def findDuplicateElements(a, n):
    count = [0] * (n + 1)

    for num in a:
        count[num] += 1

    duplicates = [i for i, freq in enumerate(count) if freq > 1]

    return sorted(duplicates)


# Taking input from the user
n = int(input("Enter the length of the array: "))
input_array = []
for i in range(n):
    element = int(input(f"Enter element {i + 1}: "))
    input_array.append(element - 1)  # Decrement by 1 to use as an index

result = findDuplicateElements(input_array, n)
if result:
    print("Duplicate elements:", result)
else:
    print("No duplicate elements found. [-1]")
