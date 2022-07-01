Using the doc in this page you will be able to configure pfsense and syslog-to-loki to receive pfsense log in loki.
As describe in this [documentation](https://docs.netgate.com/pfsense/en/latest/monitoring/logs/raw-filter-format.html) pfsense filterlog contains thos values, they will be extracted from the log and disponible in loki:
rule_number, sub_rule_number, anchor, tracker, interface, reason, action, direction, ip_version, tos, ecn, ttl, id, offset, flags, protocol_id, protocol, length, source_ip, destination_ip

# configur pfsense
In pfsense web gui go to : status -> system logs -> settings
- Enable remote logging
- Configure addres for the remote log server to the address of the server where syslog-to-loki is running
- Configure wht log to send

![pfsense screenshot](pfsense_config.png)

# run syslog-to-loki
Don't forget to configure env variable LOKI_URL to your loki server address
```
  syslog-to-loki:
    image: ghcr.io/nslythe/syslog-to-loki:latest
    container_name: syslog-to-loki
    labels:
      - "monitored=1"
    ports:
      - 514:514/udp
    environment:
      - LOKI_URL=[YOUR LOKI SERVER ADDRESS]
      - DISABLE_CONSOLE_LOG=1
      - MESSAGE_REGEX=(?P<rule_number>[^,]*),(?P<sub_rule_number>[^,]*),(?P<anchor>[^,]*),(?P<tracker>[^,]*),(?P<interface>[^,]*),(?P<reason>[^,]*),(?P<action>[^,]*),(?P<direction>[^,]*),(?P<ip_version>[^,]*),(?P<tos>[^,]*),(?P<ecn>[^,]*),(?P<ttl>[^,]*),(?P<id>[^,]*),(?P<offset>[^,]*),(?P<flags>[^,]*),(?P<protocol_id>[^,]*),(?P<protocol>[^,]*),(?P<length>[^,]*),(?P<source_ip>[^,]*),(?P<destination_ip>[^,]*)
    restart: unless-stopped
```
