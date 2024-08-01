# RASA Chatbot Project

This project is a basic chatbot built using RASA NLU and Core, with custom actions served through a Flask web server.

## Project Structure

rasa_chatbot/
│
├── actions/
│ ├── init.py
│ └── actions.py
├── data/
│ ├── nlu.yml
│ └── stories.yml
├── models/
│ └── 20230801-123456.tar.gz
├── domain.yml
├── config.yml
├── credentials.yml
├── endpoints.yml
├── index.html
└── requirements.txt


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

```sh
git clone https://github.com/maxxrail/rasa_chatbot.git
cd rasa_chatbot

### 2. Install Dependencies

```sh
pip install -r requirements.txt


### 3. Train Model
Train the RASA model using the training data provided in **`data/nlu.yml`** and **`data/stories.yml`**:
```sh
rasa train

### 4. Run Server
Start the RASA server to handle incoming messages:
```sh
rasa run --enable-api --cors "http://localhost:8000"

### 5. Run Acton Server
In a separate terminal, start the RASA action server to handle custom actions:
```sh
rasa run actions

### 6. Run App
In another separate terminal, Serve the web interface:
```sh
python -m http.server
