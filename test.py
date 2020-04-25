import asyncio


async def task(name):
    print(f'{name} задача началась')
    await asyncio.sleep(1)
    print(f'{name} задача завершилась')


async def main():
    await asyncio.gather(
        task('Первая'),
        task('Вторая'),
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())