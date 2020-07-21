#TODO check if docker already installed, prompt if not to add user to group

# enable pigpio
sudo apt-get install -y pigpiod docker docker-compose npm
sudo systemctl enable --now pigpiod
sudo systemctl enable --now docker

# get latest angular frontend and deploy in nginx
echo `dirname "$0"`
cd nginx
FILE=./raspi-led-angular
if [ -d "$FILE" ]; then
    cd raspi-led-angular
    git pull
else
    git clone https://github.com/raphaka/raspi-led-angular
    cd raspi-led-angular
fi
npm install
ng build --prod --base-href="/"
cd ../..
docker-compose up --build
