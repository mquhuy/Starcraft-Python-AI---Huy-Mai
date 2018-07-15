Update: Jul 15th, 2018: Trained the model. Now the bot can play sufficiently better than it would without the model. Unfortunately, the model file is too heavy (> 400 MB), and cannot be uploaded to Github, but you should get a somewhat similar model by running the training-model.py file.

This is an AI that plays the game Starcraft II. Play the game by the file startgame.py

(Change difficulty level by replacing "Hard" in <i>Computer(Race.Terran, Difficulty.Hard)</i> with the difficult level you want.)

Note: Change the value of os.environ["SC2PATH"] in the file to your correct Starcraft II folder.
