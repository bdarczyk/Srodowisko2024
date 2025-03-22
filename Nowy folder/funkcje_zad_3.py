def power_sum(n, p, m=1):
    if n == 0: # warunek stopu rekurencji
        return 0
    if m == 1: # jesli m = 1 sumuje liczby podniesione do p
        wartosc = n ** p
    elif n % m == 0: # obliczanie wartosci gdy n jest podzielne przez m
        wartosc = n ** p
    else:
        wartosc = 0
    #rekurencujne wywolanie dla n-1
    return wartosc + power_sum(n -1, p, m)

def main():
    n = int(input())
    p = int(input())
    m = int(input())

    result = power_sum(n, p, m)

    print(result)

if __name__ == "__main__":
    main()