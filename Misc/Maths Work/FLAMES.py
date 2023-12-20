from collections import Counter
from pprint import pprint

from matplotlib.pyplot import plot, show

NAME_1 = "ABC"  # Write in capital, without space e.g. "ARYAN"
NAME_2 = "BCDE"

FLAMES: dict = {letter: index for index, letter in enumerate("FLAMES")}


def count_non_matching_letter(name1: str, name2: str) -> int:
    output = Counter()
    name1 = Counter(name1)
    name2 = Counter(name2)

    for letter in name1:
        letters_left_count = abs(name1[letter] - name2[letter])
        output[letter] = letters_left_count

    for letter in name2:
        letters_left_count = abs(name1[letter] - name2[letter])
        output[letter] = letters_left_count

    total_count = 0
    for letter in output:
        total_count += output[letter]

    return total_count


def find_flames_letter(letter_count: int) -> int:
    flames_list: list = list(FLAMES.keys())
    for i in range(5):
        flame_letter_index = (letter_count - 1) % len(flames_list)
        flames_list.pop(flame_letter_index)

    return FLAMES[flames_list[0]]


def generate_plot_data() -> tuple[list, list]:
    dataset_size = 100
    letter_count_list = list()
    flames_letter_indexes_list = list()
    for letter_count in range(dataset_size):
        flame_index = find_flames_letter(letter_count)
        letter_count_list.append(letter_count)
        flames_letter_indexes_list.append(flame_index)

    return letter_count_list, flames_letter_indexes_list


def plot_graph(x_axis_points, y_axis_points):
    plot(x_axis_points, y_axis_points, "o")
    show()


def main():
    x_axis_data, y_axis_data = generate_plot_data()
    pprint({x_data: y_data for x_data, y_data in zip(x_axis_data, y_axis_data)})
    plot_graph(x_axis_data, y_axis_data)


if __name__ == "__main__":
    main()
