import os
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def load_library(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            books = []
            for line in file:
                book_data = line.strip().split('|')
                title, author, year, genre, read = book_data
                books.append({
                    'title': title,
                    'author': author,
                    'year': int(year),
                    'genre': genre,
                    'read': read.lower() == 'true'
                })
            return books
    else:
        return []

def save_library(filename, books):
    with open(filename, 'w') as file:
        for book in books:
            file.write(f"{book['title']}|{book['author']}|{book['year']}|{book['genre']}|{book['read']}\n")

def add_book(books):
    print(Fore.CYAN + "📚 Add a New Book")
    title = input(Fore.MAGENTA + "Enter the book title: ")
    author = input(Fore.MAGENTA + "Enter the author: ")
    year = int(input(Fore.MAGENTA + "Enter the publication year: "))
    genre = input(Fore.MAGENTA + "Enter the genre: ")
    read_status = input(Fore.MAGENTA + "Have you read this book? (Yes/No): ").strip().lower()
    if title and author and genre:
        books.append({
            'title': title,
            'author': author,
            'year': year,
            'genre': genre,
            'read': read_status == 'yes'
        })
        save_library('library.txt', books)
        print(Fore.GREEN + f"✅ Book '{title}' added successfully!")
    else:
        print(Fore.RED + "❗ Please fill in all fields.")

def remove_book(books):
    print(Fore.CYAN + "❌ Remove a Book")
    title = input(Fore.MAGENTA + "Enter the title of the book to remove: ")
    for book in books:
        if book['title'].lower() == title.lower():
            books.remove(book)
            save_library('library.txt', books)
            print(Fore.GREEN + f"✅ Book '{title}' removed successfully!")
            return
    print(Fore.RED + "❗ Book not found.")

def search_books(books):
    print(Fore.CYAN + "🔍 Search for a Book")
    search_by = input(Fore.MAGENTA + "Search by (Title/Author): ").strip().lower()
    matches = []
    if search_by == "title":
        search_title = input(Fore.MAGENTA + "Enter the title: ")
        matches = [book for book in books if search_title.lower() in book['title'].lower()]
    elif search_by == "author":
        search_author = input(Fore.MAGENTA + "Enter the author: ")
        matches = [book for book in books if search_author.lower() in book['author'].lower()]
    else:
        print(Fore.RED + "❗ Invalid search criteria.")
        return
    if matches:
        print(Fore.GREEN + "📚 Matching Books:")
        for i, book in enumerate(matches, 1):
            read_status = "✅ Read" if book['read'] else "❌ Unread"
            print(Fore.YELLOW + f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    else:
        print(Fore.RED + "❗ No matching books found.")

def display_books(books):
    print(Fore.CYAN + "📖 Your Library")
    if not books:
        print(Fore.RED + "❗ No books in the library.")
    else:
        for i, book in enumerate(books, 1):
            read_status = "✅ Read" if book['read'] else "❌ Unread"
            print(Fore.YELLOW + f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")

def display_statistics(books):
    print(Fore.CYAN + "📊 Library Statistics")
    total_books = len(books)
    read_books = len([book for book in books if book['read']])
    read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
    print(Fore.GREEN + f"📝 Total books: {total_books}")
    print(Fore.GREEN + f"📖 Percentage read: {read_percentage:.2f}%")

def main():
    library_filename = 'library.txt'
    books = load_library(library_filename)

    while True:
        print(Fore.YELLOW + "\n📚 Personal Library Manager")
        print(Fore.GREEN + "1. Add a Book")
        print(Fore.GREEN + "2. Remove a Book")
        print(Fore.GREEN + "3. Search for a Book")
        print(Fore.GREEN + "4. Display All Books")
        print(Fore.GREEN + "5. Display Statistics")
        print(Fore.RED + "6. Exit")

        choice = input(Fore.CYAN + "Select an option (1-6): ").strip()

        if choice == '1':
            add_book(books)
        elif choice == '2':
            remove_book(books)
        elif choice == '3':
            search_books(books)
        elif choice == '4':
            display_books(books)
        elif choice == '5':
            display_statistics(books)
        elif choice == '6':
            save_library(library_filename, books)
            print(Fore.GREEN + "📂 Library saved to file. Goodbye! 👋")
            break
        else:
            print(Fore.RED + "❗ Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
