#OWASP - HACK - FLASK

A simple Flask based app to simulate and play with some of the more common [OWASP top ten](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project#tab=OWASP_Top_10_for_2017_Release_Candidate) items.


## Covered Items

* SQL Injection
* XSS
* CSRF
* Sensitive Data Exposure
* Underprotected APIs


## System Setup

* Basic Flask App
* Login Form
* User Profile Form
* Predefind SQLLite database with set of shopping items.

## Installation

```sh
$> python -m venv venv
$> source venv/bin/activate
$> pip install -r requirements.txt -U
```

## Running
```sh
$> source venv/bin/activate
$> FLASK_APP=owasp-hack-flask.py python -m flask run --port=1337
```

## To Fully Solve you should:

Make sure to consult console logs to solve.

* (SQL Injection) Be able to login to the application (without a known user name and password).
* (XSS) Use Search Box to simulate XSS
* (SQL Injection) Extract user and password list from Search Box
* (Underprotected APIs) With Known User Name, update email for a different user.



## Hints

`openssl des3 -d -salt -in ./possible_solution.md.encrypted`

password:
`randomizer`