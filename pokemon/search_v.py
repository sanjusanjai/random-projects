import re

DATABASE_PATH = "database.txt"


def search_pokemon(word):
    with open(DATABASE_PATH) as db:
        return re.findall(f"{re.sub('_', '.', word)}", db.read(), re.M)


if __name__ == "__main__":
    testcases = ["_i_a_hu", "__n_mo__", "N___ra__"]
    for case in testcases:
        print(search_pokemon(case))
