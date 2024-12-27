from celery import shared_task

@shared_task
def trial_task(x, y):
    return x + y

