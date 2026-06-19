import sys
from calculator import *

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
    "health":health
}

def main():
    exit_val =  1
    try:   
        func_name = sys.argv[1]
        
        if (func_name != "health" and len(sys.argv) != 4) or (func_name == "health" and len(sys.argv) != 2) :
            raise InvalidArgumentsCount(
                "Usage: python main.py <function> <num1> <num2>"
            )

        if func_name not in function_def:
            raise FunctionNotFound(
                f"Function '{func_name}' not found"
            )
        if(func_name != "health"):
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
    