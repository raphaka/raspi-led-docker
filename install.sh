# enable pigpio
sudo apt-get install pigpiod docker docker-compose
sudo systemctl enable --now pigpiod

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
