# connect5

## Setup:
No setup is required for the client or the server.
However it is only test against the following:
```Python 3.5.2``` on ```Ubuntu 16.04```

The ```game_tester.py``` requires you to install pytest, instructions:
1. Create a virtual environment for the project
 ```virtualenv -p python3 env3```
 
2. Active the environment
 ```. env3/bin/activate```
 
3. Install the required libraries
  ```pip install requirements.txt```
  
## Usage:
Server:
```./server.py```

Client:
```./client.py```

Game Tester:
```pytest game_tester.py```

Client Tester
```./client_tester.py```
then, in a different terminal
```./client.py```
and follow the instructions.