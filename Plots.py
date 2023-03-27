import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
)

cur = mydb.cursor()
cur.execute("USE classicmodels")

sql_stmt = f"SELECT * FROM payments"

cur.execute(sql_stmt)
response = cur.fetchall()
#Lista ze słownikami zawierającymi przedzial czasowy oraz sumę wpływów danego miesiąca
data_amount=[]
#Lista ze słownikami zawierającymi przedzial czasowy oraz liczbę dokonanych zamówień w danym miesiącu
data_times=[]

#Pętla dodająca do obu list słowniki z ich danymi
for i in response:
    time_frame=pd.Period(f"{i[2].year}-{i[2].month}")
    try:
        #Jeśli dany przedział występuje już w liście dodaje do niego wpływ z
        #danego zamówienia lub +1 do liczby zamówień w danym miesiącu
        index = next(index for (index, dictionary) in enumerate(data_amount) if dictionary.get('period') == time_frame)
        data_amount[index]["amount"]+=i[3]
        data_times[index]["times"]+=1
    except StopIteration:
        #Jeśli iteracja się skończy dodaje nowy słownik do list
        data_amount.append({"period":time_frame,"amount":i[3]})
        data_times.append({"period":time_frame,"times":1})

#Sortuje obie listy
my_list_sorted_amount = sorted(data_amount, key=lambda x: x['period'])
my_list_sorted_times = sorted(data_times, key=lambda x: x['period'])

#Parametry dla wykresów
x_labels = [d['period'].strftime('%b %Y') for d in my_list_sorted_amount]
y_values = [float(d['amount']) for d in my_list_sorted_amount]

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(x_labels, y_values)

plt.title('Suma pieniędzy, która wpłynęła w danym miesiącu')
plt.xlabel('Miesiąc')
plt.ylabel('Kwota')

plt.setp(ax.xaxis.get_majorticklabels(), rotation=-55, ha="left", rotation_mode="anchor")
plt.tight_layout()
plt.show()

x_labels = [d['period'].strftime('%b %Y') for d in my_list_sorted_times]
y_values = [float(d['times']) for d in my_list_sorted_times]

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(x_labels, y_values)

plt.title('Liczba dokonanych zamówień w danym miesiącu')
plt.xlabel('Miesiąc')
plt.ylabel('Liczba')

plt.setp(ax.xaxis.get_majorticklabels(), rotation=-55, ha="left", rotation_mode="anchor")
plt.tight_layout()
plt.show()

cur.close()
mydb.close()
