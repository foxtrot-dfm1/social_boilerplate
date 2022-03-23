from django.conf import settings
from quickemailverification import Client

EMAIL_VALIDATOR = settings.EMAIL_VALIDATOR

def validate_email(email):
    if not EMAIL_VALIDATOR.get('validate'):
        return True
    client = Client(EMAIL_VALIDATOR.get('api-key'))
    quickemailverification = client.quickemailverification()
    response = quickemailverification.verify(email)
    
    if response.body.get('result') == "invalid":
        return False

    return True   
    

