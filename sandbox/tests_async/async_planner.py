"""Async planner for execution of functions"""
import datetime as dt
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio


async def dummy_task():
    """Dummy task to print in console the current time"""
    print(dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    await asyncio.sleep(1)


async def greet():
    """Dummy function to test async scheduler"""
    print("Hello from async scheduler!")
    await asyncio.sleep(1)


async def main():
    """Execution of main program for schedule"""

    # creacion de una instancia del async scheduler
    async_sched = AsyncIOScheduler()
    # añadir el job al scheduler
    async_sched.add_job(dummy_task, "interval", seconds=5, id="dummy_task")
    async_sched.add_job(greet, "cron", second="*/10", id="greet_task")
    # Iniciar el scheduler
    async_sched.start()

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Scheduler stopped by user.")

if __name__ == "__main__":
    try:
        # se arranca el event loop principal
        # esto solo creara un event loop
        # el asyncio.run() solo se debe de usar una vez en el programa
        # si no se crearian varios eventloop adicionales
        # el utilizalo dentro de un while no funciona bien para mantenera teras vivas
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")
