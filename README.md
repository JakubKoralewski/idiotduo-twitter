# idiot-duo-twitter

[![Obejrzyj jak działa na Twitterze!](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/idiot2duo)
[![CircleCI](https://circleci.com/gh/JakubKoralewski/idiotduo-twitter/tree/master.svg?style=svg)](https://circleci.com/gh/JakubKoralewski/idiotduo-twitter/tree/master)
[![CircleCI build artifacts](https://img.shields.io/badge/testowe%20obrazki-z%20CircleCI-blue.svg)](https://jakubkoralewski.github.io/idiotduo-twitter/)
[![Docker Automated build dla CircleCI](https://img.shields.io/docker/automated/jakubkoralewski/circleci-python-chrome-chromedriver-ffmpeg.svg)](https://hub.docker.com/r/jakubkoralewski/circleci-python-chrome-chromedriver-ffmpeg/)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/JakubKoralewski/idiotduo-twitter/blob/master/LICENSE)

[PL] Losowy cytat z biblii / interesujące słownictwo + losowy moment z kanału Idiot Duo = najlepszy bot na Twitterze!

<details>
<summary>[EN] I have since regretted using the Polish language on GitHub; however, all the content related with this repo is in Polish which heavily contributed to my choice. Because of this the code is using Polish variable names and comments. For a quick overview check out this small description.</summary>

### English description

This Python app runs on Heroku and posts images with funny quotes on them on Twitter. I am using `Selenium WebDrivers` to get Bible quotes online, `youtube-dl` and `ffmpy` (FFmpeg) to download single frames of videos from our YouTube channel, `PIL (Pillow)` to overlay text on images, `Sentry` to log errors and `pytest` for testing.
Both Twitter APIs and YouTube APIs are leveraged. In case getting the Bible quotes online I also have an offline alternative in [`static/slowo_na_dzis.json`](static/slowo_na_dzis.json) which is a collection of lexical fun facts in Polish.

Checkout my other repos for English content! I was only starting my GitHub career when creating this repo and I should've used English.

</details> 

## Development

Install requirements: `pip install -r requirements.txt`. Advisable to use venv.

You need to create a `config_secret.py` in the `bot` directory, with the following values:
```python
api_key = ''
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
sentry_url = ''
yandex_api = ''
```

You also need to download the `chromedriver.exe` for local development if you don't use Docker.
I downloaded it from [here](https://chromedriver.chromium.org/downloads) and put it in my `static` folder.
You need Google Chrome installed for this to work. Also make sure the version of the driver you download supports
the Chrome browser version you have installed on your Windows machine.

Do the same for `ffmpeg.exe` which you can download [here](https://www.ffmpeg.org/download.html).
Put it in the `static` directory.

The production server uses a Linux-based OS and will not use Windows' executables, this is only for development purposes. 
Only Windows has been tested and verified to be a usable development system. 
Feel free to hack the Dockerfile for your liking.

## Testing

You should now be able to verify everything is working as it should by running the following:

*Running the test will open the Chrome browser periodically as it tests certain functions related
to Selenium, don't freak out.*

```sh
py.test
```

You may add `-n NUM` where `NUM` is the amount of cores you want to use in parallel (or `auto`).

After the tests finish successfully you'll be left with 15 test images in `tests/output` that
are stored [here](https://jakubkoralewski.github.io/idiotduo-twitter/) on each CI build.

