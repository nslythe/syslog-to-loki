# syslog-to-loki
Python server listening for syslog and sendiong them to loki server

https://datatracker.ietf.org/doc/html/rfc5424

# Running with docker
# Env variable
#### LISTEN_ADDRESS
Default value : 0.0.0.0:514
#### DISABLE_CONSOLE_LOG
If the env varuiable is set no log will be outputed to the console
#### MESSAGE_REGEX
Regex to parse the message section of the sys-log
#### LOKI_URL
