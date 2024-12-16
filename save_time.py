import time
import pandas as pd
import asyncio

async def measure_execution_time(func, *args, **kwargs):
    """Measure and save the execution time of a given function, supporting async functions."""
    start_time = time.time()
    
    # Check if the function is async
    if asyncio.iscoroutinefunction(func):
        result = await func(*args, **kwargs)  # Await if the function is async
    else:
        result = func(*args, **kwargs)  # Run normally if it's not async

    end_time = time.time()
    execution_time = end_time - start_time

    # Prepare data to save to Excel
    data = {
        "Execution Time (s)": [execution_time],
        "Function": [func.__name__]
    }
    df = pd.DataFrame(data)

    # Save execution time to an Excel file
    file_path = r'C:\Users\Pegasus\Documents\Pegasus_steam_SUM\Evaluation\execution_times.xlsx'
    try:
        # Append to the file if it exists, else create it
        existing_df = pd.read_excel(file_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        updated_df = df

    updated_df.to_excel(file_path, index=False)
    print(f"Execution time saved to {file_path}")

    return result

