import sys


def format_output(input):
    output = ""
    lines = input.split("\n")
    includes_filename = True
    if lines[0].startswith("class "):
        includes_filename = False
    for num, line in enumerate(lines):
        if line[-1] == ":":
            line = line[:-1]
        if line[-1] == "(":
            line = line[:-1]
        print(f"{num} : {line}")
        if line != "":
            filename = ""
            rest_of_line = line
            if includes_filename:
                print("\tincludes filename")
                includes_filename = True
                filename = line.split(":")[0]
                print(f"\t{filename}")
                rest_of_line = line.split(":")[1].replace("(self)", "")
            if "__" in rest_of_line:
                print("\tincludes __")
                gwt_parts = rest_of_line.replace("(self)", "").split("__")
                if len(gwt_parts) == 3:
                    rest_of_line = (
                        f"{gwt_parts[0]:<40}| {gwt_parts[1]:<40}| {gwt_parts[2]}"
                    )
            if includes_filename:
                output = output + f"{filename:<50}| {rest_of_line}\n"
            else:
                output = output + f"{rest_of_line}\n"

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

