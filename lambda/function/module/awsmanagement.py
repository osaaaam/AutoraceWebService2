import os
import boto3


class Rds:
    # インスタンス名取得
    db_instance = os.getenv('DB_INSTANCE')

    def __init__(self):
        self.rds_client = boto3.client('rds')

    # RDSステータス確認
    def get_status(self):
        response = self.rds_client.describe_db_instances(DBInstanceIdentifier=self.db_instance)
        return response["DBInstances"][0]["DBInstanceStatus"]

    # RDS起動
    def start(self):
        # ステータスが停止であれば起動
        if self.get_status() == "stopped":
            self.rds_client.start_db_instance(DBInstanceIdentifier=self.db_instance)

    # RDS停止
    def stop(self):
        # ステータスが稼働中であれば停止
        if self.get_status() == "available":
            self.rds_client.stop_db_instance(DBInstanceIdentifier=self.db_instance)


class S3:
    # S3バケット名取得
    s3_bucket_data = os.getenv('S3_BUCKET_DATA')
    s3_bucket_data_daily = os.getenv('S3_BUCKET_DATA_DAILY')
    s3_bucket_data_anaylize = os.getenv('S3_BUCKET_DATA_ANAYLIZE')

    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')

    def put_file(self, file_name, file_body, s3_bucket):
        s3_obj = self.s3_resource.Object(s3_bucket, file_name)
        s3_obj.put(ACL="public-read-write", Body=file_body)

    def get_file(self, file_name, s3_bucket):
        s3_obj = self.s3_client.get_object(Bucket=s3_bucket, Key=file_name)
        return s3_obj['Body'].read().decode('utf-8').split()

    def get_filelist(self, s3_bucket):
        l_file = []
        s3_list_objects = self.s3_client.list_objects_v2(Bucket=s3_bucket)
        # 0件でなければ
        if s3_list_objects['KeyCount'] != 0:
            for s3_list_object in s3_list_objects['Contents']:
                # フォルダ/ファイル名をappend
                l_file.append(s3_list_object['Key'])
        return l_file

    def delete_file(self, file_name, s3_bucket):
        self.s3_client.delete_object(Bucket=s3_bucket, Key=file_name)
