"""Testing ascyn functions.

This script demonstrates the use of asynchronous functions in Python.
The main call execute the main async function
Inside the main async function is created three tasks with diferrent durations
and a call back to know when tasks finished or eve if there is some error.
"""
import asyncio


async def function1_10():
    """Function to print greeting."""

    print("Task 1 started")
    await asyncio.sleep(10)
    return "Task 1 completed"


async def function2_3():
    """Funciton to last during 10 seconds."""

    print("Task 2 started")
    await asyncio.sleep(3)
    return "Task 2 completed"


async def function3_8():
    """Function to last during 8 seconds."""

    print("Task 3 started")
    await asyncio.sleep(8)
    return "Task 3 completed"


async def function_error():
    """Function to raise an error."""

    print("Task 4 started")
    raise ValueError("This is an error from function_error Task4.")


def done_task_callback(task):
    """Callback for a task is finished, report it"""
    try:
        result = task.result()
        print(result)
    except Exception as e:
        print(f"Task raised an exception: {e}")


async def async_main():
    """Main function to run async tasks."""

    print("Starting async tasks")

    task1 = asyncio.create_task(function1_10())
    task2 = asyncio.create_task(function2_3())
    task3 = asyncio.create_task(function3_8())
    task4 = asyncio.create_task(function_error())
    task1.add_done_callback(done_task_callback)
    task2.add_done_callback(done_task_callback)
    task3.add_done_callback(done_task_callback)
    task4.add_done_callback(done_task_callback)
    await asyncio.gather(task1, task2, task3, task4, return_exceptions=True)
    print("All tasks completed")


if __name__ == "__main__":
    # executte main async functions
    asyncio.run(async_main())
