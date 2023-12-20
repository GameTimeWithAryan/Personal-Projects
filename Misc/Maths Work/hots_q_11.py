from fractions import Fraction

"""
General form = ax^2 + bx + c
Polynomial p(x) = a * (x-(p+1)/p) * (x-p/(p-1))

Find (a+b+c)^2
"""


def get_coef(a, p):
    zero1 = Fraction((p + 1), p)
    zero2 = Fraction(p, (p - 1))

    b = a * -1 * (zero1 + zero2)
    c = a * zero1 * zero2
    return a, b, c


def get_answer_from_coef(a, b, c):
    return (a + b + c) ** 2


def get_expected_answer(a, p):
    return Fraction(a ** 2, (p * (p - 1)) ** 2)


def main():
    for a in range(1, 11):
        for p in range(2, 11):
            answer_from_coef = get_answer_from_coef(*get_coef(a, p))
            expected_answer = get_expected_answer(a, p)

            print(f"{a=}, {p=}")
            print(f"Coef: {answer_from_coef} | Expected: {expected_answer}")

            if answer_from_coef != expected_answer:
                print("CHECK ME")


if __name__ == "__main__":
    main()
