# write celery tasks here
from celery import shared_task
from time import sleep

@shared_task
def send_token_message(phone_no, token_number):
    message = f"Hello! Your hospital token number is {token_number}. Please wait for your turn. We’ll notify you when it’s close. Thank you!"
    # Simulated SMS log
    print(f"[DEV MODE] Simulated SMS to {phone_no}: {message}")
    