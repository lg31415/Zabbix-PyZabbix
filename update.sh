 while read host proxy ;do python zabbix_host_update.py -s http://zabbix.manager.cmcdn.cdn.10086.cn/api_jsonrpc.php -u Admin -p zabbix -H $host --proxy $proxy; done
