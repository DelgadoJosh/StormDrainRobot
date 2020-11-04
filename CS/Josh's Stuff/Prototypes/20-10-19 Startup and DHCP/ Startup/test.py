"""
Basically testing what happens when you run a script upon startup

python3 test.py

python3 "Desktop/TeamBlack/Github\ Repo/StormDrainRobot/CS/Josh\'s Stuff/Prototypes/20-10-19\ Startup/test.py"

/Desktop/TeamBlack/Github Repo/StormDrainRobot/CS/Josh's Stuff

Desktop/TeamBlack/Github\ Repo/StormDrainRobot/CS/Josh\'s\ Stuff/Prototypes/20-10-19\ Startup/

python3 Desktop/TeamBlack/Github\ Repo/StormDrainRobot/CS/Josh\'s\ Stuff/Prototypes/20-10-19\ Startup/test.py


Adjust test_script.sh

Then run command to make it runnable
chmod u+x test_script.sh

Then run it with:
./test_script.sh

Or
./Desktop/TeamBlack/Github\ Repo/StormDrainRobot/CS/Josh\'s\ Stuff/Prototypes/20-10-19\ Startup/test_script.sh

./~/Desktop/TeamBlack/Github\ Repo/StormDrainRobot/CS/Josh\'s\ Stuff/Prototypes/20-10-19\ Startup/test_script.sh


bash ~/Desktop/TeamBlack/Github\ Repo/StormDrainRobot/CS/Josh\'s\ Stuff/Prototypes/20-10-19\ Startup/test_script.sh

bash ~/Desktop/TeamBlack/Github\ Repo/StormDrainRobot/CS/Josh\'s\ Stuff/Prototypes/20-11-02\ Motors/startupScript.sh



Use to add startup tasks
crontab -e


@reboot /path/to/script

Rather:
@reboot bash ~/Desktop/...


Change editor:
select-editor



Alternatively:

sudo nano /etc/rc.local

Top line = #!/bin/bash
Then it'll run command as root

Then make sure it's runnable
sudo chmod a+x /etc/rc.local

Maybe /etc/rc.d/rc.local



"""

print("Hello World")