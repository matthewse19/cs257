import argparse
import csv

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='Filter and display information about books.csv')
    parser.add_argument('-t', "--titles", default="", nargs='?', help='Phrase in title to filter by')
    parser.add_argument('-a', "--authors", default="", nargs="?", help='Phrase in author\'s name to filter by')
    parser.add_argument('-y', "--years", nargs=2, type=int, help='Range of publication years to filter by')
    #parser.add_argument('--test', '-t', action="store_true", help='test text')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def main():
    arguments = get_parsed_arguments()
    print(arguments)

    books = []
    with open('books.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not(arguments.titles.lower() in row[0].lower()):
                continue
            if not(arguments.authors.lower() in row[2].lower()):
                continue
            if arguments.years != None:
                min_year = min(arguments.years[0], arguments.years[1])
                max_year = max(arguments.years[0], arguments.years[1])
                book_year = int(row[1])
                if book_year > max_year or book_year < min_year:
                    continue
            books.append(row)

    print_authors(books)

def print_titles(book_list):
    for book in book_list:
        print(book[0])

def print_years(book_list):
    for book in book_list:
        print(book[0], ",", book[1])

def print_authors(book_list):
    authors_books = {}
    for book in book_list:
        if book[2] in authors_books:
            authors_books[book[2]].append(book[0])
        else:
            authors_books[book[2]] = [book[0]]
    print(authors_books)
if __name__ == '__main__':
    main()
