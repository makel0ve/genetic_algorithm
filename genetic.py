import random


def initialize_population(
    matrix: list[list[int]], population_size: int, start_node: int
) -> list[list[int]]:
    """Создаёт начальную популяцию случайных маршрутов."""

    nodes = [i for i in range(len(matrix)) if i != start_node]

    population = []
    for _ in range(population_size):
        individual = [start_node] + random.sample(nodes, len(nodes))
        population.append(individual)

    return population


def calculate_fitness(individual: list[int], matrix: list[list[int]]) -> float:
    """
    Оценивает качество маршрута.

    Чем короче маршрут, тем выше fitness (обратная величина расстояния).
    """

    total_distance = sum(
        matrix[individual[i]][individual[i + 1]]
        for i in range(len(individual) - 1)
    )
    total_distance += matrix[individual[-1]][individual[0]]

    return 1 / total_distance


def select_parents(
    population: list[list[int]], fitness_values: list[float]
) -> tuple[list[int], list[int]]:
    """Выбирает двух родителей методом рулеточного отбора."""

    total_fitness = sum(fitness_values)
    probabilities = [f / total_fitness for f in fitness_values]
    parent1, parent2 = random.choices(population, weights=probabilities, k=2)

    return parent1, parent2


def crossover(
    parent1: list[int], parent2: list[int]
) -> tuple[list[int], list[int]]:
    """
    Упорядоченный кроссовер (OX).

    Копирует сегмент из одного родителя и заполняет
    оставшиеся позиции генами другого родителя.
    """

    size = len(parent1)
    start, end = sorted(random.sample(range(1, size), 2))

    child1 = [None] * size
    child2 = [None] * size

    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    child1 = _fill_child(child1, parent2)
    child2 = _fill_child(child2, parent1)

    return child1, child2


def _fill_child(child: list[int | None], parent: list[int]) -> list[int]:
    """
    Заполняет пустые позиции ребёнка генами из родителя.

    Использует set для быстрой проверки (O(1) вместо O(n)).
    """

    existing = set(gene for gene in child if gene is not None)

    fill_values = [node for node in parent if node not in existing]
    fill_iter = iter(fill_values)

    return [
        gene if gene is not None else next(fill_iter)
        for gene in child
    ]


def mutate(individual: list[int], mutation_rate: float) -> list[int]:
    """Мутация инверсией — переворачивает случайный сегмент маршрута."""

    if random.random() < mutation_rate:
        start, end = sorted(random.sample(range(1, len(individual)), 2))
        individual[start:end] = reversed(individual[start:end])

    return individual


def create_new_generation(
    population: list[list[int]],
    matrix: list[list[int]],
    mutation_rate: float,
) -> list[list[int]]:
    """Создаёт новое поколение через элитизм, отбор, кроссовер и мутацию."""

    fitness_values = [calculate_fitness(ind, matrix) for ind in population]

    elite_size = max(1, int(0.1 * len(population)))
    indexed = sorted(
        zip(fitness_values, population), key=lambda x: x[0], reverse=True
    )
    new_population = [ind for _, ind in indexed[:elite_size]]

    while len(new_population) < len(population):
        parent1, parent2 = select_parents(population, fitness_values)
        child1, child2 = crossover(parent1, parent2)
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)

        new_population.append(child1)
        if len(new_population) < len(population):
            new_population.append(child2)

    return new_population


def genetic_algorithm(
    matrix: list[list[int]],
    population_size: int,
    max_no_improvement: int,
    mutation_rate: float,
    start_node: int,
) -> tuple[list[int], float, int]:
    """
    Запускает генетический алгоритм.

    Args:
        matrix: матрица смежности (расстояния между вершинами).
        population_size: размер популяции.
        max_no_improvement: число поколений без улучшений для остановки.
        mutation_rate: вероятность мутации (0.0 — 1.0).
        start_node: начальная вершина маршрута.

    Returns:
        Кортеж (лучший маршрут, длина маршрута, общее число поколений).
    """

    population = initialize_population(matrix, population_size, start_node)

    best_distance = float("inf")
    best_solution = None
    no_improvement = 0
    total_generations = 0

    while no_improvement < max_no_improvement:
        population = create_new_generation(population, matrix, mutation_rate)

        best_individual = max(
            population, key=lambda ind: calculate_fitness(ind, matrix)
        )
        distance = 1 / calculate_fitness(best_individual, matrix)

        if distance < best_distance:
            best_distance = distance
            best_solution = best_individual
            no_improvement = 0
            
        else:
            no_improvement += 1

        total_generations += 1

    effective_generations = total_generations - max_no_improvement
    return best_solution, best_distance, effective_generations