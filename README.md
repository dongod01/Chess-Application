# Chess-Application

## Aim of the Project

With the advent of online chess, there are challenges at the top level in the sport. One of the biggest problems faced is "Mouseslips", i.e. making a wrong move accidentally. The intention of starting this project is to minimize such distractions, with the use of button based sound input.

## Salient Features

The application is designed to be played between two players over the internet from any location. One player chooses to be the server, while the other becomes the client. After the connection between the two is established, both players are asked for color preferences, and when opposite colors are chosen, the game begins in a separate window.

The user interface of the game has been designed to precision. All the basic features of online chess are available in-game, such as playing moves, resign, draw, etc. The user can give speech input for each move. All the moves played are displayed as a table. Whenever a game ends, suitable messages are displayed regarding it. Additionally, at the end, a downloadable PGN for the game is available at each players' end in the main window. 

## How to use

### Setup

The setup is a one time process.

1. Clone this github project as a local repository. Alternatively, use  https://downgit.github.io/#/home to download the repository locally.
2. Windows Users: 
    Install Python from the official website, https://www.python.org/downloads/
    Windows users need to run the "install.bat" file to install all the python libraries necessary (Run this bat as an administrator).
3. Linux/MacOS/UNIX Users:
    Make the install.sh file executable using this command in the terminal opened in the downloaded/cloned directory:        sudo chmod +x install.sh
    You need to run the "install.sh" file to install all the python libraries necessary        ./install.sh

### Starting the game

1. Enter your name in the text box.
2. Mutually decide on becoming either the server/client with the opponent.
3. (i) If you choose to be the server,  select the server option and send the displayed IP address on your interface to your opponent.
   (ii) If are the client, select the client option . Next, get the IP address from your opponent and enter it. The port number is 8080 always.
4. Choose the colors as white/w or black/b.If you and your opponent choose same colours, the text boxes will be refreshed and you need to choose again. The moment opposite       colors are chosen, the game will begin.

### Playing the game

1. The game opens in a separate window. To move a piece, choose the square in which the piece is located and the destination square. If the move is legal, it will be played, else you need to go again.
2. To play using speech input, select the "Speak!" button and speak. For example, you are playing the first move e4. You need to speak this move as " e2 e4 ", with the initial and final squares for any piece. If the input is accepeted, the move will be played, else you will be notified and you can repeat this step all over again.(*)
3. During the game, if you wish to resign/draw at any point you can select the options provided. If your opponent does the same, you will be notified accordingly and the games ends.
4. After the game has ended you can get the PGN of the game from the main window, and save it at a desired location locally. You can use the Games folder in the directory to store the game.
5. Close the application.


Notes:
1. (*) The sound feature is presently in Beta version. It will be improved in the future updates.
2. The application may be updated by using the command in a terminal opened in the same directory: "git pull" 
