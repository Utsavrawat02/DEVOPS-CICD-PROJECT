import sys

from calculator import add, subtract, multiply, divide


def health():
    print("ok")


class InvalidArgumentsCount(Exception):
    pass


class FunctionNotFound(Exception):
    pass


function_def = {
    "add": add,
    "mul": multiply,
    "sub": subtract,
    "div": divide,
    "health": health
}


def main():
    exit_val = 1
    try:
        func_name = sys.argv[1]

        is_health = func_name == "health"
        arg_count = len(sys.argv)
        invalid_args = (
            (not is_health and arg_count != 4)
            or (is_health and arg_count != 2)
        )
        if invalid_args:
            raise InvalidArgumentsCount(
                "Usage: python main.py <function> <num1> <num2>"
            )

        if func_name not in function_def:
            raise FunctionNotFound(
                f"Function '{func_name}' not found"
            )

        if func_name != "health":
            a = float(sys.argv[2])
            b = float(sys.argv[3])
            result = function_def[func_name](a, b)
            print("result: ", result)
        else:
            health()
        exit_val = 0

    except FunctionNotFound as e:
        print(e)

    except InvalidArgumentsCount as e:
        print(e)

    except ValueError:
        print("Arguments must be numeric.")

    except ZeroDivisionError:
        print("Cannot divide by zero.")

    return exit_val


if __name__ == "__main__":
    sys.exit(main())
    