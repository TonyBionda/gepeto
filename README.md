<h1 align="center">
  GEPETO
</h1>
<p align="center">Machine Learning prediction with Django web-app for the CHSB</p>

## ⚡️ Quick start

First, [download](https://www.python.org/downloads/) and install **Python**. Version `3.00` or higher is required.

Follow the instructions below to start using the project :

1. Clone the repository and install the dependencies (venv is recommended) :

  ```bash
  git clone https://github.com/TonyBionda/gepeto.git
  cd gepeto
  pip install -r requirements.txt
  ```

2. Create `.env` file from `.env.example` and fill it with your own values :

  ```bash
  cp .env.example .env
  ```

3. Run the ML app to generate the model :

  ```bash
  python3 machine-learning/main.py # or python machine-learning/main.py
  ```  

4. And then, run the web-app :

  ```bash
  python app/manage.py runserver # or python3 app/manage.py runserver
  ```

5. Finally, open your browser and go to `http://127.0.0.1:8000/`
