# kyotaka-telegram-bot (Canceled)

## Attention

This is a self-developed project.

### Canceled
Welp this was a failed project that I never hosted but in local everything went well(? I guess, however I learned several things. 
If you find something useful here in this ugly code, then I'm glad for you :)

<br><br>
---  

## Then what is this?

Kyotaka, the bot for Telegram, that notifies you when a new story is uploaded (or something like that). The idea came because sometimes I like to distract myself by reading translated (to English) stories (manga, manhwa, etc.) from some specific websites.  

## So, how exactly does it work?

Welp, first of all, I use the library [python-telegram-bot][tg-bot-library] to program my bot on Telegram. However, because I need to make contact with webpages to get information, I also use the library [beautifulsoup4][bs4-library].  

So now we have two external libraries:  
* [beautifulsoup4][bs4-library].
* [python-telegram-bot][tg-bot-library]

## Features (some)
First impressions  

![start](https://user-images.githubusercontent.com/76603397/167233018-a2f6eea0-958d-46e6-9a0d-cfcb1145590e.png)  

### Search
![search](https://user-images.githubusercontent.com/76603397/167233130-ca2f2fb9-d042-49d4-a8c9-7fb1de9a0b35.png)  

### Add
![add](https://user-images.githubusercontent.com/76603397/167233213-30e875a6-8e1e-4c85-b601-939a679f5832.png)  
_Note: To add a story, you must put the direct link provided from the results of the function "search"._

### Track
![image](https://user-images.githubusercontent.com/76603397/167233360-781fbe4e-77d5-48d4-b6be-8663230bb336.png)  
_Note: When you have stories added, you can start the tracker to check eventually for new chapters._


[bs4-library]: https://beautiful-soup-4.readthedocs.io/en/latest/
[tg-bot-library]: https://github.com/python-telegram-bot/python-telegram-bot
