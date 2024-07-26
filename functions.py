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


def parallel_process(func, data: list) ->list:
    """Use parallel processing, where a single functions processes a list of items

    Args:
        func (function): Pass the name of the function, that is to be executed in parallel
        data (list): List of items, each item is to be processed by the function.

    Returns:
        list: Return the result of processing the data with the functions as a list.
    """
    from concurrent.futures import ProcessPoolExecutor, as_completed
    from os import cpu_count
    
    # Count the number of CPUs and take them as maximum number of workers for processing
    num_cpus = cpu_count()
    num_workers = min(len(data), num_cpus)
    
    with ProcessPoolExecutor(num_workers) as executor:
        # Submit tasks to be executed
        futures = [executor.submit(func, date) for date in data]
        
        results = []
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                # Handle the exception (print, log, etc.)
                print(f"Error processing data: {e}")
    
    return results



if __name__ == "__main__":
    
    def square(x):
        return x*x
    
    my_data = list(range(20))
    
    answer = parallel_process(func=square, data=my_data)
    
    print(answer)
