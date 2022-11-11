# Price Tracker

## About

This application enables you to track the price of any product on any website.

Everything can be managed from the Django Admin interface, where you can create, edit and delete products, as well as set how often the prices should be checked for updates.

## Technologies used in the Application

- Django
- Celery
- Django Celery Beat
- Beautiful Soup

## Using the Application

You can start tracking your first product by following five simple steps.

### 1 - Choose a Broker

First of all, you need to choose a broker to use with Celery. The application is currently configured for Redis running on localhost (port 6379). If this configuration is fine for you, just start your Redis server.

If you would like to use another broker, you can change the current configuration at the end of the Django settings.py file.

The current settings.py file also includes configuration for Amazon SQS. To use this configuration, you should:

1. Uncomment the CELERY_BROKER_URL, CELERY_TASK_DEFAULT_QUEUE and CELERY_BROKER_TRANSPORT_OPTIONS variables below #SQS; 
2. Add your access and private keys to the CELERY_BROKER_URL variable;
3. Comment out the configuration for Redis.

To learn more about brokers, go to https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html#broker-overview.

### 2 - Install Dependencies

The project includes a requirements.txt file. To install the dependencies, run the command: 
```
pip install -r requirements.txt
```
Note that these are the necessary dependencies for using the application with Redis. If you choose to use another broker, you will most likely have to install extra dependencies.

For example, to use the application with Amazon SQS, you can install the extra dependecies by running:
```
pip install celery[sqs]
```

### 3 - Create a Super User

You will manage all the products you are tracking from the Django Admin. In order to log into the Django Admin, you need to create a super user. To do that, run the command:
```
python manage.py createsuperuser
```
To finish creating your super user, enter a username, email and password.

### 4 - Start Django, Celery Worker and Celery Beat

To start the servers, run the following commands in different terminal instances.

1. Django
```
python manage.py runserver
```
2. Celery Worker
```
celery -A application worker -l info
```
3. Celery Beat
```
celery -A application beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### 5 - Track your First Product

Once the servers are running, go to http://127.0.0.1:8000/admin/. We can log into the admin by using the username and password of the user we created in the step 3.

After logging in, we can see three sections: Authentication and Authorization, Periodic Tasks and Scraper. We need to worry only about the last one.

Let's take a look at a simple example of how we can track a real product.

I am going to track an acoustic guitar on the website Muztorg: https://www.muztorg.ru/produ%D1%81t/A088397.

In the Scraper section, there are three models: Prices, Products and Websites.

I have to add a website for Muztorg and a product for the guitar I want to track.

The reason why we add this information separately is because usually we want to track many products on the same website. This way, we need to add the information about the website only once.

So, first I will click on Websites, then, in the top right corner of the screen, I will click on ADD WEBSITE.

A website needs two pieces of information: name and path.

For name you can choose any name you would like (max of 64 characters).

Path is where you will tell the application how to find the price of the product on the website page (using JSON.) Usually it's located in a **p** or **span** tag.

In most cases, you will be able to track a product by specifying the **tag** and **id** or **class** attributes.

For example, the price of the guitar I want to track is located in the following tag:
```
<p class="price-value-gtm">44000</p>
```
So the path can be:
```
{
    "tag": "p", 
    "class": "price-value-gtm"
}
```
In this case, this path would work. Sometimes, however, there may be more than one tag on the page using the same class, which can cause some problems. In this scenario, you can use the child attribute. 

For example, the above **p tag** is inside the following **div tag**:
```
<div class="product-info"></div>
```
So the path can be:
```
{
    "tag": "div", 
    "class": "product-info", 
    "child": {
        "tag": "p", 
        "class": "price-value-gtm"
    }
}
```
You can nest as many child attributes as you need. For example:
```
{
    "tag": "section", 
    "class": "section-class", 
    "child": {
        "tag": "div", 
        "class": "div-class",
        "child": {
            "tag": "p", 
            "class": "p-class",
             "child": {
                "tag": "span", 
                "class": "span-class"
            }
        }
    }
}
```
If for some reason, however, you can't specify the path to the price using the tag's **id** or **class**, you can use **attrs**, which takes a key and value representing any property that the tag has. For example, imagine the price was located in the following tag:
```
<span data-key="value">1000</span>
```
The path can be:
```
{
    "tag": "span", 
    "attrs": {
        "data-key": "value"
    }
}
```

That was the most difficult part. Now we just have to add the product. 

So, first I will click on Products, then, in the top right corner of the screen, I will click on ADD PRODUCT.

Then, I will enter 5 pieces of information that are quite self-explanatory: website, name, url, interval and period. For example:

1. Website: Muztorg (which I just created)
2. Name: TAKAMINE G70 SERIES
3. Url: https://www.muztorg.ru/produ%D1%81t/A088397
4. Interval: 1
5. Period: Days

With this configuration, the application will check for the price of the product every day. If I wanted to check the price every 6 hours, for example, I could just set the interval to 6 and the period to Hours.

Each time the price is checked, a new instance of Price is created, which contains three pieces of information: product, price and date.

Finding the path to the price is by far the trickiest part. The good news is that usually websites have the same page structure for all their products, which means that once I manage to get the right path to the price of one product, I can very easily get the URL of a large number o products and start tracking them all. 

To find out whether the path you entered for a website works for a specific product, you can run the command:
```
python manage.py products-test <product-id>
```
Or you can test all your products at once by running:
```
python manage.py products-test
```
