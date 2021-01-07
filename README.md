# Bayar ID API

### Prerequisites

1. Python Installation
    This project needs python version 3.6.6

2. Virtual Environment Installation
	- Windows:
        ```
        cd web_flask
	    py -m venv venv
        .\venv\Scripts\activate
        ```
	- MacOS / Linux:
        ```
        $ cd web_flask
	    $ python3 -m venv venv
        $ source venv/bin/activate
        ```

3. Dependencies Installation
   
    ```
    (venv) python3 -m pip install -r requirements.txt
    ```
    NB: requirement.txt is being produce from `python3 -m pip freeze > requirements.txt`

4. How To Run Program
    - Run MySQL Database <br>
        1. You can run MySQL database native server or using docker
        ```    
        docker run -d -p 3306:3306 --name bayarid-mysql -e MYSQL_ROOT_PASSWORD=root mysql:5 
        ```
        2. After the database server is running, import the `web_flask.sql`
    - Run Flask App
    ```
	(venv) set FLASK_APP=app.py
    (venv) set FLASK_ENV=development
    (venv) flask run --host 0.0.0.0
    ```

### Issue on Installation
- Error when Install flask-mysqldb 
    - MacOS
        ```
        brew install mysql
        ```





 
