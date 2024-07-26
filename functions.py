# Selection of useful functions

from typing import Any


def write_to_json(data: Any, json_file: str) -> None:
    """Write Data to JSON File

    The content of the JSON is completely deleted and replaced by the new content written into the file

    Args:
        data: preferably structured data such as lists or dictionaries to be stored in a JSON file
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
        json_file (name.json): Name of a json file stored in working directory

    Returns:
        _type_: content of the JSON file as list or dictionary
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
        # Keys: The keys of this dictionary are the Future objects returned by executor.submit(func, date).
        # values:  indices (idx) of the elements in the data list, provided by enumerate(data)
        futures = {executor.submit(func, date): idx for idx, date in enumerate(data)}
        # futures = [executor.submit(func, date) for date in data]

        # Create empty list with length equal to length of data
        results = [None] * len(data)

        # for each result retrieve the corresponding index.
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

    Returns:
        float: execution time of the function in seconds.
    """
    from timeit import timeit

    setup_code = f"from {source} import {algorithm}"
    stmt = f"{algorithm}({data})"
    execution_time = timeit(stmt, setup=setup_code, number=1)
    return execution_time


def speed_compare_algorithms(
    data: list, algorithm_1: str, algorithm_2: str, source_1: str, source_2: str
) -> list[tuple] | None:
    """Compare speed of algorithms

    Let different algorithms run on the same set of data.
    Return the time for executing the algorithms for said data in a list of tuples.

    Args:
        data (list): A list of data points, which are arguments of both functions.
        algorithm1 (str): Name of functions/alogorithms performing taskon data.
        algorithm2 (str): ""
        source1, source2 (str): Name of module containing algorithm1 or algorithm2, respectively.

    Returns:
        list[tuple] | None: List of tuples containing:
        (datum, execution time for algorithm1, execution time for algorithm2)
    """
    return_list = list()
    for datum in data:
        al1_time = measure_time(source_1, algorithm_1, datum)
        al2_time = measure_time(source_2, algorithm_2, datum)
        result = (datum, al1_time, al2_time)
        return_list.append(result)

    return return_list


if __name__ == "__main__":
    data_list = list(range(15))
    answer = speed_compare_algorithms(
        data_list, "square1", "square2", "square", "square"
    )

    print(answer)
