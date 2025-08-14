import asyncio

async def main(task,wait):
    print(f"{task} started")
    await asyncio.sleep(wait)
    print(f"{task} completed after {wait} seconds")

async def run_tasks():
    await asyncio.gather(
        main("1", 4),
        main("2", 3),
        main("3", 2),
        main("4", 1)
    )

if __name__ == "__main__":
    asyncio.run(run_tasks())
