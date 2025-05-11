# users/utils.py
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_sms_via_provider(phone_number, message):
    """
    Twilio аркылуу SMS жөнөтүү функциясы.
    """
    if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_PHONE_NUMBER]):
        error_message = "Twilio орнотуулары (ACCOUNT_SID, AUTH_TOKEN, PHONE_NUMBER) толук эмес."
        print(f"SMS ЖӨНӨТҮҮДӨ КАТА: {error_message}")
        return False, error_message

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    try:
        twilio_message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print(f"Twilio SMS SID: {twilio_message.sid}, Status: {twilio_message.status}")
        
        if twilio_message.status in ['sent', 'queued', 'delivered']:
             return True, f"SMS {phone_number} номерине ийгиликтүү жөнөтүлдү (же кезекке турду)."
        else:
            error_detail = f"Статус: {twilio_message.status}."
            if twilio_message.error_message:
                error_detail += f" Ката: {twilio_message.error_message} (Код: {twilio_message.error_code})"
            print(f"SMS жөнөтүүдө күтүлбөгөн статус: {error_detail}")
            return False, f"SMS жөнөтүүдө күтүлбөгөн статус: {error_detail}"

    except TwilioRestException as e:
        error_message = f"Twilio API катасы: {str(e)}"
        print(f"SMS ЖӨНӨТҮҮДӨ КАТА: {error_message}")
        return False, error_message
    except Exception as e:
        error_message = f"SMS жөнөтүүдө күтүлбөгөн ката: {str(e)}"
        print(f"SMS ЖӨНӨТҮҮДӨ КАТА: {error_message}")
        return False, error_message