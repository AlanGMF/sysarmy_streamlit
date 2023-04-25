FIBO_ORDER = [
    "<1",
    "1 - 2)",
    "2 - 3)",
    "3 - 5)",
    "5 - 8)",
    "8 - 13)",
    "13 - 21)",
    "+21",
]

COMPANY_SIZE = [
    "1 (solamente yo)",
    "De 2 a 10 personas",
    "De 11 a 50  personas",
    "De 51 a 100 personas",
    "De 101 a 200 personas",
    "De 201 a 500 personas",
    "De 501 a 1000 personas",
    "De 1001 a 2000 personas",
    "De 2001 a 5000 personas",
    "De 5001 a 10000 personas",
    "Más de 10000 personas",
]

ORDER_0_10 = [
    "•0",
    "•1",
    "•2",
    "•3",
    "•4",
    "•5",
    "•6",
    "•7",
    "•8",
    "•9",
    "•10",
]


ORDER_1_4 = [
    "•1",
    "•2",
    "•3",
    "•4",
]

ORDER_5 = [
    "•0",
    "•1",
    "•2",
    "•3",
    "•4",
    "•5",
]

ORDER_1_3 = [
    "No",
    "Uno",
    "Dos",
    "Tres",
    "Más de tres",
]


def get_order(unordered_list: list) -> list:
    """
    This function takes a list of strings containing values with format <50k, 50k-100k, 750k-1m, and 1m+. The function returns a new list with the same elements
    but sorted from the smallest value to the biggest.

    :param unordered_list: The original list of strings with unsorted values.
    :type unordered_list: list
    :return: A new list with the same elements but sorted from the smallest value to the biggest.
    :rtype: list
    """
    position_value = {}
    modified_dict = {}

    # placed the values inside a dictionary
    for position, value in enumerate(unordered_list):
        if type(value) == float:
            position_value[position] = "0"
            continue
        position_value[position] = value

    # get the numbers from the strings
    for key, value in position_value.items():
        modified_dict[key] = int(
            value.split()[0]
            .translate(str.maketrans("", "", "+<_:.%,"))
            .replace("k", "000")
            .replace("mill", "000000")
        )

    # sorts the numbers, saving them together with the position
    sorted_items = sorted(modified_dict.items(), key=lambda x: x[1])

    # scroll through the tuples in the sorted_items list,
    #  call the original values, stored in the position_values dictionary,
    #  using the position in the dictionary.
    return [
        position_value[tuples_values[0]]
        for position, tuples_values in enumerate(sorted_items)
    ]
