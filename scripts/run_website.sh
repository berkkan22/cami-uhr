#!/bin/bash

# Variables
SESSION_NAME="prayer_times"
COMMAND="source ~/.bashrc && cd /home/pi/cami-uhr && npm run dev"

# Check if tmux session exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
  # If session doesn't exist, create a new one and run the command
  tmux new-session -d -s $SESSION_NAME
  tmux send-keys -t $SESSION_NAME "$COMMAND" C-m
else
  # If session exists, send the command to the existing session
  tmux send-keys -t $SESSION_NAME "$COMMAND" C-m
fi

# Attach to the session (optional)
# tmux attach -t $SESSION_NAME