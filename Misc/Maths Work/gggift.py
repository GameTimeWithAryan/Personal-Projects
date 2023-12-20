def get_name(name: str):
    return int("".join([str(ord(char) - 96) for char in name.lower()]))


def factorize(number: int, divisor_list: list):
    # 7211472114 [7] -> 1030210302 * 7 + 0
    # 7211472114 [7, 14] -> (73586450 * 14 + 2) * 7 + 0
    template = "{q} * {n} + {r}"
    dividend = number
    output_list = []
    divisor_list.reverse()

    for divisor in divisor_list:
        quotient = dividend // divisor
        remainder = dividend % divisor
        output = template.format(q=quotient, n=divisor, r=remainder)
        dividend = quotient
        output_list.append(output)
    return output_list


def get_equation(equation_list):
    equation_list.reverse()
    for index, output in enumerate(equation_list):
        if index == len(equation_list) - 1:
            return equation_list[len(equation_list) - 1]
        value = str(eval(output))
        equation_list[index + 1] = equation_list[index + 1].replace(value, f"({output})")
