# Selection of useful functions

from typing import Any


def write_to_json(data: Any, json_file: str) -> None:
    """Write Data to JSON File

    The content of the JSON is completely deleted and replaced by the new content written into the file

    Args:
        data: preferably structured data such as lists or dictionaries to be stored in a JSON file
    """
    import json

    with open(json_file, "w") as file:
        contents = json.dumps(data, indent=2)
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
    import json

    with open(json_file, "r") as file:
        contents = file.read()
        data = json.loads(contents)
    return data


def parallel_process(func, data: list) ->list | None:
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
    if num_cpus != None:
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



if __name__ == "__main__":
    
    def square(x):
        return x*x
    numbers = list(range(20))
    
    result = parallel_process(square, numbers)
    
    print(result)