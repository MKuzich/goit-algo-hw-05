import random

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    count = 0
    mid = 0
    closest_high = high

    while low <= high:
        count += 1
        mid = (high + low) // 2

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
            closest_high = mid
        else:
            return count, arr[mid]
    return count, arr[closest_high] 

arr = []
search = random.randint(1, 100)
for i in range(1, 101):
    arr.append(i +  round(random.uniform(0, 0.9), 1))

print('Дано масив: ', arr)
print('Шукаємо число: ', search)
print('Кількість порівнянь та ближнє число: ', binary_search(arr, search))