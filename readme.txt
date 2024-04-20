To start the server, switch to bash terminal and follow the next steps.

Step #1: create a virtual enviroment.

1. virtualenv -p python3 env

Step #2: activate the env.

2. source env/Scripts/activate

You should get: 
(env) 
Warre@Warren MINGW64 ~/OneDrive/Escritorio/Poro-Academy-master (master)

Step #3: Install the required dependencies used in this project.

3. install Flask pymongo certifi

Step #4: Execute the line command ./app to initialize the server on the port

You should get: 

Warre@Warren MINGW64 ~/OneDrive/Escritorio/Poro-Academy-master (master)
$ ./app
 * Serving Flask app 'app.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000