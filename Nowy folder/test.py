from functools import reduce

def get_operation(operation_name) :
    if operation_name == "square":
        return lambda numbers: map(lambda x: x**2, numbers)
    if operation_name == "cube":
        return lambda numbers: map(lambda x: x**3, numbers)
    if operation_name == "absolute":
        return lambda numbers: map(lambda x: abs(x), numbers)
    if operation_name == "negative":
        return lambda numbers: map(lambda x: -x, numbers)
    if operation_name == "even_only":
        return lambda numbers: filter(lambda x: x % 2 == 0, numbers)
    if operation_name == "odd_only":
        return lambda numbers: filter(lambda x: x % 2 != 0, numbers)
    if operation_name == "positive_only":
        return lambda numbers: filter(lambda x: x > 0, numbers)
    if operation_name == "sum":
        return lambda numbers: reduce(lambda x, y: x + y, numbers)
    if operation_name == "product":
        return lambda numbers: reduce(lambda x, y: x * y, numbers)
    else:
        return lambda numbers: numbers

def list_operations(numbers, operation):
    return list(operation(numbers))

def main():
    numbers = list(map(int, input().split()))
    operation_name = input().strip()

    operation = get_operation(operation_name)
    result = list_operations(numbers, operation)

    print (" ".join(map(str, result)))
if __name__ == "__main__":
    main()