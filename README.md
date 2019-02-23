# class Play

class Play is a web application that allows professor to take quizes in real time. Following are the main features
Web application features
Some of the features for the application are as follows:
* professor to create “Courses” that students can register.
* students to sign up in the application
* students to register the “Courses" created by the professor.
* students to view their individual performance
* CORE FEATURE: As soon as the professor starts the quiz, the application must allows
students to view the question and answer them within the specific time period.
* professor to start the question (or bulk of question) to be displayed on the professor side.
* After the all the question timer expires, it shows the correct answers along with the metrics
of how many answered correctly and how many did not (option of three, review question
either now or after the end of quiz, don’t show results at all)
* professor to view individual student performance as well as the performance of the entire
class

### Prerequisites

* Language: Python 2.7
* Web Framework: Flask 1.0.2
* Templating Engine: Jinja2
* State maintenance: REDIS (in memory database)
* Persistence: PostgreSQL
* Structure: Html 5
* Styling: Bootstrap (CSS framework) 4.0
* Dynamic behaviour (Java script)
* Jquery for AJAX calls
* REST API
* Data type: JSON




## Getting Started

To get the development environment up and running. First make sure the prerequisites are installed. Then setup 
virtual environment with following commands

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

Then install the package prerequisite by:
```
 python setup.py install
```

Make sure the you setup 
* PostgreSQL
* Redis

Put in their endpoints in the `classPlay/config.py` file.

Navigate to `classPlay` directory and then run the flask back-end by the following command:

```
python run.py
```

you should have your server up and running

## Application Screenshots

![Alt text](Artifacts/Running_Application_ScreenShot/1.png?raw=true "1")
![Alt text](Artifacts/Running_Application_ScreenShot/2.png?raw=true "2")
![Alt text](Artifacts/Running_Application_ScreenShot/3.png?raw=true "3")
![Alt text](Artifacts/Running_Application_ScreenShot/4.png?raw=true "4")