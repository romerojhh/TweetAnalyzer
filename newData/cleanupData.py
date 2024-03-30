import csv

def main():
    print
    a = extractCol("newData/DonaldTrump.csv", [1,5], "Donald Trump", [])
    b = extractCol("newData/JoeBiden.csv", [0,3], "Joe Biden", a)
    writeData("tweetAggregated", b)


def extractCol(filename: str, columns_to_keep: list[int], author_name: str, data: list):
    count = 0
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            # index 2 isRetweet for donald trump
            if author_name == 'Donald Trump' and row[2] == 't':
                continue
            else:
                new_row = [row[i] for i in columns_to_keep]
                new_row.insert(0, author_name)
                data.append(new_row)
                count += 1

            if count >= 1000:
                break
    return data

def writeData(output_file_name: str, data: list):
    # Open a new CSV file for writing
    with open(f'newData/{output_file_name}.csv', 'w') as file:
        writer = csv.writer(file)
        header = ["tweet_author", 'tweet', "like_count"]
        writer.writerow(header)
        # Write the data rows
        writer.writerows(data)

main()