Welcome to the Market-based Multiagent Systems experimental Pac-Man package!
Please find the "Pacman" folder alongside this readme file. The Auction Method algorithm can be found in the ghostAgents.py file. Inside, the AuctionGhost agent can be found, along with the MultiGhostAgent parent class that takes care of the auctions.
The pacman agent that uses the Markov Decision Process can be found in mdpAgents.py

 --- SETUP INSTRUCTIONS --- 
To get set up with this modified version of the UC Berkeley Pac-Man package, please place this "Source_Code" folder in a directory you can navigate into using the command line interface.

 --- VARIABLE INFORMATION FOR RUN COMMANDS --- 
Please note that to run experiments equivalent to the ones run in the report, only certain command line arguments were used. These are listed next to the argument identifiers as a list:

-g (Ghost agent): 	[AuctionGhost]
-p (Pacman agent): 	[MDPAgent]
-l (Map layout): 	[smallClassic, mediumClassic, originalClassic]
-k (Number of ghosts): 	[1, 2, 3, 4] 	NOTE: values 3 and 4 are only valid on the originalClassic map layout.

 --- CHANGING EXPERIMENTAL AUCTION VARIABLES --- 
Variables relevant to the auction method implemented can be changed in the AuctionVars.csv file. Only values on the 2nd line can be changed. Namely, these values are:

INTERVAL:	[1, 2, 4]
MODE:		[FOOD, CAP]
PRINT:		[FALSE, TRUE]

These variables only apply when the AuctionGhost ghost agent has been specified in the run command. NOTE: these values will work for any of the map layouts listed above and any number of ghost agents also listed above. Using values for MODE and PRINT other than the ones listed may not work.

 --- RUN INSTRUCTIONS --- 
To run a single game of Pac-Man using the MDP Pacman agent and the Auction Ghost agents, please navigate into the "Pacman" folder on the command line and run the one of the following commands:

smallClassic map with 1 ghost:
> python pacman.py -g AuctionGhost -p MDPAgent -l smallClassic -k 1
smallClassic map with 2 ghosts:
> python pacman.py -g AuctionGhost -p MDPAgent -l smallClassic -k 2

mediumClassic map with 1 ghost:
> python pacman.py -g AuctionGhost -p MDPAgent -l mediumClassic -k 1
mediumClassic map with 2 ghost:
> python pacman.py -g AuctionGhost -p MDPAgent -l mediumClassic -k 2

originalClassic map with 1 ghost:
> python pacman.py -g AuctionGhost -p MDPAgent -l originalClassic -k 1
originalClassic map with 2 ghost:
> python pacman.py -g AuctionGhost -p MDPAgent -l originalClassic -k 2
originalClassic map with 4 ghost:
> python pacman.py -g AuctionGhost -p MDPAgent -l originalClassic -k 3
originalClassic map with 5 ghost:
> python pacman.py -g AuctionGhost -p MDPAgent -l originalClassic -k 4

To run 100 games without the interface for testing purposes, please change the PRINT variable inside the AuctionVars.csv file to FAlSE and save the file. You can then run the following command:

> python pacman.py -g AuctionGhost -p MDPAgent -l smallClassic -k 1 -q -n 100

Where the -q argument disables the Pac-Man interface and the number after the -n argument controls the number of games to run. Again, the -l (Map layout) and -k (Number of ghosts) arguments can be changed as mentioned above.

Once the -n number of games have been run, the average score of all the games, the score in each game, the win rate across the games and the win record of each game is printed to the console.