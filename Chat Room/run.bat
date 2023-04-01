@REM Run chatroom server along with 2 clients for testing

start cmd /k "mode con: cols=50 lines=60 & python server.py"
start cmd /k "mode con: cols=50 lines=60 & python client.py admin adminpass"
start cmd /k "mode con: cols=50 lines=60 & python client.py GameTimeWA"
