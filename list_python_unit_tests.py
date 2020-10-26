import sys


def format_output(input):
    output = ""
    lines = input.split("\n")
    for num, line in enumerate(lines):
        print(num)
        if line != "":
            filename = line.split(":")[0]
            rest_of_line = line.split(":")[1]
            if "__" in rest_of_line:
                gwt_parts = rest_of_line.split("__")
                if len(gwt_parts) == 3:
                    rest_of_line = (
                        f"{gwt_parts[0]:<40}| {gwt_parts[1]:<40}| {gwt_parts[2]}"
                    )
            output = output + f"{filename:<50}| {rest_of_line}\n"

    return output


def main():
    pass


if __name__ == "__main__":
    filename = sys.argv[1]
    grep_text = ""
    with open(filename, "r") as file:
        grep_text = file.read()
    print(f"Read: {filename}")
    print(grep_text)

    formatted = format_output(grep_text)
    print(formatted)

