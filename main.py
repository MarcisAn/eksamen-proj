import sqlite3

# Izveido savienojumu ar datubāzi
con = sqlite3.connect("noma.db")
cur = con.cursor()

#sagatavo Mailjet API epastu sūtīšanai
#from mailjet_rest import Client
import os
#api_key = os.environ['MJ_APIKEY_PUBLIC']
#api_secret = os.environ['MJ_APIKEY_PRIVATE']
#mailjet = Client(auth=(api_key, api_secret), version='v3.1')

prompt = """
Veicamā darbība:
Beigt darbu - 1
Reģistrēt pasūtījumu - 2
Pievienot noliktavai jaunu produkta tipu - 3
"""

def get_product_types():
    res = cur.execute("SELECT * FROM produktu_tipi")
    products = []
    for product in res.fetchall():
        products.append("{} {} {}".format(product[2],product[3],product[1]))
    return products

def register_new_product_type():
    name = input("Produkta nosaukums: ")
    maker = input("Produkta ražotājs: ")
    prod_type = input("Produkta tips: ")
    amount = int(input("Daudzums noliktavā: "))
    cost = float(input("Produkta nomas maksa dienā: "))
    data = (prod_type, maker, name, cost, amount)
    cur.execute("INSERT INTO produktu_tipi VALUES (null, ?, ?, ?, ?, ?)", data)
    con.commit()



def register_event():
    title = input("Pasākuma nosaukums: ")
    email = input("Pasūtītāja e-pasta adrese: ")
    data = (title, email)
    cur.execute("INSERT INTO pasakumi VALUES (null, ?, ?)", data)
    con.commit()
    events = cur.execute("SELECT id FROM pasakumi")
    pasakuma_id = events.lastrowid
    
    for index, product in enumerate(get_product_types()):
        print(index + 1, "-", product)
    print()
    amount_of_product_types = int(input("Dažādo produktu tipu skaits: "))
    for _ in range(amount_of_product_types):
        product_type = input("Pieprasītais produkta tips: ")
        product_amount = input("Pieprasītais produkta daudzums: ")
        
        check = cur.execute("SELECT daudzums_noliktava FROM produktu_tipi WHERE id={}".format(int(product_type)))
        availible_amount = check.fetchone()[0]

        if int(product_amount) > availible_amount:
            send_email(False, email)
            return False
        print(availible_amount)

        data = (pasakuma_id, product_type, product_amount)
        cur.execute("INSERT INTO pasutijumi VALUES (null, ?, ?, ?)", data)
        con.commit()
    send_email(True, email)


def send_email(is_possible, recipient_addr):
    if is_possible:
        result = "apstiprināts"
    else:
        result = "noraidīts"
        
    data = {
    'Messages': [
				{
					"From": {
							"Email": "pazinojumi@tehnikas_noma.lv",
							"Name": "Tehnikas noma"
					},
					"To": [
							{
									"Email": recipient_addr,
									"Name": recipient_addr
							}
					],
					"Subject": "Informācija par tehnikas nomu pasākumam",
					"TextPart": "Jūsu pasūtījums ir {}.".format(result),
				}
		]
    }
    print(data)
    #mailjet.send.create(data=data)

def main():
    while True:
        action = input(prompt)     
        if action == "1":
            exit()
        elif action == "2":
            is_possible = register_event()
        elif action == "3":
            register_new_product_type()
            

if __name__ == "__main__":
    main()