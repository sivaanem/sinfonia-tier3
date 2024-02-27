from locust import HttpUser, task, constant_throughput


class HelloWorldUser(HttpUser):
    # Maximum request load per second
    wait_time = constant_throughput(100)

    @task
    def hello_world(self):
        self.client.get('http://localhost/livez')
