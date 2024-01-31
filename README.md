# Python-Platformer


DONE:
- add health of the player
- touching fire should deal damage to the player
- if player lose all his health he should be reborned on the start of the level
- add up&down camera movement
- add music and welcome sound to the game

TODO:
- control the bottom death line (mark it), make possible levels can be "infinite" height
- add health bar
- add different types of ground (slippery, sticky, etc)
- add possibility to add shapes of any type as a ground of the level
- add level creator that will allow to draw levels
- add final point of the level if player is in the final point move him to the next level
- add moveable objects to the game
- add possibility to shoot the tongue and swing on it (if player in air)
- add abilities as a game progress (shooting, double jump, etc)
- add opponents to the game
- make opponents intelligent by coding some actions or using AI
- check possibility of using AI (chatGpt API) for upgrading player weapons and skills try to use data gathered by microphone
- add a lot of levels
- try to somehow check if levels are possible to be completed and try to balance them
- add different levels of difficulty by lowering player power and making opponents stronger
- add more sounds (player sounds), enemy sounds, etc.
- play with sounds make them stereo (left, right)
```
chanel = pygame.mixer.Channel(7)
chanel.set_volume(0, 1)
snoring = pygame.mixer.Sound('assets/Sound/Sounds/snoring.mp3')
chanel.play(snoring)
```

ABANDONED:
- if player is already in air he should be able to only jump once (??)