#!/bin/bash

ps aux | awk '{if($3>95) print $2}' | while read pid; do
    kill -9 $pid
done