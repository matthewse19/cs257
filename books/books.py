#Riaz Kelly, Matthew Smith-Erb
#Revised by Riaz Kelly and Matthew Smith-Erb
import argparse
import csv
import sys

def get_parsed_arguments():
    '''create and return a parser object to get arguments'''
    parser = argparse.ArgumentParser(description='Filter and display information about books.csv')
    parser.add_argument('-t', "--titles", default="", nargs='?',
        help='Phrase in title to filter by')
    parser.add_argument('-a', "--authors", default="", nargs="?",
        help='Phrase in author\'s name to filter by')
    parser.add_argument('-s', "--start_year", default = 0, nargs="?", type=int,
        help='Lowest year to filter by')
    parser.add_argument('-e', "--end_year", default = 2021, nargs="?", type=int,
        help='Highest year to filter by')
    parser.add_argument('-o', "--order", default="title", nargs="?",
        help='[title, author, year] Which category to sort by and how to display, defaults to title')
    parser.add_argument('-d', "--descending", action="store_true",
        help='Order results in descending order instead of ascending')

    parsed_arguments = parser.parse_args()
    return parsed_arguments

def print_titles(book_list, descending):
    '''print only the titles of books alphabetically'''
    title_index = 0
    book_list.sort(reverse = descending, key=lambda x: x[title_index])
    for book in book_list:
        title = book[title_index]
        print(title)

def print_titles_years(book_list, descending):
    '''print the titles of books followed by their year chronologically'''
    title_index = 0
    year_index = 1
    book_list.sort(reverse = descending, key=lambda x: x[year_index])
    for book in book_list:
        title = book[title_index]
        year = book[year_index]
        print(title, year)

def print_authors(book_list, descending):
    '''print the name of authors alphabetically followed by the books they wrote matching the filters'''
    title_index = 0
    author_index = 2
    #dict where keys are author's names and values are a list of strings of books they wrote
    authors_books = {}
    #adds to authors_books according to which books fit the filter
    for book in book_list:
        title = book[title_index]
        author = book[author_index]
        if author in authors_books:
            authors_books[author].append(title)
        else:
            authors_books[author] = [title]

    #sorts the authors_books based on authors' names
    for author in sorted(authors_books.keys(), reverse = descending):
        print(author)
        for book in authors_books[author]:
            print("\t", book)
        print("\n")

def filter_books(reader, title_filter, author_filter, start_year, end_year):
    '''returns a list of books from the reader object that matches the filters'''
    books = []

    for row in reader:
        book_title = row[0].lower()
        book_author = row[2].lower()
        book_year = int(row[1])

        if not(title_filter in book_title):
            continue
        if not(author_filter in book_author):
            continue
        if book_year > end_year or book_year < start_year:
            continue

        books.append(row)

    return books

def call_correct_print(order_type, descending, books):
    '''calls one of three print functions based on order_type, defaults to print_titles()'''
    if len(books) == 0:
        print("No books matched your filters")
    elif order_type == "title":
        print_titles(books, descending)
    elif order_type =="year":
        print_titles_years(books, descending)
    elif order_type =="author":
        print_authors(books, descending)
    else:
        print("Inputed incorrect order parameter, must be 'title', 'author', or 'year'", file=sys.stderr)

def main():
    arguments = get_parsed_arguments()
    #list of books that will fit the filters
    books = []

    with open('books.csv', newline='') as f:
        reader = csv.reader(f)
        title_filter = arguments.titles.lower()
        author_filter = arguments.authors.lower()
        start_year = arguments.start_year
        end_year = arguments.end_year

        books = filter_books(reader, title_filter, author_filter, start_year, end_year)

    order_type = arguments.order
    descending = arguments.descending
    call_correct_print(order_type, descending, books)

if __name__ == '__main__':
    main()
