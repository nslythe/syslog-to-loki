# configuration with pfsense
## pfsense
Go to : status -> system logs -> settings
- Enable remote logging
- Configure addres for the remote log server to the address of the server where syslog-to-loki is running
- Configure wht log to send

![pfsense screenshot](pfsense_config.png)

Run syslog-to-loki
```
  syslog-to-loki:
    image: ghcr.io/nslythe/syslog-to-loki:latest
    container_name: syslog-to-loki
    labels:
      - "monitored=1"
    ports:
      - 514:514/udp
    environment:
      - LOKI_URL=http://curie.home.slythe.net:3100/loki/api/v1/push
      - DISABLE_CONSOLE_LOG=1
      - MESSAGE_REGEX=(?P<rule_number>[^,]*),(?P<sub_rule_number>[^,]*),(?P<anchor>[^,]*),(?P<tracker>[^,]*),(?P<interface>[^,]*),(?P<reason>[^,]*),(?P<action>[^,]*),(?P<direction>[^,]*),(?P<ip_version>[^,]*),(?P<tos>[^,]*),(?P<ecn>[^,]*),(?P<ttl>[^,]*),(?P<id>[^,]*),(?P<offset>[^,]*),(?P<flags>[^,]*),(?P<protocol_id>[^,]*),(?P<protocol>[^,]*),(?P<length>[^,]*),(?P<source_ip>[^,]*),(?P<destination_ip>[^,]*)
    restart: unless-stopped
```
