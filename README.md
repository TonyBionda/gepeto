<h1 align="center">
  GEPETO
</h1>
<p align="center">Machine Learning prediction with web-app for the CHSB</p>

## ⚡️ Quick start

First, [download](https://www.python.org/downloads/) and install **Python**. Version `3.00` or higher is required.

Follow the instructions below to start using the project :

- Clone the repository and install the dependencies (venv is recommended) :
  ```bash
  git clone https://github.com/TonyBionda/gepeto.git
  cd gepeto
  pip install -r requirements.txt
  ```

- Run the ML app to generate the model :
  ```bash
  python3 machine-learning/main.py # or python machine-learning/main.py
  ```  

- And then, run the web-app :
  ```bash
  python app/manage.py runserver # or python3 app/manage.py runserver
  ```

- Finally, open your browser and go to `http://127.0.0.1:8000/`
