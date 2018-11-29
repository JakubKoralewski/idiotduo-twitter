from setuptools import setup, find_packages

setup(
    name="idiot-duo-twitter", 
    packages=find_packages(),
    setup_requires=["pytest-runner", "youtube-dl", "Pillow", "python-twitter", "urllib3", "ffmpy", "selenium"],
    tests_require=["pytest"]
    )
