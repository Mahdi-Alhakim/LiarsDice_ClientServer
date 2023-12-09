# Liar's Dice - Client/Server

This is a 4 - player Client/Server game developed as an online digital copy of the game "Liar's Dice". The repository consists of both the Client and the Server code


## Requirements:
- #### python 3.x
- #### Tkinter 8.6+
- #### Thread6 0.2.0
- #### Socket


## Setup:

1. Create a virtual environment using the latest release of virtualenv:

``` bash
> pip install virtualenv --upgrade
> virtualenv venv
```

_If there are problems with installing tkinter:_
- Install tkinter package. Ex: Homebrew:
``` bash
> brew install python-tk
```
- Then create the virtual environment as follows:
```
> virtualenv venv --system-site-packages
```

2. Access the virtual environment `./venv`
``` bash
> source ./venv/bin/activate
```


## Execution:

#### To run the server, execute the following command:

``` bash
> python3 ./Server/main.py
```

#### To run the client, execute the following command:

``` bash
> python3 ./Client/index.py
```

* > Creat 4 Clients and join with different usernames.


## How to Play:

1. **Objective:** Survive until all other players have lost their dice

2. **Each Round:** 

    - Players role their dice and hide them from the other players.
    - The first player in the round calls a bet concerning how many dice landed on a certain value.\
        `Ex: " There are four '6's! "`
    - From then on, players have to options:
        - Raise the bet.\
        `Ex: " There are seven '6's! " or " There are five '2's! "`
        - Or Call the previous player a liar and reveal the dice to discover whether or not the bet was valid. (`Ex: Were there actually atleast four '6's?` )
    - If a player chose to call a lie and the bet turns out valid, the lie-caller loses a die.
    - Otherwise, the previous player loses a die.
    - A new round begins with reshuffled dice, and the game continues until all but one player lose all their dice.

