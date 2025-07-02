# write celery tasks here
from celery import shared_task
from time import sleep
@shared_task
def add_numbers(x, y):
    print("++++++++++++++++++++++++++++++++++++++++++")
    print("BEFORE SLEEPING")
    sleep(10)
    print("___________________________________________")
    print("AFTER SLEEPING")
    return x + y