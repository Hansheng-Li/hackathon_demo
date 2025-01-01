from django.test import TestCase

# Create your tests here.
import redis

r = redis.Redis(host='127.0.0.1', port=6379)
r.ping()
print("Connected to Redis!")
