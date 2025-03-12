import os
import streamlit as st
st.set_page_config(page_title="Personal Library Manager", page_icon="📚")
st.markdown("""
  <style>
    .main-container {
        max-width: 80%;
        margin: auto;
        transition: max-width 0.1s ease-in-out;
    }
    .sidebar-hidden .main-container {
        max-width: 100%;
    }
    .css-1d391kg { 
        padding: 2rem !important;
    }
    /* Background*/
    .stApp {
        background: linear-gradient(to right, #d1a7e0, #6a2c91);  
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(to top, #6a2c91, #a072b4);  
        color: white !important;
    }
    .stButton>button {
        background-color: #6a2c91; 
        color: white !important;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #a072b4;  
    }
    .stButton>button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(106, 44, 145, 0.5);
    }
  </style>
""", unsafe_allow_html=True)
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
    st.subheader("📚 Add a New Book")
    title = st.text_input("Enter the book title:")
    author = st.text_input("Enter the author:")
    year = st.number_input("Enter the publication year:", min_value=1)
    genre = st.text_input("Enter the genre:")
    read_status = st.radio("Have you read this book?", ('Yes', 'No'))
    if st.button("Add Book 📥"):
        if title and author and genre:
            books.append({
                'title': title,
                'author': author,
                'year': year,
                'genre': genre,
                'read': read_status == 'Yes'
            })
            save_library('library.txt', books)  
            st.success(f"✅ Book '{title}' added successfully!")
        else:
            st.error("❗ Please fill in all fields.")
def remove_book(books):
    st.subheader("❌ Remove a Book")
    title = st.text_input("Enter the title of the book to remove:")
    if st.button("Remove Book 🗑️"):
        for book in books:
            if book['title'].lower() == title.lower():
                books.remove(book)
                save_library('library.txt', books)  # Save immediately after removing
                st.success(f"✅ Book '{title}' removed successfully!")
                return
        st.error("❗ Book not found.")
def search_books(books):
    st.subheader("🔍 Search for a Book")
    search_by = st.selectbox("Search by", ["Title", "Author"])
    matches = []
    if search_by == "Title":
        search_title = st.text_input("Enter the title:")
        if st.button("Search 🔎"):
            matches = [book for book in books if search_title.lower() in book['title'].lower()]
    else:
        search_author = st.text_input("Enter the author:")
        if st.button("Search 🔎"):
            matches = [book for book in books if search_author.lower() in book['author'].lower()]
    if matches:
        st.write("📚 Matching Books:")
        for i, book in enumerate(matches, 1):
            read_status = "✅ Read" if book['read'] else "❌ Unread"
            st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    else:
        st.write("❗ No matching books found.")
def display_books(books):
    st.subheader("📖 Your Library")
    if not books:
        st.write("❗ No books in the library.")
    else:
        for i, book in enumerate(books, 1):
            read_status = "✅ Read" if book['read'] else "❌ Unread"
            st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
def display_statistics(books):
    st.subheader("📊 Library Statistics")
    total_books = len(books)
    read_books = len([book for book in books if book['read']])
    read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
    st.write(f"📝 Total books: {total_books}")
    st.write(f"📖 Percentage read: {read_percentage:.2f}%")
def main():
    library_filename = 'library.txt'
    books = load_library(library_filename)
    st.title("📚 Personal Library Manager")
    # Sidebar
    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Exit"]
    choice = st.sidebar.radio("🔧 Select an option", menu)
    if choice == "Add a Book":
        add_book(books)
    elif choice == "Remove a Book":
        remove_book(books)
    elif choice == "Search for a Book":
        search_books(books)
    elif choice == "Display All Books":
        display_books(books)
    elif choice == "Display Statistics":
        display_statistics(books)
    elif choice == "Exit":
        save_library(library_filename, books)
        st.success("📂 Library saved to file. Goodbye! 👋")
    st.markdown("""
    <p style="font-size:14px; text-align:center;">Developed by Aleeza❤️</p>
    """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()
