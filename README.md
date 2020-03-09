# Currency Bot

## What is it

It's a telegram bot that can offer various information about the rate of currencies.
Ready for use an instance of this bot you can find in Telegram under the name [@StrongCurrencyBot](https://t.me/StrongCurrencyBot).

## Development

### Local development

1. You must have installed the python 3.7 and the Postgres

2. In the Postgres create a user and a database. Don't forget set this information to settings.

3. Install the requirements
    
    `pip install -r requirments.txt`
 
4. Keep in mind for correct work you must pass at least TELEGRAM_TOKEN to environment variables
    
    `export TELEGRAM_TOKEN=_your_token_`
       
5. Run the test server

    `python currency_bot/manage.py runserver`
    
6. For expose the locale server port outside you can use [ngrok](https://ngrok.com/).
    
7. For registering the webhook you can use next command

    `python currency_bot/manage.py set_telegram_webhook https://example.com/`

### Development in the container

1. Build the image
 
    `docker build -f Dockerfile . --tag currency-bot`

2. Run a container with the host network

    `docker run --rm -it --network host currency-bot` 

## Deployment

### Settings

Don't forget to set the next environment variables if you use `currency_bot.settings.container` settings(default in the container).

* `ALLOWED_HOSTS` - your Heroku host name

* `DATABASE_URL` - must already exist from the database add-on

* `SECRET_KEY` - a Django settings [secret key](https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key)

* `TELEGRAM_SECRET_PATH` - secret path(optional) that will be added to webhook API to make sure that the Webhook request comes from Telegram. [docs](https://core.telegram.org/bots/api#setwebhook)

* `TELEGRAM_TOKEN` - token that you get from BotFather in the Telegram

### Deployment to Heroku

1. Login to your Heroku account

    `heroku login`

2. Set Heroku git

    `heroku git:remote -a <app_name>`

3. Set `container` type of deployment instead of `buildpacks`

    `heroku stack:set container -a <app_name>`

4. Push project to Heroku

    `git push heroku master`

5. Register webhook, using Heroku console(also you local environment with same settings and environment variables)

    `python3 currency_bot/manage.py set_telegram_webhook https://strong-currency.herokuapp.com/`
