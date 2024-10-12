import random

def generate_sorted_array(size, lower_bound, upper_bound):
    # Генеруємо випадковий масив дробових чисел
    array = [round(random.uniform(lower_bound, upper_bound), 2) for _ in range(size)]
    array.sort()  # Сортуємо масив
    return array

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if arr[mid] == target:
            return (iterations, arr[mid])  # Повертаємо кількість ітерацій та знайдене значення
        
        if arr[mid] < target:
            low = mid + 1
        else:
            upper_bound = arr[mid]
            high = mid - 1
    
    # Якщо елемент не знайдено, повертаємо upper_bound
    if upper_bound is None and low < len(arr):
        upper_bound = arr[low]
    
    return (iterations, upper_bound)

# Генеруємо відсортований масив випадкових чисел
array_size = 15 # Якщо цікаво побавитись, то можна змінити розмір масиву і подивитись як змінюється кількість ітерацій
lower_bound = 1.0
upper_bound = 10.0
sorted_array = generate_sorted_array(array_size, lower_bound, upper_bound)

# Випадкове цільове значення з діапазону
target_value = round(random.uniform(lower_bound, upper_bound), 2)

# Викликаємо двійковий пошук
result = binary_search(sorted_array, target_value)

# Виводимо результат
print(f"Відсортований масив: {sorted_array}")
print(f"Цільове значення: {target_value}")
print(f"Кількість ітерацій: {result[0]}")
print(f"Верхня межа: {result[1]}")
