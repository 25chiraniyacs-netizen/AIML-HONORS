from functools import wraps


def trace_task(label):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            border = "-" * 28
            print(border)
            print(f"Task   : {label}")
            print(f"Inputs : {args}")
            res = fn(*args, **kwargs)
            print(f"Result : {res}")
            print(border)
            return res

        return wrapper

    return decorator


@trace_task("Addition")
def sum_values(x, y):
    return x + y


if __name__ == "__main__":
    sum_values(4, 3)
