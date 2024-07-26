# Selection of useful functions

from typing import Any


def write_to_json(data: Any, json_file: str) -> None:
    """Write Data to JSON File

    The content of the JSON is completely deleted and replaced by the new content
    written into the file.

    Args:
        data (Any): preferably structured data such as lists or dictionaries
        to be stored in a JSON file.
        json_file (string): Name of the Json file as a string.
    """
    from json import dumps

    with open(json_file, "w") as file:
        contents = dumps(data, indent=2)
        file.write(contents)


def read_from_json(json_file: str) -> Any:
    """Import data from JSON file

    The content of the JSON file is completely copied and converted into a python data structure,
    which is returned by the function.

    Args:
        json_file (string): Name of a json file stored in working directory

    Returns:
        Any: content of the JSON file as python data structure
    """
    from json import loads

    with open(json_file, "r") as file:
        contents = file.read()
        data = loads(contents)
    return data


def parallel_process(func, data: list) -> list | None:
    """Use parallel processing, where a single functions processes a list of items

    Args:
        func (function): Pass the name of the function, that is to be executed in parallel
        data (list): List of items, each item is to be processed by the function.

    Returns:
        list: Return the result of processing the data with the functions as a list.
        None: Return None if an error occurs.
    """
    from concurrent.futures import ProcessPoolExecutor, as_completed
    from os import cpu_count

    # Count the number of CPUs and take them as maximum number of workers for processing
    num_cpus = cpu_count()
    if num_cpus != None and num_cpus >= 2:
        num_workers = min(len(data), num_cpus)
    else:
        print("No parallel processing possible due to lack of CPUs")
        return None

    # Perform Multitasking
    with ProcessPoolExecutor(num_workers) as executor:
        # Submit tasks to be executed with dictionary comprehension
        # Keys: objects returned by executor.submit(func, date).
        # values: indices (idx) of the elements of data
        futures = {executor.submit(func, date): idx for idx, date in enumerate(data)}

        # for each result retrieve the corresponding index.
        results = [None] * len(data)
        # return futures if possible.
        for future in as_completed(futures):
            idx = futures[future]
            # add the result at the corresponding index to the results list.
            try:
                results[idx] = future.result()
            except Exception as e:
                print(f"Error processing data at index {idx}: {e}")
    return results


def measure_time(source: str, algorithm: str, data: Any) -> float:
    """Measure time it takes for a function/algorithm to process data

    Args:
        source (str): Name of the library containing the function
        algorithm (str): Name of the function to be executed
        data (Any): datum passed to the function as argument

    Returns (float): execution time of the function in seconds.
    """
    from timeit import timeit

    setup_code = f"from {source} import {algorithm}"
    stmt = f"{algorithm}({data})"
    execution_time = timeit(stmt, setup=setup_code, number=1)
    return execution_time


def speed_compare_algorithms(
    data: list, algorithm_1: str, algorithm_2: str, source_1: str, source_2: str
) -> list[tuple]:
    """Compare speed of algorithms

    Let different algorithms run on the same set of data.
    Return the time for executing the algorithms for said data in a list of tuples.

    Args:
        data (list): A list of data points, which are arguments of both functions.
        algorithm1 (str): Name of function/algorithm performing task on data.
        algorithm2 (str): Name of second function to be compared.
        source1, source2 (str): Name of module containing algorithm1 and algorithm2, respectively.

    Returns:
        list (tuple): List of tuples, each tuple containing:
        (datum, execution time for algorithm1, execution time for algorithm2)
    """
    return_list = list()
    for datum in data:
        al1_time = measure_time(source_1, algorithm_1, datum)
        al2_time = measure_time(source_2, algorithm_2, datum)
        result = (datum, al1_time, al2_time)
        return_list.append(result)

    return return_list


def save_speed_comparison(
    speed_results: list[tuple],
    json_file: str,
    algorithm_1: str = "Algorithm 1",
    algorithm_2: str = "Algorithm 2",
) -> None:
    """Save speed  comparision to JSON-File

    Args:
        speed_results (list[tuple]): List of tuples, each tuple containing:
        (datum, execution time for algorithm1, execution time for algorithm2)
        json_file (str): Name of JSON-File for storing data
        algorithm_1 (str, optional): Name of first Algorithm. Defaults to "Algorithm 1".
        algorithm_2 (str, optional): Name of second Algorithm. Defaults to "Algorithm 2".
    """

    JSON_data = [(json_file, algorithm_1, algorithm_2), speed_results]

    write_to_json(JSON_data, json_file)

    return None

def read_speed_comparison(json_file: str) -> list[list]:
    """Read speed comparison data from JSON-file

    Args:
        json_file (str): JSON-File comprising measurement results from
        speed comparisons.

    Returns:
        list(list): list[0] = ['filenmae.json', '1. Algorithm', '2. Algorithm']
                    list[1] = list of list each comprising:
                    [datum, exec-time 1. Algorithm, exec_time 2. Algorithm]
    """
    retrieved_list = read_from_json(json_file)

    return retrieved_list

def display_speed_comparison(
    speed_results: list[tuple],
    algorithm_1: str = "Algorithm 1",
    algorithm_2: str = "Algorithm 2",
) -> None:
    """Display execution times in graph

    Retrieve data as well as execution times from two different algorithms.
    Display results in a graph.

    Args:
        speed_results (list[tuple]): List of tuples, each tuple containing:
        (datum, execution time for algorithm1, execution time for algorithm2)
        algorithm1 (str): Name of first algorithm.
        algorithm2 (str): Name of second function.
    """

    from matplotlib import pyplot as plt

    input_sizes = [result[0] for result in speed_results]
    algorithm_1_times = [result[1] for result in speed_results]
    algorithm_2_times = [result[2] for result in speed_results]

    # Plot the first curve for kilian2 algo
    plt.plot(input_sizes, algorithm_1_times, label=algorithm_1)
    # Plot the second curve for merge_sort algo
    plt.plot(input_sizes, algorithm_2_times, label=algorithm_2)

    plt.xlabel("Input Data")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time of Algorithms")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    
    result = read_speed_comparison("Square.json")
    
    print(result[0])
    print(result[1])
    
    """ data_list = list(range(10, 25))
    answer = speed_compare_algorithms(
        data_list, "square1", "square2", "square", "square"
    )

    display_speed_comparison(
        answer, algorithm_1="easy square", algorithm_2="complicated square"
    ) """

    """    save_speed_comparison(
        answer,
        "Square.json",
        algorithm_1="easy square",
        algorithm_2="complicated square",
    )
    
    
    """
    