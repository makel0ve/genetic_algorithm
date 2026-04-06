from genetic import genetic_algorithm


def read_matrix(filepath: str) -> list[list[int]]:
    """Читает матрицу смежности из файла."""

    with open(filepath, "r") as f:
        matrix = [list(map(int, line.split())) for line in f if line.strip()]

    if not matrix:
        raise ValueError("Файл пуст или не содержит данных")

    size = len(matrix)
    for i, row in enumerate(matrix):
        if len(row) != size:
            raise ValueError(f"Строка {i} содержит {len(row)} элементов, ожидалось {size}")

    return matrix


def input_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Запрашивает целое число с валидацией диапазона."""

    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Значение должно быть не меньше {min_val}")
                continue

            if max_val is not None and value > max_val:
                print(f"Значение должно быть не больше {max_val}")
                continue

            return value
        
        except ValueError:
            print("Введите целое число")


def input_float(prompt: str, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Запрашивает дробное число с валидацией диапазона."""
    
    while True:
        try:
            value = float(input(prompt))
            if not (min_val <= value <= max_val):
                print(f"Значение должно быть в диапазоне {min_val} — {max_val}")
                continue

            return value
        
        except ValueError:
            print("Введите число")


def main():
    filepath = input("Путь до файла с матрицей смежности: ").strip().replace('"', '')
    matrix = read_matrix(filepath)
    n = len(matrix)

    print(f"Загружена матрица {n}x{n}\n")

    population_size = input_int(
        "Размер популяции (рекомендуется 50–200): ", min_val=2
    )
    max_no_improvement = input_int(
        "Поколений без улучшений для остановки (рекомендуется 200–1000): ", min_val=1
    )
    mutation_rate = input_float(
        "Вероятность мутации (рекомендуется 0.1–0.5): ", min_val=0.0, max_val=1.0
    )
    start_node = input_int(
        f"Начальная вершина маршрута (0–{n - 1}): ", min_val=0, max_val=n - 1
    )

    solution, distance, generations = genetic_algorithm(
        matrix, population_size, max_no_improvement, mutation_rate, start_node
    )

    route = solution + [solution[0]]

    print(f"\nКратчайший маршрут: {' → '.join(map(str, route))}")
    print(f"Длина маршрута: {round(distance, 2)}")
    print(f"Поколений до сходимости: {generations}")


if __name__ == "__main__":
    main()