class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("The email address for {user} has been updated.".format(user = self.name))

    def __repr__(self):
        return """\tUser: {name}
        Email: {email}
        Books Read: {books}\n""".format(name = self.name, email = self.email, books = len(self.books))

    def __eq__(self, other_user):
        if (self.name == other_user.name) and (self.email == other_user.email):
            return True
        else:
            return False

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        total_rating = 0
        count = 0

        for book in self.books.values():
            if not (book == None):
                total_rating += book
                count += 1

        return total_rating / count

class Book(object):
    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, number):
        self.isbn = number
        print("The ISBN of {book} has been updated.".format(book = self.title))

    def add_rating(self, rating):
        if not (rating == None):
            if rating >= 0 and rating <= 4:
                self.ratings.append(rating)
            else:
                print("Invalid Rating")

    def __eq__(self, other_book):
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        else:
            return False

    def get_average_rating(self):
        total_rating = 0

        for rating in self.ratings:
            total_rating += rating

        return total_rating / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return self.title +"\n"

class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return self.title + " by " + self.author + "\n"

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return self.title + ", a " + self.level + " manual on " + self.subject + "\n"

class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}
        self.isbns = []

    def __repr__(self):
        return """Tome Rater Users:\n{users}
        Tome Rater Books:\n{books}
        """.format(users = list(self.users.values()), books = list(self.books.keys()))

    def create_book(self, title, isbn, price):
        if isbn in self.isbns:
            print("This is not a unique ISBN.")
        else:
            self.isbns.append(isbn)
            return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price):
        if isbn in self.isbns:
            print("This is not a unique ISBN.")
        else:
            self.isbns.append(isbn)
            return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, subject, level, isbn, price):
        if isbn in self.isbns:
            print("This is not a unique ISBN.")
        else:
            self.isbns.append(isbn)
            return Non_Fiction(title, subject, level, isbn, price)

    def add_book_to_user(self, book, email, rating = None):
        if email in self.users:
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("No user with email {email}!".format(email = email))

    def add_user(self, name, email, user_books = None):
        if email in self.users:
            print("The user with email {} already exists.".format(email))
        else:
            if ("@" in email) and ((".com" in email) or (".edu" in email) or (".org" in email)):
                new_user = User(name, email)
                self.users[email] = new_user

                if not (user_books == None):
                    for book in user_books:
                        self.add_book_to_user(book, email)
            else:
                print("Not a valid email.")

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        max_value = -1
        for key, value in self.books.items():
            if value > max_value:
                max_value = value
                most_read_book = key
        return most_read_book

    def highest_rated_book(self):
        max_value = -1
        for book in self.books:
            if book.get_average_rating() > max_value:
                max_value = book.get_average_rating()
                highest_rated_book = book
        return highest_rated_book

    def most_positive_user(self):
        max_value = -1
        for user in self.users.values():
            if user.get_average_rating() > max_value:
                max_value = user.get_average_rating()
                most_positive_user = user
        return most_positive_user

    def get_n_most_read_books(self, n):
        sorted_list = sorted(self.books, key=self.books.__getitem__, reverse=True)
        n_most_read = sorted_list[:n]
        return n_most_read

    def get_n_most_prolific_reader(self, n):
        reader_dict = {}
        for key, value in self.users.items():
            reader_dict[value.name] = len(value.books)
        sorted_readers = sorted(reader_dict, key=reader_dict.__getitem__, reverse=True)
        n_most_prolific = sorted_readers[:n]
        return n_most_prolific

    def get_n_most_expensive_books(self, n):
        temp_dict = {}
        for book in self.books:
            temp_dict[book.title] = book.price
        sorted_books = sorted(temp_dict, key=temp_dict.__getitem__, reverse=True)
        n_most_expensive = sorted_books[:n]
        return n_most_expensive

    def get_worth_of_user(self, user_email):
        total_cost = 0
        for book in self.users[user_email].books:
            total_cost += book.price
        return "$" + str(total_cost)
