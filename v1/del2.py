import atexit
import signal
import sys
import time
class MyClass:
    def __init__(self):
        print("Object created")

    def __del__(self):
        print("gone")

    def cleanup(self):
        print("Object deleted")

def exit_handler(signum, frame):
    print(f"Received signal {signum}. Exiting gracefully.")
    sys.exit(0)


def main():
   
    # Register exit signals
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    try:
        # Your main code here
        my_object = MyClass()
        time.sleep(500)
    except Exception as e:
        print(f"Exception: {e}")

    finally:
        if 'my_object' in locals():
            del my_object
        print("Object deleted")



if __name__ == "__main__":
    main()
