<h3 align="center"><img src="https://i.postimg.cc/s2Pb8srG/banner.png" width="500"></a></h3>

<span align="center"> 
  
<br>
<h1>Muso</h1><h4>A Friendly Neighbourhood Discord Music Player<h4>
<br>

[![GitHub license](https://img.shields.io/github/license/DivyaKumarBaid/Muso?color=e63946&logo=Big%20Cartel&logoColor=white&style=for-the-badge)](https://github.com/DivyaKumarBaid/Muso/blob/main/LICENSE) [![GitHub forks](https://img.shields.io/github/forks/DivyaKumarBaid/Muso?logo=JFrog%20Bintray&logoColor=white&style=for-the-badge)](https://github.com/DivyaKumarBaid/Muso/network) [![GitHub stars](https://img.shields.io/github/stars/DivyaKumarBaid/Muso?color=%23ffcb77&logo=Apache%20Spark&logoColor=yellow&style=for-the-badge)](https://github.com/DivyaKumarBaid/Muso/stargazers)

</span>

## Description

A simple but efficient Music Bot that plays your favourite music in a loop so just add a playlist and chill listening it playing for you.

<br>
<br>

---

## Commands

<span align = "center">

| m.add              | Adds music to the bots playlist.                       |
| ------------------ | ------------------------------------------------------ |
| m.play <channel>   | Plays the playlist added to the bot.                   |
| m.next             | Skips the current song and plays the next in Queue.    |
| m.stop             | Stop the Music.                                        |
| m.volume <int>     | Sets the volume.                                       |
| m.remove <int>     | Removes the song in Queue.                             |
| m.clear_playlist   | Clears the Queue.                                      |
| m.playOn <Channel> | Set the Default Voice Channel on which Bot would play. |
| m.songs            | List the songs present in the Queue.                   |

</span>

---

## Forking and Hosting

This music bot is now hosted on heroku and works well on repl also.

For using it on heroku
Fork this repository and then under Deploy in heroku add your this forked repo
Under setting - buildpack add

> heroku/python
> https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
> https://github.com/xrisk/heroku-opus.git

In setting - config vars add

> Key - Token
> and in value add your discord bots generated Token (For more info go through Youtube Videos)

And then under resources enable worker.

**TADA Your Bot is now online**

For using in on other platforms make sure you install requirements.txt

```
    pip install -r requirements.txt
```

---

For any other Questions raise an issue and I will try to solve you problem.
