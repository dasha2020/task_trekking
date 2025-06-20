# Task Trekking App

This app allows users to manage their tasks, look through other users' task boards, and leave comments under the task. Users can **add** task with opportunity to **edit**, and **delete** information. 
Made using Django and Python. 

### Task itself contains: 
* title 
* description 
* date when created 
* deadline 
* status 
    * Done
    * Not Done 
    * In progress 
* priority 
    * Urgent 
    * Not Urgent 


## Features

* View detailed info about task 
* Add, edit and delete tasks 
* View other users' boards
* Add, edit, delete comment for tasks 
* Authentication System  

## User Roles 

* Author of the task: has access to viewing, adding, editing and deleting information, and replying to the comments
* Users that view author's task: has read-only and commenting access to the task


## Getting Started

First clone the repository from Github and switch to the new directory:

```bash
git clone https://github.com/dasha2020/task_trekking.git
cd task_trekking
```

Create virtual environment (if necessary):

```bash
python -m venv env

env\Scripts\activate
```


Install project dependencies:

```bash
pip install -r requirements.txt
```


Apply migrations: 
```bash
python manage.py migrate
```

Then just run the project: 

```bash

python manage.py runserver
```

You will be able to go to this page in browser -> http://127.0.0.1:8000