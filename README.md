# Currency Bot

## What is it

It's bot which can offer various information about the rate of currencies

## Local development

1. You must had installed python 3.7 and postgres

2. In postgres create user and database as described in `currency_bot/settings/dev.py`

3. Install requirements 
    
    `pip install -r requirments.txt`
 
4. Keep in mind for correct work you must pass at least TELEGRAM_TOKEN to environment variables
    
    `export TELEGRAM_TOKEN=_your_token_`
       
5. Run test server

    `python currency_bot/manage.py runserver`
    
6. For expose locale server port outside you can use [ngrok](https://ngrok.com/).
    
7. For registering webhook you can use command

    `python currency_bot/manage.py set_telegram_webhook https://example.com/`
