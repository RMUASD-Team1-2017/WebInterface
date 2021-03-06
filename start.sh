#!/bin/bash
#start rabbitmq
rabbitmq-server &
sleep 10
rabbitmqctl add_user drone drone
rabbitmqctl set_permissions -p / drone ".*" ".*" ".*"
rabbitmqctl set_user_tags drone administrator
if [ "$1" == "run" ]; then
  ./run.sh
elif [ "$1" == "test" ]; then
  ./test.sh
else
echo "Not a valid command, only test and run are valid!"
exit 1
fi
