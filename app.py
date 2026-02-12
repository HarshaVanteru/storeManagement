import asyncio

async def task1():
    print("Start Task 1")
    await asyncio.sleep(3)
    print("End Task 1")

async def task2():
    print("Start Task 2")
    await asyncio.sleep(2)
    print("End Task 2")

async def main():
    print('before async')
    await asyncio.gather(task1(), task2())
    print('after async')

asyncio.run(main())
