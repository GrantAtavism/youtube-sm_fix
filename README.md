# Youtube_subscription_manager

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Type of File](#type-of-file)
- [Cache](#cache)
- [HTML & RSS](#html--rss)
- [Requirements](#requirements)
- [Compatible](#compatible)
- [Screenshots](#screenshots)

## Description
Youtube_subscription_manager was built as a free alternative to https://www.youtube.com/feed/subscriptions and does not requires to use your youtube account.

It can gather informations about every video in a playlist, a channel or your subsciption feed and outputs it as a html page, a detailed list or a list of links.

## Installation
1. Clone the project: `git clone https://github.com/sawyerf/Youtube_suscription_manager.git`
2. Open the folder you just cloned : `cd Youtube_subscription_manager`
3. Execute the setup: `sudo python3 setup.py install`
4. Recover your subscription file in youtube and you are ready to go !

## Usage

Before using youtube-sm, it is recommended that you download your subscriptions configuration from youtube.com by using this link once you are connected to youtube.com :

https://www.youtube.com/subscription_manager?action_takeout=1

Once this is done, you may load it in youtube-sm by using the following command :

`youtube-sm --init [file]`

Finally, you can start using the program using the commands shown below (or through `youtube-sm -h`)

```
youtube-sm [OPTIONS]
```

## Commands

```
-h                     Print this help text and exit
-n     [file]          Use an other xml file for your subscriptions
-m     [mode]          Choose the type of the output (html, raw, list)
-t     [nb of days]    Choose how far in the past do you want the program to look for videos
-d                     Show the dead channels + those who posted no videos
-o     [nb of months]  Show the channels who didn't post videos in [nb of months] + dead channels
-l     [id]            Choose to analyze only one channel or playlist
-r                     Remove the cache running the program
-s     [id/all]        Outputs the stats of the selected channel(s)
-a     [id]            Choose to append a channel or a playlist at the end of sub.
--init [file]          Remove all your subs and the cache and init with your subscription file.
--af   [file]          Append a file with list of channel or a playlist in sub.swy
--ax   [file]          Append a xml file in sub.swy
--all                  Recover yours subs in the common page web (more videos)
--cat                  View your subscriptions
--css                  Import the css files
--loading              Prints a progress bar while running
```

## Type of File
- raw :
```
{date}     {video_id}     {channel_id}     {title}     {channel}     {link_pic}
```
- list :
```
https://www.youtube.com/watch?v={video_id}
```
- html :
```
<!--NEXT -->
<div class="video">
	<a class="left" href="https://www.youtube.com/watch?v={video_id}"> <img src="{link_pic}" ></a>
	<a href="https://www.youtube.com/watch?v={video_id}"><h4>{title}</h4> </a>
	<a href="https://www.youtube.com/channel/{channel_id}"> <p>{channel}</p> </a>
	<p>{date}</p>
	<p class="clear"></p>
</div>
```

## Cache
3 files are generated by the program : `sub.swy`, `log` and `data/`.
- `sub.swy` is a list of yours subscriptions.
- `log` contains the script's time of execution.
- `data/` is a folder where the information for every video are stored.

These 3 files are generated in:
- Windows: `C:\Users\<name>\.youtube_sm\`.
- Linux:   `/home/<name>/.cache/youtube_sm/.`.

## HTML & RSS
With youtube-sm you can recover your subscriptions using two methods:
- RSS (default): videos are recovered through an XML page.
- HTML (with --all): videos are recovered through an HTML page.

They are two choice because they cannot recover the same informations and don't require the same amount of time. 
So the default method (the RSS method) is more adapted to recover only the newest videos, whereas the HTML method is more adapted to recover all the videos of a playlist or to recover its last 30 videos.

|            |   *HTML*  |   *HTML*   |   *RSS*   |
|:----------:|:-------:|:--------:|:-------:|
|            | **Channel** | **Playlist** |   **Both**   |
|  Execution |   slow  |   slow   |   Fast  |
|   Number   |30 videos|100 videos|15 videos|
|    Date    | **~** | ✖ | ✔ |
|  Like Rate | ✖ | ✖ | ✔ |
|    Views   | ✔ | ✖ | ✔ |


## Requirements
- Python 3

## Compatible
- Linux
- Windows
- Android (Termux)
- MacOS (I don't known)

## Screenshots
<p><img src="./screenshot/index.jpg" alt="Phone screen" width=405px height=720px></p>
<p><img src="./screenshot/index_pc.jpg" alt="PC screen" width=100% height=auto></p>
