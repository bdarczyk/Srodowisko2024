def get_transformer(operation):
    samogloski = "aeiouAEIOU"
    if operation == "duplicate":
        return lambda word, n: word * n
    if operation == "alternate":
        return lambda word, n: "".join(
            c.upper() if (i % n == 0) else c for i, c in enumerate(word)
        )
    if operation == "reverse":
        return lambda word: word[::-1]
    if operation == "every_nth":
        return lambda word, n: "".join(word[i] for i in range(0, len(word), n))

    if operation == "vowels_to_upper":
        return lambda word: "".join(
            c.upper() if c in samogloski else c for c in word
        )
def transform_word(word, operation, n=1):
    transformer = get_transformer(operation)
    if operation in {"duplicate", "alternate", "every_nth"}:
        return transformer(word, n)
    return transformer(word)

def main():
    word = input().strip()
    operation = input().strip()

    if operation in {"duplicate", "alternate", "every_nth"}:
        n = int(input().strip())
        result = transform_word(word, operation, n)
    else:
        result = transform_word(word, operation)

    print(result)


if __name__ == "__main__":
    main()
