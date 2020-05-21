import random

from locust import HttpUser, task, between


URLS = (
    '/m/FOO',
    '/universityambassadors',
    '/os/FOO',
    '/desktop/FOO',
    '/android/FOO',
    '/developer/FOO',
    '/10',
    '/independent/FOO',
    '/hello/FOO',
    '/hello/FOO?name=dude',
    '/personal/',
    '/choose/',
    '/switch/',
    '/enterprise/',
    '/containers/',
    '/pdx/',
    '/pair/',
    '/any/other/url',
    '/',
)


class WebsiteUser(HttpUser):
    wait_time = between(2, 9)

    @task(10)
    def get_redirect(self):
        self.client.get(random.choice(URLS), name='/redirect')

    @task(1)
    def health_check(self):
        self.client.get('/healthz/')
