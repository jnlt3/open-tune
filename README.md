# open-tune

This project's goal is to become a user friendly system for distributed SPSA tuning of chess engines

## Setup

```
cd open-tune
```

#### Linux/MacOS

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### Windows

```
pip install -r requirements.txt
```

## Server

```
cd server
flask run
```

## Client

```
cd client
```

#### Linux/MacOS

```
python3 main.py
```

#### Windows

```
python main.py
```

## To Do

### Website
1. Should show all the ongoing tuning sessions
2. Include graphs for each one of them
3. Submit/Remove tests

### Client
1. Should handle cutechess-cli installation
2. Should handle opening book installation
3. Should handle cleaning up all the directories when the client exits

### Server
1. Save the ongoing tuning sessions to a database
2. Distribute workloads across clients based on time control
3. Login system
