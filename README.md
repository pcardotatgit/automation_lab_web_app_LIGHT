# automation lab web app_LIGHT

This package is a light version of the ***automation Lab Web App*** which contains only the files needed to run the Lab.

For information the complete  ***automation Lab Web App*** includes the Application editor as well. which is not the case in this LIGHT version. 

It is the same application with the same installation procedure

# Automation REST API automation Lab Web App

This application is a tiny Desktop Web Application that can be run either as a standalone desktop application on Windows, Linux or Mac computers, or as a tiny Web Server running on a Windows, Linux or Mac computers with python installed.

This is a tiny REST API lab infrastructure for Automation Workshops. It simulates real security solutions you have to automate thznks to their API. It is an alternative to use if you don't have these solutions.

As student you will go to a Threat Hunting operations which comes from a real life scenario. You will start from a detection by one of the productt, and from there you have to investigate to confirm and understand the scope of the attack, and finally and block the Threat. You must automate every operation in order to go as fast as possible. Exactly the same as in real life.

The Backend simulator is a python flask API web server, which exposes exactly the same REST API as the Security solutions. And it replies back exactly the same JSON results as the real solutions.

Your challenge consist of creating an automation workflows which will execute every operations we need to achieve the goal, one after the other until the Threat is blocked. 

The workflows is a series of steps which are just Web front end for python scripts. The web front end avoid to have to edit python scripts, but it is python in the background.

You have the send the correct API call to the correct solution in order to collect some specific information whcih is need. You have to pass the correct inputs to the wofkflows step, and you have to parse the JSON result you recieve in order to go to the next step.

The server simulates completely  REST APIs of the Security Solutions, from authentication to query details perspective. 

Students have to go the product API documentations first to understand which API to use and how to invoke it. And then send the API to the solution thru an Automation step in the Web App.

This Web App runs on Windows, Linux and Mac machines

But The package in this repo has been PrePackaged for windows machines to make installation very fast ( less than 5 Minutes ).

Prerequisit on the machines is : python version 3.11 or more installed.

Installation on windows is very straight forward. Installation on Mac or Linux is done thru standard python installation

# Installation on windows desktops

## Prerequisit

You must start with a machine that already has python installed. This project was written in python 3.11 version but should work with python 3.10.


## Very fast install for windows users

For anyone who don't want to waste time.

Download the project into a working directory into your laptop. Unzip the dowloaded file and open a terminal console into the project root directory. Then

- type a
- then type b
- then type c

***Notice :*** I came accros several times to the situation where this c.bat ( which does a pip install -r requirements.txt ) fails.

Then we have to install the modules one by one as shown bellow
    
    pip install flask
    pip install flask_request_params
    pip install sqlalchemy
    pip install pandas
    pip install crayons
    pip install requests
    pip install ijson

- then type d
- finally type e

Okay.  The simulator is installed.

Now to run it you just have to type the letter ***a*** from a CMD console openned into the working directory.

You must see the flask server start

## Here under the step by step installation if you don't use the procedure above

## Step 1. Create a working directory

Create a working directory into your laptop. Open a terminal CMD window into it. Name It XDR_BOT for example.

## Step 2. Copy the code into your laptop

The Download ZIP Method

The easiest way for anyone not familiar with git is to copy the ZIP package available for you in this page. Click on the Code button on the top right of this page. And then click on Download ZIP.

Unzip the zip file into your working directory.

The "git clone" method with git client

And here under for those of you who are familiar with Github.

You must have a git client installed into your laptop. Then you can type the following command from a terminal console opened into your working directory.

    git clone https://github.com/pcardotatgit/automation_lab_web_app.git
    

## Step 3. Go to the code subfolder

Once the code unzipped into your laptop, then Go to the code subfolder.

## Step 4. Create a Python virtual environment

It is still a best practice to create a python virtual environment. Thank to this you will create a dedicated package with requested modules for this application. 

### Create a virtual environment on Windows

    python -m venv venv 

And then move to the next step : Activate the virtual environment.

### Activate the virtual environment on Windows

    venv\Scripts\activate  

## Step 5. Install needed python modules

You can install them with the following 2 commands one after the other ( Windows / Mac / Linux ):

The following command might be required if your python version is old.

    python -m pip install --upgrade pip   

Then install required python modules ( Windows / Mac / Linux )

    pip install -r requirements.txt
    
Some time this instruction above fails. It seems to work but the modules are not installed.  

I such case we have to install the python modules one by one as shown bellow
    
    pip install flask
    pip install flask_request_params
    pip install sqlalchemy
    pip install pandas
    pip install crayons
    pip install requests
    pip install ijson
    
## finalize the installation run the **z_minimum_init_appli.py** script

    python z_init_appli.py

## Step 7 : run the simulator

type the following cli command

    venv\Scripts\activate
    
or 
    a.bat
    
You should see the flask console indicating you the the web server is listening on port 4000. 

## Authorize Network Connections to the application in the Firewall !

When you run the flask server for the first time... you are suppose to see a popup from for personnal firewall, telling you to authorize connections to this application on port TCP 4000.

Authorize this

## The challenge starts

Your browser should open on the login page.

username is : admin
password is : password

***Notice :*** username/password is a possible improvement for this application. It is not the case so far, but the application is ready for this.

# Your Challenge

The principle of this lab is to create a workflow in the workflow editor.

Student have to follow the lab guide. 

API keys shared with students are fakes keys, only valid for the simulator.

This workflow is a serie of steps, put one after the other which execute every atomic operation needed to achieve the final goal.

Generally speaking you to... find the correct API call to send to the targeted Security Solution, Search in the Web Application the step which had been prepared for this call. Then customize it by selecting the correct inputs, and selecting the correct output.

The output will be the input of the next step.  Etc etc... until the final step ( Malicious objects blocked ).

Every tile you have to send an API call, get the JSON result, parse it for extracting from it the searched information, and then store this extracted data into the variable library.

You can test step by step your workflow at any time, either from the begining, or from a selected step.

As you run a step, you are supposed to see your queries in the simulator console. And you see the server replies as well.

The challenge ends when in the Results page you see every objects to discover, and malicious objects blocked.

# Have Fun !!


# Installation on Mac Machines 

***Under construction***

# Installation on Linux machines

***Under construction***