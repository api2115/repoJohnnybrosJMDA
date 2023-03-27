import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
)

cur = mydb.cursor()
cur.execute("USE classicmodels")

sql_stmt = f"SELECT * FROM orders"

cur.execute(sql_stmt)
response = cur.fetchall()

#Lista ze wszystkimi komentarzami
comment_list = [sublist[5] for sublist in response if sublist[5] is not None]
#Lista rekordów z tabeli orders z komentarzami
with_comment_list = [sublist for sublist in response if sublist[5] is not None]
#Lista rekordów z tabeli orders bez komentarza
without_comment_list = [sublist for sublist in response if sublist[5] is None]

print(f"Liczba komentarzy do dostaw: {len(comment_list)}")
print(f"Liczba dostaw bez komentarzy: {len(response)-len(comment_list)}")

#Podzielenie listy z komentarzami na liste z pojedyńczymi komentarzami
word_list=[word for string in comment_list for word in string.split()]
print(f"Liczba wyrazów w komentarzach: {len(word_list)}\n")

#Lista zawierająca anulowane zamówienia z komentarzami
not_shipped_list_with_comment = [(order[3], order[1], order[5]) for order in with_comment_list if order[3] is None and order[4]!='In Process']
#Lista zwierająca tuple z czasem potrzebnym na zrealizowanie zamówienia oraz komentarz do danego zamówienia
with_comment_time_list = [((order[3]-order[1]).days, order[5]) for order in with_comment_list if order[3] is not None]

#Lista zawierająca anulowane zamówienia bez komentarza
not_shipped_list_without_comment = [(order[3], order[1], order[5]) for order in without_comment_list if order[3] is None and order[4]!='In Process']
#Lista zawierająca tuple z czasem potrzebnym na zrealizowanie zamówienia oraz None
without_comment_time_list = [((order[3]-order[1]).days, order[5]) for order in without_comment_list if order[3] is not None]

#Średnie czasy potrzebne na zrealizowanie zamówień
avg_time_with_comment = sum(sublist[0] for sublist in with_comment_time_list) / len(with_comment_time_list)
avg_time_without_comment = sum(sublist[0] for sublist in without_comment_time_list) / len(without_comment_time_list)

print(f"Średni czas dostawy dla zamówień z komentarzami: {round(avg_time_with_comment,2)}"
      f", liczba zamówień niedostarczonych z komentarzami: {len(not_shipped_list_with_comment)}")
print(f"Średni czas dostawy dla zamówień bez komentarza: {round(avg_time_without_comment,2)}"
      f", liczba zamówień niedostarczonych bez komentarza: {len(not_shipped_list_without_comment)}")


cur.close()
mydb.close()
