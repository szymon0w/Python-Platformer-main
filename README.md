# Python-Platformer


DONE:
- add health of the player
- touching fire should deal damage to the player
- if player lose all his health he should be reborned on the start of the level
- add up&down camera movement
- add music and welcome sound to the game

TODO:
- consult with the game developer and writer about the story
- think about adding new developer to help you
- change the look of the background add different themes, investigate if you can change everything to be darker or brighter
- write unit tests for current functions
- investigate possibility of writing automatic tests
- control the bottom death line (mark it), make possible levels can be "infinite" height
- add health bar
- add player statistics like (agility, strength, knowledge, charisma, reputation itp..) and block some abilities or make them stronger/weaker based on that
- add different types of ground (slippery, sticky, etc)
- add possibility to add shapes of any type as a ground of the level
- add level creator that will allow to draw levels
- add final point of the level if player is in the final point move him to the next level
- add moveable objects to the game
- add some traps to the levels
- add abilities as a game progress (shooting, double jump, grabbing things, hitting, assasination, sneaking etc..)
- add opponents to the game
- add attacking and some weapons
- add opponents vision to the game to play 
- make opponents intelligent by coding some actions or using AI
- check possibility of using AI (chatGpt API) for upgrading player weapons and skills try to use data gathered by microphone
- add more sounds (player sounds), enemy sounds, etc. and play with sounds make them stereo (left, right)
```
chanel = pygame.mixer.Channel(7)
chanel.set_volume(0, 1)
snoring = pygame.mixer.Sound('assets/Sound/Sounds/snoring.mp3')
chanel.play(snoring)
```
- add a lot of levels with different themes (look and sound)
- add map of the city with smith, alchemist, magicians, quests, etc. and possibility to move around the map
- add possibility to talk with people on the map using your microphone (QA?, chatGPT?)
- maybe add allies to the game that will fight among with you
- try to somehow check if levels are possible to be completed and try to balance them
- add different levels of difficulty by lowering player power and making opponents stronger
- if there is no possibility of completing level player should be able to back up and train or exchange some abilities for another


RULES:
- write unit tests for functions
- use design patterns
- add possibility to shoot the tongue and swing on it (if player in air) (if frog)



ABANDONED:
- if player is already in air he should be able to only jump once (??)