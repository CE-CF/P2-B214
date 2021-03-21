import threading

# --------------------
# Credit: jfs
# Link: https://stackoverflow.com/a/16368571
# Description:
# Decorator for executing the same function at a set interval
# --------------------
def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True  # stop if the program exits
            t.start()
            return stopped

        return wrapper

    return decorator
