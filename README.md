# Price Tracker

## About

This application enables you to track the price of any product on any website.

Everything can be managed from the Django Admin interface, where you can create, edit and delete products, as well as set how often the prices should be checked for updates.

## Technologies used in the Application

- Django
- Celery
- Django Celery Beat

## Using the Application

#Todo

### 1 - Choose a Broker

First of all, you need to choose a broker to use with Celery. The application is current configured for Redis running on localhost (port 6379). If this configuration is fine for you, just start your Redis server.

If you would like to use another broker, you can change the current configuration in the Django settings.py file (very end of the file).

The current settings.py file also includes configuration for Amazon SQS. To you use this configuration, you should:

1. Uncomment the CELERY_BROKER_URL, CELERY_TASK_DEFAULT_QUEUE and CELERY_BROKER_TRANSPORT_OPTIONS variables beneath #SQS; 
2. Add your access and private keys to the CELERY_BROKER_URL variable;
3. Comment out the configuration for Redis.

To learn more about brokers, go to https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html#broker-overview.

### 2 - Install Dependencies

#Todo