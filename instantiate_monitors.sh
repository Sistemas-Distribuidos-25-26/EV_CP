#!/bin/bash

if [ -z "$1" ]; then
  echo "Uso: $0 <numero_de_instancias>"
  exit 1
fi


run_in_terminal() {
  CMD=$1
  if command -v gnome-terminal &>/dev/null; then
    gnome-terminal -- bash -c "$CMD; exec bash"
  elif command -v xterm &>/dev/null; then
    xterm -e "$CMD; bash"
  elif command -v konsole &>/dev/null; then
    konsole -e bash -c "$CMD; exec bash"
  elif command -v screen &>/dev/null; then
    screen -dmS multi_instance bash -c "$CMD; exec bash"
    screen -r multi_instance
  else
    echo "No compatible terminal emulator found"
    exit 1
  fi
}

count=$1
for (( i=1; i<=count; i++ ))
do
  engine_port=$((14000+i))
  cp_id=$(printf "CP%03d" "$i")
  dash_port=$((7000+i))

  run_in_terminal "docker run --network ev_network -e PORT=$dash_port -p $dash_port:$dash_port -it --name monitor$i ev_cp_m engine$i $engine_port ev_central 10001 $cp_id"
done
