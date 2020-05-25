#!/bin/sh

printf "use 315\r\n\r\nclientlist\r\n\r\nquit\r\n\r\n" | nc $TS3ADDR $TS3PORT | grep clid | python3 display.py
