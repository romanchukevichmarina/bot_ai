import telebot
import database

bot = telebot.TeleBot("7254201623:AAE7qAm8FDmOEo0nqlEj3wdGIRRtwFs3gvg", threaded=False)
# try:
#     database.create_db()
# except:
#     print("couldn/'t create database")

# try:
#     database.create_tables()
# except:
#     print("couldn/'t create tables")
database.create_db()
database.create_tables()