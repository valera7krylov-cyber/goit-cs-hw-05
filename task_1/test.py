import asyncio


async def task():
    print("Start")
    await asyncio.sleep(3)
    print("Finish")


async def main():
    await asyncio.gather(
        task(),
        task(),
        task()
    )


asyncio.run(main())