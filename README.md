# Task Manager Project

Django Project for managing tasks in IT Company

## Check it out!

[Task Manager Project deployed to Render](https://task-manager-sufi.onrender.com)

## Installation

Python3 must be already installed.

```shell
git clone https://github.com/olia-trofymchuk/task-manager
cd task-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate # initialize database
python manage.py runserver # starts Django Server
```

## Features


* Authentication functionality for Worker/User
* Managing tasks: their types, deadlines, priority & information about workers + their positions
* Powerful admin panel for advanced managing
* Security for all data

Just sign in, create a task and you are off!

```shell
login: user
password: user12345
```

#### Shh! You can check how the admin panel works!
Click on this link and check all the power!

[Admin panel](https://task-manager-sufi.onrender.com/admin/)

## DB Structure
![DB Structure](db.jpg)

## Demo pages

* Login page
![Login page](login_page.png)

* Home page
![Home page](home_page.png)

* Page with tasks
![Task page](task-list.png)
