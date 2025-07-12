

from typing import Any, Iterable, Sized, Callable


def parallel_sweep(group_assertion: Callable[[int, Iterable], Any], input_iterable: Sized, number_of_threads: int = 2) -> None:
    iterations: int = len(input_iterable)
    iterations_by_thread: int = iterations // number_of_threads

    # elements by thread.
    split_iterations: list[Iterable] = [input_iterable[iterations_by_thread * i: iterations_by_thread * (i + 1)] for i in range(number_of_threads - 1)]

    # last iteration.
    split_iterations.append(input_iterable[(number_of_threads - 1) * iterations_by_thread:])
    print(split_iterations)

    def thread_task(group_index: int, sliced_iterable: Iterable) -> Any:
        return group_assertion(group_index, sliced_iterable)

    from threading import Thread
    thread_pool: list[Thread] = list()

    # creating the threads
    for i, group in enumerate(split_iterations):
        thread_pool.append(Thread(args=(i, group), daemon=True, target=thread_task))

    # starting the threads
    for thread in thread_pool:
        thread.start()

    # sync barrier
    for thread in thread_pool:
        thread.join()

    return None


def process(x: float) -> float:
    return x * 2


def invert_process(x: float) -> float:
    return x / 2


if __name__ == "__main__":

    def group_assertion(group_index: int, slice: Iterable) -> None:
        from random import random
        from time import sleep

        for element in slice:
            element = float(element)
            assert element == invert_process(process(element))
            sleep(random())

        print(f"Group {group_index} is over")
        return None

    # parallel_sweep(assertion, range(101), number_of_threads=2)

    from time import perf_counter
    L: Iterable = range(1, 25)

    before: float = perf_counter()
    parallel_sweep(group_assertion, L, number_of_threads=12)
    after: float = perf_counter()

    elapsed: float = after - before
    print(f"Parallel: {elapsed} [s]")

    before = perf_counter()
    group_assertion(0, L)
    after = perf_counter()
    elapsed = after - before

    print(f"Sequential: {elapsed} [s]")

