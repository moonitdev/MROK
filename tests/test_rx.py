import asyncio
import rx
import rx.operators as ops
from rx.scheduler.eventloop import AsyncIOScheduler
from random import *

async def foo():
    await asyncio.sleep(1)
    r = randint(1, 100)
    if r%2 == 1:
        return 'odd'
    else:
        return 'even'
    # return 42

def intervalRead(rate, fun) -> rx.Observable:
    loop = asyncio.get_event_loop()
    return rx.interval(rate).pipe(
        ops.map(lambda i: rx.from_future(loop.create_task(fun()))),
        ops.merge_all()
    )

async def main(loop):
    obs = intervalRead(5, foo)
    obs.subscribe(
        # on_next=lambda item: print(item),
        # on_next=on_next_test(item),
        on_next=lambda item: on_next_test(item),
        scheduler=AsyncIOScheduler(loop)
    )

def on_next_test(item):
    if item == 'odd':
        print('Oh Ye!!, {} number'.format(item))
    else:
        print('Oh, No~~ {} number'.format(item))

loop = asyncio.get_event_loop()
loop.create_task(main(loop))
loop.run_forever()

# from rx import create

# def hello_rx(observer, scheduler):
#     observer.on_next("Hello")
#     observer.on_next("RxPy")
#     observer.on_next("WAWAWA!!")
#     observer.on_completed()
 
 
# def str_double(_str: str):
#     print("{} {}".format(_str, _str))
 
 
# source = create(hello_rx)
# source.subscribe(lambda x: print(x))
# source.subscribe(str_double)


# from rx import of

# source = of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")

# source.subscribe(
#     on_next = lambda i: print("Received {0}".format(i)),
#     on_error = lambda e: print("Error Occurred: {0}".format(e)),
#     on_completed = lambda: print("Done!"),
# )



# from rx import of

# source = of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")

# source.subscribe(lambda value: print("Received {0}".format(value)))




