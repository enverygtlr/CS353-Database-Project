## CS353 Database Systems
### Social Betting Platform

Batuhan Tosyalı 21702055

Berk Güler 21402268

Enver Yiğitler 21702285

Ufuk Bombar 21703486

[Project Functionality Document](https://github.com/Wondrous27/CS353-Database-Project/blob/master/CS%20353%20PROJECT%20FUNCTIONALITY%20DOCUMENT.pdf)

# Installation guide
Make sure you have Python 3.x and PostgreSQL installed on your computer.   
To install PostgreSQl on Ubuntu type the following in your command line:  
sudo apt-get install postgresql-client-12 postgresql-12  
Clone the repository using:   
git clone -b dev https://github.com/Wondrous27/CS353-Database-Project.git  

## Python Virtual Environment  
Python Virtual Environment is a copy of the Python interpreter. You can install packages without affecting the global Python interpreter in your system. To install venv use the following command:    
$ sudo apt-get install python3-venv

Next, create a virtual environment named 'venv' in the directory you cloned.  
python3 -m venv venv  
In order to activate the virtual environment use the following command:  
source venv/bin/activate  
If you see (venv) $ the installation was successful.  
Next we're going to install the dependencies using pip. I created a requirements.txt file that includes all of our dependencies. Use the following command to install them:  
pip install -r requirements.txt  
## Running the website locally
If you got everything working so far, great news! Locate to the directory you cloned the repository to and type the following commands:  
(venv) $ export FLASK_APP=app.py  
(venv) $ export FLASK_DEBUG=1  
(venv) $ flask run  
And that is it, you have the instance running on your local host now! Open your favorite browser and go to either http://127.0.0.1:5000/ or localhost:5000.  

