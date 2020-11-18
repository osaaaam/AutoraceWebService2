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
    s3_bucket = os.getenv('S3_BUCKET')

    def __init__(self):
        # self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')

    def put_file(self, file_name, file_body):
        s3_obj = self.s3_resource.Object(self.s3_bucket, file_name)
        s3_obj.put(ACL="public-read-write", Body=file_body)
