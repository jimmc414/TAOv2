import os
import shutil
import pandas as pd
from datetime import datetime, timedelta

class SharedUtilities:
    @staticmethod
    def create_directory(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def delete_directory(path):
        shutil.rmtree(path)

    @staticmethod
    def move_file(source, destination):
        shutil.move(source, destination)

    @staticmethod
    def copy_file(source, destination):
        shutil.copy2(source, destination)

    @staticmethod
    def read_csv(file_path):
        return pd.read_csv(file_path)

    @staticmethod
    def write_csv(dataframe, file_path):
        dataframe.to_csv(file_path, index=False)

    @staticmethod
    def read_excel(file_path):
        return pd.read_excel(file_path)

    @staticmethod
    def write_excel(dataframe, file_path):
        dataframe.to_excel(file_path, index=False)

    @staticmethod
    def get_date_range(start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        date_range = [start + timedelta(days=x) for x in range((end-start).days + 1)]
        return [date.strftime("%Y-%m-%d") for date in date_range]

    @staticmethod
    def validate_date_format(date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False