# CSC480_Poker_Bot


**Game Rules and Simplification**
- players: 2 (bot vs opponent)
- decisions: fold or stay (no betting)
  - decision points: before each phase (bot has 10 seconds to decide whether to fold or stay) 
- card dealing phases:
  - pre-flop: each player recieves 2 private cards (hole cards)
  - flop: 3 community cards are revealed
  - turn: 1 additional community card is revealed
  - river: 1 final community card is revealed
- hidden information:
  - bot can see its own hole cards and any revealed community cards
  - oppoonent's hole cards remain hidden unless both players stay until river
- win condition: neither player folds, highest ranking hand wins


**Implementation** 
- MCTS to estimate winning probability at each decision point
- each decision:
  - random rollouts (maximize number of simulations completed in 10 secs):
    - simulate random possible opponent hole cards
    - simulate random future community cards
    - play out to showdown randomly
  - selection policy:
    - UCB1 to guide exploration during simulations
    - tracks wins vs losses
    - calculate win probability-- wins / simulations
  - decision rule:
    - stay if >= 50%
    - fold if < 50%


**Set Up**
- card representation: using integers 0-51
  - (0-12) are clubs
  - (0-12) are diamonds
  - (0-12) are hearts
  - (0-12) are spades
- deck management: shuffling, drawing, no duplicate cards drawn, simulate from remaining deck correctly
- hand evaluation: determines hand rankings
  - rank all hands properly (royal flush > straight flush > four of a kind > etc)
