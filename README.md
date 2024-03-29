# Swapify
## Structure
For the front end of our project, we used HTML/CSS. For the back-end, we used a framework called Flask, which uses the Python programming language.
## How to get the project running
To ensure that the project runs smoothly locally, here are the instructions:
1. If Python has not been installed, [this page](https://www.python.org/downloads/) will guide you in installing it.
2. Pip is required to install Flask. If pip is not installed, [this page](https://pip.pypa.io/en/stable/cli/pip_install/) will guide you in installing it.
2. Clone the repo into a local directory.
3. Make sure you have some type of software that supports HTML, CSS, and Python. We decided to use VSCode.
4. Start installing Python flash command lines by entering these steps into a terminal:
```
    pip3 install virtualenv
    virtualenv env
    source env/bin/activate
    pip3 install flask flask-sqlalchemy flask-login
    python3 app.py
```
5. If the steps are done correctly, you should see this pop up:
![alt text](showterminal.png)
6. Lastly, type in `localhost:5000` in your browser to run the frontend webpages. So, if you were to visit the profile page,
you would type in localhost:5000/profile.
## Authors
This project was created in CSE 481, a Social Computing Capstone at the University of Washington. Our team name is Swapify, and
our members consists of Andy Thai, Nancy Jimenez-Garcia, Nora Medina and Gai Wai Wong.
