from locust import Locust
from locust import TaskSet
from locust import task


class GoogleTask(TaskSet):
    @task
    def index(self):
        self.client.get("/")


class GoogleUser(Locust):
    task_set = GoogleTask
    min_wait = 2000
    max_wait = 5000
