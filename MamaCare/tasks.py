# tasks.py
from datetime import timedelta, date
from celery import shared_task
from .models import Immunization
from .utils import get_parent_phones  # Import the utility function

# If you have Celery configured, this task will be scheduled to run periodically
@shared_task
def send_immunization_notifications():
    """
    This task sends notifications to the mother and father 2 days before the immunization date.
    """
    today = date.today()
    # Find immunizations where the next visit is scheduled in 2 days
    immunizations = Immunization.objects.filter(bcg_next_visit=today + timedelta(days=2))

    for immunization in immunizations:
        # Get the phone numbers of the parents
        mother_phone, father_phone = get_parent_phones(immunization)

        # Here, call your notification function to send the message
        send_notification(mother_phone, father_phone, immunization)

def send_notification(mother_phone, father_phone, immunization):
    """
    This function is responsible for sending SMS notifications to the parents.
    You can integrate with any SMS gateway API here (like Twilio or other).
    """
    message = f"Reminder: Your child's immunization for {immunization} is due soon!"
    
    # Example: Send message to the mother's phone number
    if mother_phone:
        # Example: Call an external service like Twilio to send SMS
        print(f"Sending SMS to mother: {mother_phone} - {message}")
    
    # Example: Send message to the father's phone number
    if father_phone:
        # Example: Call an external service like Twilio to send SMS
        print(f"Sending SMS to father: {father_phone} - {message}")
