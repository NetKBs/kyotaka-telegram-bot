# kyotaka-telegram-bot

## Attention

This is a self-developed project made while I was doing #100DaysOfCode on twitter. This **doesn't generate profits** for me. If you have a complaint, please contact me.  

---  

## Then what is this?

Kyotaka, the bot for Telegram, that notifies you when a new story is uploaded (or something like that). The idea came because sometimes I like to distract myself by reading translated (to English) stories (manga, manhwa, etc.) from some specific websites.  

## So, how exactly does it work?

Welp, first of all, I use the library [python-telegram-bot][tg-bot-library] to program my bot on Telegram. However, because I need to make contact with webpages to get information, I also use the library [beautifulsoup4][bs4-library].  

So now we have two external libraries:  
* [beautifulsoup4][bs4-library].
* [python-telegram-bot][tg-bot-library]

[bs4-library]: https://beautiful-soup-4.readthedocs.io/en/latest/
[tg-bot-library]: https://github.com/python-telegram-bot/python-telegram-bot
