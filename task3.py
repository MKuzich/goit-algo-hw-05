import timeit

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
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1 

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

def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

def test_search_algorithms(file1, file2, pattern1, pattern2):
    
    article1 = read_file(file1)
    bm_a1 = timeit.timeit(lambda: boyer_moore_search(article1, pattern1), number=1)
    kpm_a1 = timeit.timeit(lambda: kmp_search(article1, pattern1), number=1)
    rk_a1 = timeit.timeit(lambda: rabin_karp_search(article1, pattern1), number=1)
    
    article2 = read_file(file2)
    bm_a2 = timeit.timeit(lambda: boyer_moore_search(article2, pattern2), number=1)
    kpm_a2 = timeit.timeit(lambda: kmp_search(article2, pattern2), number=1)
    rk_a2 = timeit.timeit(lambda: rabin_karp_search(article2, pattern2), number=1)

    print('Стаття 1:')
    print('Boyer-Moore:', bm_a1)
    print('KMP:', kpm_a1)
    print('Rabin-Karp:', rk_a1)
    print('\nСтаття 2:')
    print('Boyer-Moore:', bm_a2)
    print('KMP:', kpm_a2)
    print('Rabin-Karp:', rk_a2)
    print('\nУ цілому:')
    print('Boyer-Moore:', bm_a1 + bm_a2)
    print('KMP:', kpm_a1 + kpm_a2)
    print('Rabin-Karp:', rk_a1 + rk_a2)

print('Тестування алгоритмів пошуку з пошуком існуючого паттерну: ')
test_search_algorithms('article1.txt', 'article2.txt', 'готових бібліотек', 'розглянутих структур')
print('\nТестування алгоритмів пошуку з пошуком неіснуючого паттерну: ')
test_search_algorithms('article1.txt', 'article2.txt', 'мав', 'мав')

