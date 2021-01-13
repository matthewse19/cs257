import argparse
import csv
import sys

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='Filter and display information about books.csv')
    parser.add_argument('-t', "--titles", default="", nargs='?', help='Phrase in title to filter by')
    parser.add_argument('-a', "--authors", default="", nargs="?", help='Phrase in author\'s name to filter by')
    parser.add_argument('-y', "--years", metavar="YEAR", nargs=2, type=int, help='Range of publication years to filter by')
    parser.add_argument('-o', "--order", default="", nargs="?", help='[title, author, year] Which category to sort by and how to display')
    parser.add_argument('-d', "--descending", action="store_true", help='Sets to descending')

    parsed_arguments = parser.parse_args()
    return parsed_arguments

def print_titles(book_list, descending):
    book_list.sort(reverse = descending, key=lambda x: x[0])
    for book in book_list:
        print(book[0])

def print_years(book_list, descending):
   	book_list.sort(reverse = descending, key=lambda x: x[1])
    for book in book_list:
        print(book[0], ",", book[1])

def print_authors(book_list, descending):
    authors_books = {}
    for book in book_list:
        if book[2] in authors_books:
            authors_books[book[2]].append(book[0])
        else:
            authors_books[book[2]] = [book[0]]

    for author in sorted(author_books.keys(), reverse = descending):
        print(author)
        for book in authors_books[author]:
            print("\t", book)
        print("\n")

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

    if arguments.order == "title":
        print_titles(books, arguments.descending)
    elif arguments.order =="year":
        print_years(books, arguments.descending)
    elif arguments.order =="author":
        print_authors(books, arguments.descending)
    elif arguments.order == "":
        if arguments.titles != "":
            print_titles(books, arguments.descending)
        elif arguments.authors != "":
            print_authors(books, arguments.descending)
        elif arguments.years != None:
            print_years(books, arguments.descending)
        else:
            print("No search argument was inputed, type books.py --help to see commands", file=sys.stderr)
    else:
        print("Inputed incorrect order parameter, must be 'title', 'author', or 'year'", file=sys.stderr)

if __name__ == '__main__':
    main()
