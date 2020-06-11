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
