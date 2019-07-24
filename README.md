# idiot-duo-twitter

[![Obejrzyj jak działa na Twitterze!](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/idiot2duo)
[![CircleCI](https://circleci.com/gh/JakubKoralewski/idiotduo-twitter/tree/master.svg?style=svg)](https://circleci.com/gh/JakubKoralewski/idiotduo-twitter/tree/master)
[![CircleCI build artifacts](https://img.shields.io/badge/testowe%20obrazki-z%20CircleCI-blue.svg)](https://jakubkoralewski.github.io/idiotduo-twitter/)
[![Docker Automated build dla CircleCI](https://img.shields.io/docker/automated/jakubkoralewski/circleci-python-chrome-chromedriver-ffmpeg.svg)](https://hub.docker.com/r/jakubkoralewski/circleci-python-chrome-chromedriver-ffmpeg/)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/JakubKoralewski/idiotduo-twitter/blob/master/LICENSE)

[PL] Losowy cytat z biblii / interesujące słownictwo + losowy moment z kanału Idiot Duo = najlepszy bot na Twitterze!

[EN] I have since regretted using the Polish language on GitHub; however, all the content related with this repo is in Polish which heavily contributed to my choice. Because of this the code is using Polish variable names and comments. For a quick overview check out this small description:

<details>
<summary> English description</summary>

This Python app runs on Heroku and posts images with funny quotes on them on Twitter. I am using Selenium WebDrivers to get Bible quotes online, youtube-dl and ffmpy (FFmpeg) to download single frames of videos from my YouTube channel, PIL (Pillow) to overlay text on images, Sentry to log errors and pytest for testing.
Both Twitter APIs and YouTube APIs are leveraged. In case getting the Bible quotes online I also have an offline alternative in `static/slowo_na_dzis.json` which is a collection of lexical fun facts in Polish.

Checkout my other repos for English content! I was only starting my GitHub career when creating this repo and I should've used English.
</details> 


## Działa na dwa sposoby

### Pierwszy sposób

[![Przykładowy tweet](https://i.imgur.com/64jXPWs.png)](https://twitter.com/idiot2duo/status/1054050784017612800)

### Drugi sposób

[![Przykładowy tweet numer 2](https://i.imgur.com/mvEVG7p.png)](https://twitter.com/idiot2duo/status/1060472290985631744)

## Jak działa pod spodem

![Jak działa](docs/0_jak_dziala.ipynb)

## Jak samemu postawić tego/takiego bota

Do stworzenia
