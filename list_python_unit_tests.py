def format_output(input):
    output = ""
    lines = input.split("\n")
    for line in lines:
        filename = line.split(":")[0]
        rest_of_line = line.split(":")[1]
        output = output + f"{filename:<40}|{rest_of_line}\n"

    return output


def main():
    pass


if __name__ == "__main__":
    unittest.main()

