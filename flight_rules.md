# Things you need to know

## 1- Firmare Installation for Power Distribution PIs


- To obtain IPs of chargers that are currently on, go under '~/git/power_distribution/interfacing' and write:
```
sudo python3 get_ip_by_mac.py ../config/mac_list.json wlp5s0

```
First argument is the json file containing all the ip addresses and second argument is the interface.

- ssh into the desired charger
- Check if git and docker are installed
- If git is not there:
```
sudo apt-get install git
```
- Install power_distribution repo (includes firmware file that we need to run):
```
git clone https://github.com/robotarium/power_distribution
```
- Change rc.local file so that all the necessary software is installed on the next startup
```
sudo nano /etc/rc.local
```
Note: Add the line "/home/pi/setup_service start" right before "exit 0" (last line).
- Move Files named 'setup' and 'setup_service' (under power_distribution/setup/) to /home/pi/ (aka ~) 
- Restart PI to install firmware
```
sudo shutdown -r now
```
- Note
No need to remove the line we added to rc.local since the files "setup" & "setup_service" will be automatically removed upon the completion of the installation.
- Note 2
Normally, setup files should be already there already and installation should automatically happen upon the first boot. This is thanks to the fact that we already add the setup files when we flash the SD card.
- To check what's going on with the installation
This assuming that you gave the PI enough time to reboot of course.
Re-ssh into the PI and run:
```
tail -f /var/log/setup_firmware.log 
```
The command simply tells you what the log file contains. You should see it installing the different pieces of software such as python and docker.

- To check if everything is working after installation 
While ssh-ed, run:
```
docker ps
```
To know which containers are running.

You can also run:
```
docker logs firmware --follow --tail 50
```
To know what the container firware is printing for example. 
Note: The flag "follow" is to show what's being printed in a live fashion. The flag "tail" simply shows you the last x lines (in this case 50).

## 1- How to Add A Modification to the Repository

- The idea here is that after every modification, we push the edit to github, and rebuild the docker container then also push the container. Ideally, the watchtowers on the chargers would then detect the update and pull it. 
- The first thing after editing your desired file in the repo 'power_distribution' is to navigate to that repo in a terminal.
- Then run (you might need to use sudo):
```
git add -u
git status
git commit -m 'comment on the update...'
git push
```
- Then navigate to the 'power_distribution/docker' repo and re-build the container:
```
sudo ./docker_build.sh 192.168.1.8 1884
```
The first argument in that command is the ip address of the router. That ip address can be retrieved by running 'ifconfig' in any terminal on the main computer. The second argument in that command is the port being used. 
"Think of the IP-address as the building address and the port as the apt#" - Paul
- Next, we want to push the container we just built:
```
sudo ./docker_push.sh
```
- Congrats! We are done. Now, we just want to check if the chargers got the updated version. Various ways of doing this is possible. One way is to ssh into one of the power stations (check part 1 of this guide) and check the watchtower log. 
