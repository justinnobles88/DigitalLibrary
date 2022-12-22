
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, Contact, contact_schema, contacts_schema, book_schema, books_schema
from forms import UserLoginForm
api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Hidey': 'Hoe'}

@api.route('/contacts', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Contact(name, email, phone_number, address, user_token = user_token )

    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    contact = Contact.query.get(id) 
    contact.name = request.json['name']
    contact.email = request.json['email']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    cover = request.json['cover']
    pages = request.json['pages']
    user_token = current_user_token.token

    book = Book(title,author,cover,pages,user_token = user_token)

    db.session.add(book)
    db.session.commit()


    response = book_schema.dump(book)
    return jsonify(response) 


# RETRIEVE ALL CARS ENDPOINT
@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    # set owner equal to 
    owner = current_user_token.token
    # .all to get everthing
    books = Book.query.filter_by(user_token = owner).all()
    response = book_schema.dump(books)
    return jsonify(response)


# RETRIEVE ONE CAR BY ID
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)


# UPDATE CAR ENDPOINT
@api.route('/books/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    # Grabbing the book from the table - instance is denoted by the id
    book = Book.query.get(id)  #Getting a book instance

    # Then grab each individual attribute and update zero or more of the following values
    book.title = request.json['title']
    book.author = request.json['author']
    book.cover = request.json['cover']
    book.pages = request.json['pages']
    book.user_token = current_user_token.token

    # Then commit it to the database
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


# DELETE CAR ENDPOINT
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)