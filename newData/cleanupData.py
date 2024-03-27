import csv

def main():
    print
    openFile("./newData/DonaldTrump.csv")

def openFile(filename: str):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            isValid = False
            for col in row:
                if (row[2] == 'f' and row[1] == col):
                    print(row[0], col, sep=',', end='')
                    isValid = True

            if isValid:       
                print('\n')
            count += 1
            if count >= 10:
                break
main()