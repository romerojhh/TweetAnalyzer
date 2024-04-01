def clean_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    cleaned_lines = []

    for line in lines:
        if (not line.isspace()):
            cleaned_lines.append(line)

    # for line in lines:
    #     s = re.sub(r'[\n]+', '\n', line)
    #     cleaned_line = line.replace('\n\n', '\n')
    #     cleaned_lines.append(cleaned_line)

    with open(output_file, 'w') as f:
        f.writelines(cleaned_lines)

def main():
    clean_file('./data/JoeBidenCopy.txt', "./data/JoeBidenCopyCleaned.txt")

main()