# syslog-to-loki
Python server listening for syslog and sendiong them to loki server.
I wrote this server in replacement of syslog-ng and promtail combo. I found this solution dificult to understand.
I use this solution with pfsense and loki. To see my solution I wrote a page explaining how to configure syslog-to-loki with pfsense.

This syslog server is targeted to support [rfc5424](https://datatracker.ietf.org/doc/html/rfc5424)
The section [TODO](todo) contains task planned to achieve this goal.

# Running
## docker
```
docker run -p 514:514/udp -e LOKI_URL=http://loki:3100/loki/api/v1/push ghcr.io/nslythe/syslog-to-loki
```
## docker-compose 
```
  syslog-to-loki:
    image: ghcr.io/nslythe/syslog-to-loki:latest
    container_name: syslog-to-loki
    labels:
      - "monitored=1"
    ports:
      - 514:514/udp
    environment:
      - LOKI_URL=http://loki:3100/loki/api/v1/push
      - DISABLE_CONSOLE_LOG=1
```

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
##### Regex example
- pfsense
```
(?P<rule_number>[^,]*),(?P<sub_rule_number>[^,]*),(?P<anchor>[^,]*),(?P<tracker>[^,]*),(?P<interface>[^,]*),(?P<reason>[^,]*),(?P<action>[^,]*),(?P<direction>[^,]*),(?P<ip_version>[^,]*),(?P<tos>[^,]*),(?P<ecn>[^,]*),(?P<ttl>[^,]*),(?P<id>[^,]*),(?P<offset>[^,]*),(?P<flags>[^,]*),(?P<protocol_id>[^,]*),(?P<protocol>[^,]*),(?P<length>[^,]*),(?P<source_ip>[^,]*),(?P<destination_ip>[^,]*)
```


# TODO
