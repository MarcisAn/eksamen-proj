
#sagatavo Mailjet API epastu sūtīšanai
import os
api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

class EmailSender:
    def __init__(self, email):
        self.email = email
    def send_email(self, is_possible):
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
									"Email": self.email,
									"Name": self.email
							}
					],
					"Subject": "Informācija par tehnikas nomu pasākumam",
					"TextPart": "Jūsu pasūtījums ir {}.".format(result),
				}
		    ]
        }
        mailjet.send.create(data=data)
        
        
class EmailSendTest(EmailSender):
    def test_email(self):
        data = {
        'Messages': [
				{
					"From": {
							"Email": "pazinojumi@tehnikas_noma.lv",
							"Name": "Tehnikas noma"
					},
					"To": [
							{
									"Email": "tests@tehnikas_noma.lv",
									"Name": "Testēšanas e-pasta adresāts"
							}
					],
					"Subject": "E-pasta sūtīšanas tests",
					"TextPart": "E-pasts nosūtīts veiksmīgi.",
				}
		    ]
        }
        mailjet.send.create(data=data)