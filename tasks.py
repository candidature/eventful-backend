from celery import Celery

app = Celery('tasks', broker='amqp://localhost//', backend='db+sqlite:///results-db')

@app.task
def reverse(string):
    return string[::-1]
