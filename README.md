# LabLineup
LabLineup is a web app that allows students inside of a course lab to request help from the teaching assistant(s). The app will provide the
TA(s) with a queue of students in the order in which they submitted requests for help. The functionality can be expanded to include reports
and notifications for the instructor of record. The instructor will be able to see short descriptions of problems, which will allow him/her
to see common issues between students. After the student receives help, he/she can rate the TA’s assistance (feedback will be submitted to
the instructor). If the number of requests in the queue reaches a threshold, the professor can receive a notification telling him/her that
more assistance is needed in the lab. The web app can display the student’s current position in the queue along with an estimated wait time.

# Style
Google Style Guide: https://google.github.io/styleguide/

# Technologies
- Django
- Bootstrap
- Google Cloud Platform
- MailGun
- MySQL (CloudSQL)
- Selenium IDE
- Square API / Checkout

# Authors
- Bryce Tant - bjtant@email.sc.edu
- Graham McDonald - mcdonag@email.sc.edu
- Landon Everhart - lte@email.sc.edu
- Reed Segars - jrsegars@email.sc.edu
- Nick Knight - nrknight@email.sc.edu

# Editing
The virtualenv name is LLenv.
To activate the virtualenv in Windows, go to the project dir, type .\LLenv\Scripts\activate.bat

# Running
To run the app:
- Clone the source code
- Run pip3 install -r LLenv/LabLineup/requirements.txt
- Run python manage.py runserver

# Testing
To run the behavorial tests:
- Run pip3 install -r LLenv/LabLineup/requirements.txt
- Selenium Command-Line Runner requires the following dependencies:
  - node (the Node.js programming language) : https://nodejs.org/en/download/
- Selenium Command-Line Runner requires a browser driver
  - Chrome: $ npm install -g chromedriver
  - Edge: $ npm install -g edgedriver
  - Firefox: $ npm install -g geckodriver
  - Internet Explorer: $ npm install -g iedriver
- Navigate to the LLenv/LabLineup/app/tests/ directory
- $ selenium-side-runner BehavTests.side

To run the unit tests:
- Run pip3 install -r LLenv/LabLineup/requirements.txt
- Navigate to the LLenv/LabLineup/app/tests/ directory
- $ python ../../manage.py test
