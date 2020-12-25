# Bayar ID API

### Prerequisite

1. Install virtual environment
    - CD ke folder 'web_flask'
	- Windows:
        ```
	    py -m venv venv
        .\venv\Scripts\activate
        ```
	- MacOS / Linux:
        ```
	    python3 -m venv env
        source venv/bin/activate
        ```

2. Install Library Pendukung
    - pip3 install numpy
    - pip3 install matplotlib
    - pip3 install pandas
    - pip3 install scikit-learn
    - pip3 install librosa
    - pip3 install tensorflow
    - pip3 install keras
    - pip3 install flask
    - pip3 install flask-restful // buat REST api
    - pip3 install flask-mysqldb // buat database

3. Setting file python yang mau menjadi program utama flask 
	a. buat file python namanya app.py utk jadi program utama flask
	b. jalankan perintah set FLASK_APP=app.py

4. Setting environment menjadi development
	a. jalanin perintah set FLASK_ENV=development

5. Jalanin server flask utk bisa buka website yang kita buat
	a. jalanin perintah flask run --host 0.0.0.0


### Issue on Installation
- Error when Install flask-mysqldb 
    - MacOS
        ```
        brew install mysql
        ```

### Run MySQL on Docker
```
docker run -it -p 3306:3306 --name bayarid-mysql- -e MYSQL_ROOT_PASSWORD=root mysql:5 
```




 
