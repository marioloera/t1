#!/usr/bin/env python3
import os
import time
from google.cloud import bigquery
import pydata_google_auth
import sys


def main():
    file_count = 0
    runnining_time = time.time()
    fileformat = 'json'
    #fileformat = 'avro'
    directory = os.path.join('..', 'samplefiles', fileformat + 'files')
    bq_loaded_directory = os.path.join('..', 'samplefiles', 'bq_loaded')

    bqClient = BqClient(type=fileformat)
    max_files = 3
    print('loanding files up to:', max_files)
    for filename in os.listdir(directory):
        if not fileformat in filename:
            continue
        if file_count >= max_files:
            break
        print('loading:', filename)
        bqClient.load_file(os.path.join(directory, filename))

        os.replace(os.path.join(directory, filename),
                   os.path.join(bq_loaded_directory, filename))

        file_count += 1

    print('file_count:', file_count)
    print('runnining_time:', time.time() - runnining_time)


class BqClient():

    def __init__(self, type):
        # client = bigquery.Client()
        self.project_id = 'valiant-striker-272613'
        self.dataset_id = 'Flights'
        self.table_id = 'Routes'
        self.credentials = pydata_google_auth.get_user_credentials(
            ['https://www.googleapis.com/auth/bigquery'],)
        self.client = bigquery.Client(project=self.project_id,
                                      credentials=self.credentials)
        self.dataset_ref = self.client.dataset(self.dataset_id)
        self.job_config = bigquery.LoadJobConfig()

        if type == 'avro':
            self.init_avro()
        else:
            self.init_json()

    def init_avro(self):
        self.table_ref = self.dataset_ref.table(self.table_id)
        self.job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        # WRITE_TRUNCATE WRITE_APPEND WRITE_EMPTY
        self.job_config.source_format = bigquery.SourceFormat.AVRO
        self.job_config.use_avro_logical_types = True

    def init_json(self):
        self.table_ref = self.dataset_ref.table(self.table_id)
        self.job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        # WRITE_TRUNCATE WRITE_APPEND WRITE_EMPTY
        self.job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    def load_file(self, file):
        with open(file, "rb") as source_file:
            job = self.client.load_table_from_file(source_file,
                                                   self.table_ref,
                                                   job_config=self.job_config)

        job.result()  # Waits for table load to complete.
        print("Loaded {} rows into \n`{}.{}.{}`".format(job.output_rows,
                                                        self.project_id,
                                                        self.dataset_id,
                                                        self.table_id))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    main()
