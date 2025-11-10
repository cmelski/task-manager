# config.py
class Config:
    ENV = "production"
    BASE_URL = "https://task-manager-6pqf.onrender.com/"

class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    BASE_URL = "http://127.0.0.1:5002"


class TestingConfig(Config):
    ENV = "testing"
    DEBUG = True
    BASE_URL = "http://127.0.0.1:5002"
