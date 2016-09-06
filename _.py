import asyncio

@asyncio.coroutine
def mycor():
    print('in coroutine')
    yield from asyncio.sleep(3)

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(mycor())
)

loop.close()
print('done')