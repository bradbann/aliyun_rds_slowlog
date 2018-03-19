# aliyun_rds_slowlog

A few Python classes that help with finding slow queries on Aliyun RDS.

## Dependencies

Written with Python 3.6.4. Not tested on other versions.

- aliyunsdkcore
- aliyun-python-sdk-rds

```Shell
$ pip install -r requirements.txt
```

## Example

```Python
# Import "Connection" and "Instance" classes
>>> from aliyun_rds_slowlog import Connection, Instance

# Create a Connection instance
>>> my_connection = Connection(aliyun_access_key='HbF7vjeBs58KEt7t',
                               aliyun_access_secret='h3UXzNQKWcYJ9tUwFFPnuvb5Ss38EA')

# Get all rds instances with a static method in "Instance"
>>> all_db_instances = Instance.get_all_db_instances(my_connection, region='cn-shanghai')

# Get all slow logs of an rds instance within a period of time.
>>> slow_logs = all_db_instances[0].get_all_slow_logs(my_connection,
                                        start_date='2018-01-01',
                                        end_date='2018-01-10')
>>> print(slow_logs)
[<Slow Log: 887202079394340864>, <Slow Log: 887202079088156672>]

# Some details of a slow log.
>>> slow_logs[0].db_name
'my_web'
>>> slow_logs[0].max_execution_time
1
>>> slow_logs[0].parse_total_row_counts
2938392
```

## Classes, methods and properties

### *class* **Connection** (aliyun_access_key, aliyun_access_secret)

A reusable connection class that contains access key and secret.

```Python
>>> my_connection = Connection(aliyun_access_key='HbF7vjeBs58KEt7t',
                    aliyun_access_secret='h3UXzNQKWcYJ9tUwFFPnuvb5Ss38EA')
```

#### *method* Connection.**get_db_instances**(self, aliyun_region, page_size=30, page_number=1)

Return a list of rds instances based on given page_size and page_number.

```Python
>>> my_connection.get_db_instances(region='cn-shanghai')
[<Instance: prod_web_db(rm-uf6plmdubpg2oqsqr)>, <Instance: prod_service_member_db(rm-uf6rea7r139f5r95e)>]
```

*page_size* defaults to 30.

*page_number* defaults to 1.

>**Notice**: this method may not return ALL of your instances. Use *Instance*.**get_all_db_instances(\*args)** instead.

#### *method* Connection.**get_slow_logs**(self, db_instance_id, start_date, end_date, page_size=30, page_number=1)

Return a list of slow logs of an rds instance based on given page_size and page_number.

```Python
>>> my_connection.get_slow_logs(db_instance_id='rm-uf6plmdubpg2oqsqr',
                                start_date='2018-01-01',
                                end_date='2018-01-10')
[<Slow Log: 887202079394340864>, <Slow Log: 887202079088156672>]
```

*page_size* defaults to 30.

*page_number* defaults to 1.

>**Notice**: this method may not return ALL slow logs of an instance. Use *Instance*.**get_all_slow_logs(\*args)** instead.

### *class* **Instance** (instance_id, instance_description, region='cn-shanghai')

A class that represents an Aliyun RDS instance.

>Notice: Instantiate an "instance" is not recommended, use `Instance.get_all_db_instances()` or `Connection.get_db_instances()` instead.

#### *staticmethod* Instance.**get_all_db_instances**(connection: Connection, region)

Return a list of all Aliyun RDS instances within a region.

```Python
>>> Instance.get_all_db_instances(my_connection, region='cn-shanghai')
[<Instance: prod_web_db(rm-uf6plmdubpg2oqsqr)>, <Instance: prod_service_member_db(rm-uf6rea7r139f5r95e)>]
```

#### *method* Instance.**is_prod**()

Return true if `Instance.instance_description` starts with "prod".

#### *method* Instance.**get_all_slow_logs**(self, connection: Connection, start_date, end_date)

Return a list of all slow logs of an instance within a period of time.

```Python
>>>my_instance = get_all_slow_logs(my_connection, start_date='2018-01-01', end_date='2018-01-10')
[<Slow Log: 887202079394340864>, <Slow Log: 887202079088156672>, <Slow Log: 886115004129583104>]
```

### *class* **SlowLog** (db_name, create_time, sql_id, slow_log_id, sql_text, max_execution_time,return_max_row_count, return_total_row_counts, parse_max_row_count, parse_total_row_counts, max_lock_time, total_lock_times, mysql_total_execution_counts, mysql_total_execution_times)

A class that represents a slow query log.

>Notice: Instantiate a "SlowLog" is not recommended, use `Instance.get_all_slow_logs()` or `Connection.get_slow_logs()` instead.

#### *variable* SlowLog.**db_name**

Name of the database.

```Python
>>> my_slow_log.db_name
'my_web'
```

#### *variable* SlowLog.**create_time**

The time this SQL gets created.

```Python
>>> my_slow_log.create_time
'2018-01-08Z'
```

#### *variable* SlowLog.**sql_id**

ID of this SQL.

```Python
>>> my_slow_log.sql_id
887032195117060096
```

#### *variable* SlowLog.**slow_log_id**

ID of this slow query log.

```Python
>>> my_slow_log.slow_log_id
887202079394340864
```

#### *variable* SlowLog.**sql_text**

Text of this SQL.

```Python
>>> my_slow_log.sql_text
'select * from my_table'
```

#### *variable* SlowLog.**max_execution_time**

Longest time this SQL has ever executed.

```Python
>>> my_slow_log.max_execution_time
1
```

#### *variable* SlowLog.**return_max_row_count**

Maximum row counts this SQL has ever returned.


```Python
>>> my_slow_log.return_max_row_count
1141
```

#### *variable* SlowLog.**return_total_row_counts**

Total row counts this SQL returned.

```Python
>>> my_slow_log.return_total_row_counts
1141
```

#### *variable* SlowLog.**parse_max_row_count**

Maximum row counts this SQL has ever parsed.

```Python
>>> my_slow_log.parse_max_row_count
2938392
```

#### *variable* SlowLog.**parse_total_row_counts**

Total row counts this SQL parsed.

```Python
>>> my_slow_log.parse_total_row_counts
2938392
```

#### *variable* SlowLog.**max_lock_time**

Maximum lock time results from this SQL.

```Python
>>> my_slow_log.max_lock_time
0
```

#### *variable* SlowLog.**total_lock_times**

Total lock time results from this SQL.

```Python
>>> my_slow_log.total_lock_times
0
```

#### *variable* SlowLog.**mysql_total_execution_counts**

Number of times this SQL has been executed.

```Python
>>> my_slow_log.mysql_total_execution_counts
1
```

#### *variable* SlowLog.**mysql_total_execution_times**

Total amount of time spent executing this SQL.

```Python
>>> my_slow_log.mysql_total_execution_times
1
```

## Reference

More details can be found on Aliyun doc site.

- https://help.aliyun.com/document_detail/26289.html?spm=a2c4g.11186623.6.897.OoxtE8
