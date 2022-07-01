# syslog-to-loki
Python server listening for syslog and sendiong them to loki server

https://datatracker.ietf.org/doc/html/rfc5424

# Running with docker
# Env variable
#### LOKI_URL
The url of your loki server, this variable is mandatory.
Ex: http://loki:3100/loki/api/v1/push
#### LISTEN_PORT
Default value : 514
#### DISABLE_CONSOLE_LOG
If the env varuiable is set no log will be outputed to the console
Default this value is not set.
#### MESSAGE_REGEX
Regex to parse the message section of the sys-log
Default this value is empty

