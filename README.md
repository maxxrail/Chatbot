# RASA Chatbot Project

This project is a basic chatbot built using RASA NLU and Core, with custom actions served through a Flask web server.

## Project Structure

rasa_chatbot/< br / >
│< br / >
├── actions/< br / >
│ ├── init.py< br / >
│ └── actions.py< br / >
├── data/< br / >
│ ├── nlu.yml< br / >
│ └── stories.yml< br / >
├── models/< br / >
│ └── 20230801-123456.tar.gz< br / >
├── domain.yml< br / >
├── config.yml< br / >
├── credentials.yml< br / >
├── endpoints.yml< br / >
├── index.html< br / >
└── requirements.txt< br / >


### Directory and File Descriptions

- **actions/**: Contains custom actions for the chatbot.
  - `__init__.py`: Marks the directory as a Python package.
  - `actions.py`: Defines custom action classes.
- **data/**: Contains training data for the NLU and Core models.
  - `nlu.yml`: Defines intents, entities, and example phrases for training the NLU model.
  - `stories.yml`: Defines conversation stories for training the Core model.
- **models/**: Contains trained model files.
  - `20230801-123456.tar.gz`: Example trained model file.
- **domain.yml**: Defines the chatbot's domain, including intents, entities, slots, responses, and actions.
- **config.yml**: Configuration for the NLU and Core pipelines.
- **credentials.yml**: Configuration for connecting RASA to various messaging platforms.
- **endpoints.yml**: Configuration for the action server endpoint.
- **index.html**: HTML file to run chatbot in browser.

- **requirements.txt**: List of dependencies required for the project.

## Setup Instructions to Run Locally

### 1. Clone the Repository
```
git clone https://github.com/maxxrail/rasa_chatbot.git
cd rasa_chatbot
```
### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Train Model

Train the RASA model using the training data provided in **`data/nlu.yml`** and **`data/stories.yml`**:
```
rasa train
```
### 5. Run Acton Server

In a separate terminal, start the RASA action server to handle custom actions:
```
rasa run actions
```
### 4. Run Server

Start the RASA server to handle incoming messages:
```
rasa run --enable-api --cors "http://localhost:8000"
```
### 5. Open Webpage

Go to http://localhost:8000 to begin chatting with chatbot

## Editing Domain, NLU, Stories and Actions

### 1. Editing NLU, Stories and Domain

Stop the server edit the files: **`data/nlu.yml`**, **`data/stories.yml`** or **`domain.yml`** and retrain and rerun server:
```
rasa train
rasa run --enable-api --cors "http://localhost:8000"
```
### 2. Editing Actions

Stop the actions server, edit actions files and rerun actions server:
```
rasa run actions
```
