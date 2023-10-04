# flappy-bird-AI-game
Flappy bird made using AI Reinforcement Learning

Code written using object oriented Principle

First commit Lib used :-
    > pip install pygame
    > pip install neat-python

Creting 3 Objects 
    1. Bird
    2. Pipe 
    3. Ground

Velocity Concept
    UP & LEFT = -ve velocity
    Right & Bottom = +ve velocity


AI Part
  > Consists of 
    1. Input (Birds , Top Pipe , Bottom Pipe)
    2. OutPut (Jump ? )
    3. Activation Function ( TanH )
    4. Population Size 100 ( How these birds will get better )
    5. Fitness Function ( Distance )
    6. Max Generation ( 30 )

Final Part when we get the best bird among the birds we save it (here) known as Pickle
 > so , we pickle out the best bird