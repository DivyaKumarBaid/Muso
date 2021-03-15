# Live_Discord_music_bot
<p align="left">
<a href="https://github.com/DivyaKumarBaid/Live_Discord_music_bot/blob/main/LICENSE" alt="Lisence"><img src="https://img.shields.io/github/license/DivyaKumarBaid/Live_Discord_music_bot"></a> <a href="https://github.com/DivyaKumarBaid/Live_Discord_music_bot/issues" alt="Issues"><img src="https://img.shields.io/github/issues/DivyaKumarBaid/Live_Discord_music_bot"></a> <a href="https://twitter.com/DivyakumarBaid1?s=09" alt="Twiter-Follow"><img src="https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2FDivyaKumarBaid%2FDiscord_Music_bot"></a>
</p>

This is a simple Discord Music bot that plays music 24/7 looping thorugh the ```URL```  from youtube.
To run this bot we need to several packages such as PyNaCl, discord.py, youtube-dl

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) \
To install discord.py

```bash
python3 -m pip install -U discord.py
```
To install PyNaCl
```bash
pip install pynacl
```
To install youtube_dl
```bash
pip install youtube_dl
```
You also need to install [FFmpeg](https://www.ffmpeg.org/) 

## Pre-Text:

This is a discord bot made using the lastest discord.py api as of march 2021. This bot uses list to store ```URL``` of youtube songs and then play it on the desired voice channel until and unless commanded to stop. I did this program in python language and have used discord.py , youtube_dl , PyNaCl , FFmpeg and several other packages and api's. Initially this bot was build on repl.it IDE and was monitored to be online using [Uptimerobot](https://uptimerobot.com/)

## How to Install

1. Create a ```python``` virtual environment.I did in repl.it
2. Clone the repo ```git clone https://github.com/DivyaKumarBaid/Discord_Music_bot.git``` or download the repository.
3. Go to the cloned/downloaded directory ``` cd Discord_Music_bot ``` 
4. Upload it in ```repl.it```
5. Create a bot in [discord developers portal]((https://discord.com/developers/docs/game-and-server-management/vanity-perks))
6. Copy the ``Token`` of the bot and paste it in the ``.env`` file as ``TOKEN``
7. Run the bot on ```repl.it```
8. Copy the ``url`` that appears on the right side of window
9. Go to [Uptimerobot](https://uptimerobot.com/) and create a monitor and paste the copied ``url`` and start the monitor.This will keep the bot alive even after you close it.

    For more precise steps have a look at [FreeCodeCamp](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)

## Commands

```
m.add [url]

This adds the music to queue

m.play [VoiceChannel(optional)]

This command plays music in the desired channel or by default in General

m.songs

Lists all the songs in the playlist

m.volume [integer value]

Sets the volume level

m.stop

Stops the music player

m.clear_playlist

Removes every song from the playlist

m.remove [index from the list of songs provided by typing m.songs]**

Removes the particular song
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Note:
I have similar bot that downloads music and then play. If you dont have problem for space and downloading time you may have a look to my repo from [here](https://github.com/DivyaKumarBaid/Discord_Music_bot)
