from rx import create

def hello_rx(observer, scheduler):
    observer.on_next("Hello")
    observer.on_next("RxPy")
    observer.on_next("WAWAWA!!")
    observer.on_completed()
 
 
def str_double(_str: str):
    print("{} {}".format(_str, _str))
 
 
source = create(hello_rx)
source.subscribe(lambda x: print(x))
source.subscribe(str_double)



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








# from rx import Observable, Observer


# def push_hello_world(observer):
#     observer.on_next("hello")
#     observer.on_next("world")
#     #observer.on_error("error")
#     observer.on_completed()


# class PrintObserver(Observer):
#     def on_next(self, value):
#         print("Received {0}".format(value))

#     def on_completed(self):
#         print("Done!")

#     def on_error(self, error):
#         print("Error Occurred: {0}".format(error))


# if __name__ == '__main__':
#     source = Observable.create(push_hello_world)
#     source.subscribe(PrintObserver())
