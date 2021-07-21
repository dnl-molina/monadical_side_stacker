# monadical_side_stacker

Author: Daniel Alejandro Molina Yepes
\
Technologies: Python (flask,websockets,unittest), React(react, react-router, jest), Docker, Nginx

# Requirements
you need to put the next ports available: 3000,3001 and 3002.

# How to run with docker-compose
go to the cloned repository and run the next command
\
```$ docker compose up```

# How to run with docker
go to the cloned repository and run the next commands
### run front
```
cd front
npm install
npm run build
docker build -t front .
docker stop front & docker rm front & docker run --name front -p 3000:80 front
```
### run back
```
cd back
docker build -t back .
docker stop back & docker rm back & docker run --name back -p 3001:3001 -p 3002:3002 back
```

# How to run with linux
### run front
ensure you have nodejs v14
```
cd front
npm install
npm start
```
## run api
ensure you have python 3
```
cd back
pip install -r requirements.txt
python src/api.py
```

## run websocket
ensure you have python 3
```
cd back
pip install -r requirements.txt
python app.py
```


# How to run with windows
### run front
ensure you have nodejs v14
```
cd front
npm install
npm start
```
## run api
ensure you have python 3
```
cd back
pip install -r requirements.txt
python src/api.py
```

## run websocket
ensure you have python 3
```
cd back
pip install -r requirements.txt
python app.py
```

#test the application
\
after install the application, you need to open [http://localhost:3000](http://localhost:3000)
1.login screen
\
![Drag Racing](https://iacode.co/img/1.png)
2.choose user to play with
\
![Drag Racing](https://iacode.co/img/2.png)
3.start the game
\
![Drag Racing](https://iacode.co/img/3.png)

### The game have the next rules:
This is essentially connect-four, but the pieces stack on either side of the board instead of bottom-up.
Two players see a board, which is a grid of 7 rows and 7 columns. They take turn adding pieces to a row, on one of the sides. The pieces stack on top of each other, and the game ends when there are no spaces left available, or when a player has four consecutive pieces on a diagonal, column, or row.
