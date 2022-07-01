# syslog-to-loki
Python server listening for syslog and sendiong them to loki server

https://datatracker.ietf.org/doc/html/rfc5424

# Running with docker
<<<<<<< HEAD
<img src="../assets/docker-logo.svg">
=======
>>>>>>> ad61b6dff03d3c5f8a5fdd4ef89d9b9830bc87e3

# Env variable
#### LISTEN_ADDRESS
Default value : 0.0.0.0:514
#### DISABLE_CONSOLE_LOG
If the env varuiable is set no log will be outputed to the console
#### MESSAGE_REGEX
Regex to parse the message section of the sys-log
#### LOKI_URL
