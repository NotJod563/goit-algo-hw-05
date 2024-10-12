import timeit

# Алгоритм Кнута-Морріса-Пратта (КМП)
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1

        if j == M:
            return i - j
        elif i < N and pattern[j] != main_string[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# Алгоритм Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)
    base = 256 
    modulus = 101  

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# Алгоритм Боєра-Мура
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1

# Вимірювання часу виконання для кожного алгоритму
def measure_time(func, text, pattern):
    return timeit.timeit(lambda: func(text, pattern), number=100)

def determine_fastest(results):
    fastest_algo = min(results, key=results.get)
    fastest_time = results[fastest_algo]
    return fastest_algo, fastest_time

# Завантаження текстів
with open("text-1.txt", "r", encoding="windows-1251") as f:
    text1 = f.read()

with open("text-2.txt", "r", encoding="utf-8") as f:
    text2 = f.read()

# Підрядки для пошуку: реальні фрагменти з тексту
existing_substring_text1 = text1[80:100]  # Вибір існуючого підрядка з тексту 1
existing_substring_text2 = text2[100:120]  # Вибір існуючого підрядка з тексту 2
non_existing_substring = "nonexistent_substring"  # Підрядок, що не існує в жодному тексті

# Вимірювання часу виконання для першого тексту
print(f"Текст 1: Підрядок існує ('{existing_substring_text1}')")
results_text1_exist = {
    "KMP": measure_time(kmp_search, text1, existing_substring_text1),
    "Rabin-Karp": measure_time(rabin_karp_search, text1, existing_substring_text1),
    "Boyer-Moore": measure_time(boyer_moore_search, text1, existing_substring_text1)
}
for algo, time in results_text1_exist.items():
    print(f"{algo}: {time:.8f} секунд")

fastest_algo, fastest_time = determine_fastest(results_text1_exist)
print(f"Найшвидший для тексту 1 (існуючий підрядок): {fastest_algo}, {fastest_time:.8f} секунд\n")

print(f"Текст 1: Підрядок не існує ('{non_existing_substring}')")
results_text1_non_exist = {
    "KMP": measure_time(kmp_search, text1, non_existing_substring),
    "Rabin-Karp": measure_time(rabin_karp_search, text1, non_existing_substring),
    "Boyer-Moore": measure_time(boyer_moore_search, text1, non_existing_substring)
}
for algo, time in results_text1_non_exist.items():
    print(f"{algo}: {time:.8f} секунд")

fastest_algo, fastest_time = determine_fastest(results_text1_non_exist)
print(f"Найшвидший для тексту 1 (неіснуючий підрядок): {fastest_algo}, {fastest_time:.8f} секунд\n")

# Вимірювання часу виконання для другого тексту
print(f"Текст 2: Підрядок існує ('{existing_substring_text2}')")
results_text2_exist = {
    "KMP": measure_time(kmp_search, text2, existing_substring_text2),
    "Rabin-Karp": measure_time(rabin_karp_search, text2, existing_substring_text2),
    "Boyer-Moore": measure_time(boyer_moore_search, text2, existing_substring_text2)
}
for algo, time in results_text2_exist.items():
    print(f"{algo}: {time:.8f} секунд")

fastest_algo, fastest_time = determine_fastest(results_text2_exist)
print(f"Найшвидший для тексту 2 (існуючий підрядок): {fastest_algo}, {fastest_time:.8f} секунд\n")

print(f"Текст 2: Підрядок не існує ('{non_existing_substring}')")
results_text2_non_exist = {
    "KMP": measure_time(kmp_search, text2, non_existing_substring),
    "Rabin-Karp": measure_time(rabin_karp_search, text2, non_existing_substring),
    "Boyer-Moore": measure_time(boyer_moore_search, text2, non_existing_substring)
}
for algo, time in results_text2_non_exist.items():
    print(f"{algo}: {time:.8f} секунд")

fastest_algo, fastest_time = determine_fastest(results_text2_non_exist)
print(f"Найшвидший для тексту 2 (неіснуючий підрядок): {fastest_algo}, {fastest_time:.8f} секунд\n")
