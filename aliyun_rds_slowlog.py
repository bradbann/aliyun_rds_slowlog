# -*- coding: utf-8 -*-
"""rds_slow_log.py

A few Python classes that help with finding slow queries on Aliyun RDS.



"""

__author__ = "Li Guanghui"


import json
from aliyunsdkcore import client as ali_sdk_client
from aliyunsdkrds.request.v20140815 import DescribeSlowLogsRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest


class Connection(object):

    def __init__(self, aliyun_access_key, aliyun_access_secret):
        self.aliyun_access_key = aliyun_access_key
        self.aliyun_access_secret = aliyun_access_secret
        self._connection = ali_sdk_client.AcsClient(aliyun_access_key, aliyun_access_secret)
    
    def get_db_instances(self, aliyun_region, page_size=30, page_number=1):
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_accept_format('json')
        request.add_query_param('RegionId', aliyun_region)
        request.add_query_param('PageSize', page_size)
        request.add_query_param('PageNumber', page_number)
        response = self._connection.do_action(request)
        instance_dict = json.loads(response)

        instances = list()
        for instance in instance_dict['Items']['DBInstance']:
            instance = Instance(instance['DBInstanceId'], instance['DBInstanceDescription'], instance['RegionId'])
            instances.append(instance)

        return instances
    
    def get_slow_logs(self, db_instance_id, start_date, end_date, page_size=30, page_number=1):
        request = DescribeSlowLogsRequest.DescribeSlowLogsRequest()
        request.set_accept_format('json')
        request.add_query_param('DBInstanceId', db_instance_id)
        request.add_query_param('StartTime', start_date + 'Z')
        request.add_query_param('EndTime', end_date + 'Z')
        request.add_query_param('PageSize', page_size)
        request.add_query_param('PageNumber', page_number)
        response = self._connection.do_action(request)
        slow_log_dict = json.loads(response)

        slow_logs = list()
        for slow_log in slow_log_dict['Items']['SQLSlowLog']:
            slow_log = SlowLog(
                slow_log['DBName'],
                slow_log['CreateTime'],
                slow_log['SQLId'],
                slow_log['SlowLogId'],
                slow_log['SQLText'],
                slow_log['MaxExecutionTime'],
                slow_log['ReturnMaxRowCount'],
                slow_log['ReturnTotalRowCounts'],
                slow_log['ParseMaxRowCount'],
                slow_log['ParseTotalRowCounts'],
                slow_log['MaxLockTime'],
                slow_log['TotalLockTimes'],
                slow_log['MySQLTotalExecutionCounts'],
                slow_log['MySQLTotalExecutionTimes']
            )
            slow_logs.append(slow_log)

        return slow_logs

        

class Instance(object):

    def __init__(self, instance_id, instance_description, region='cn-shanghai'):
        self.instance_id = instance_id
        self.instance_description = instance_description
        self.region = region

    def __repr__(self):
        return "<Instance: %s(%s)>" % (self.instance_description, self.instance_id)

    def is_prod(self):
        if self.instance_description[:4] == 'prod':
            return True
        return False

    @staticmethod
    def get_all_db_instances(connection: Connection, region):
        page_size = 100
        page_number = 1
        current_db_instances = connection.get_db_instances(region, page_size, page_number)
        all_db_instances = current_db_instances
        while len(current_db_instances) == page_size: 
            page_number = page_number + 1
            current_db_instances = connection.get_all_db_instances(region, page_size, page_number)
            all_db_instances.extend(current_db_instances)
        return all_db_instances

    def get_all_slow_logs(self, connection: Connection, start_date, end_date):
        page_size = 100
        page_number = 1
        current_slow_logs = connection.get_slow_logs(self.instance_id, start_date, end_date, page_size, page_number)
        all_slow_logs = current_slow_logs
        while len(current_slow_logs) == page_size:
            page_number = page_number + 1
            current_slow_logs = connection.get_slow_logs(self.instance_id, start_date, end_date, page_size, page_number)
            all_slow_logs.extend(current_slow_logs)
        return all_slow_logs


class SlowLog(object):

    def __init__(self, db_name, create_time, sql_id, slow_log_id, sql_text, max_execution_time,
                return_max_row_count, return_total_row_counts,
                parse_max_row_count, parse_total_row_counts,
                max_lock_time, total_lock_times,
                mysql_total_execution_counts, mysql_total_execution_times
                ):
        self.db_name = db_name
        self.create_time = create_time
        self.sql_id = sql_id
        self.slow_log_id = slow_log_id
        self.sql_text = sql_text
        self.max_execution_time = max_execution_time
        self.return_max_row_count = return_max_row_count
        self.return_total_row_counts = return_total_row_counts
        self.parse_max_row_count = parse_max_row_count
        self.parse_total_row_counts = parse_total_row_counts
        self.max_lock_time = max_lock_time
        self.total_lock_times = total_lock_times
        self.mysql_total_execution_counts = mysql_total_execution_counts
        self.mysql_total_execution_times = mysql_total_execution_times
    
    def __repr__(self):
        return "<Slow Log: %s>" % self.slow_log_id


def main():
    pass

if __name__ == '__main__':
    main()