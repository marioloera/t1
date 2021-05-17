import os
from shutil import copy2

import pydata_google_auth
from google.cloud import bigquery


def main():

    # find .sql source code
    bqClient = BqClient()
    src_dir = os.path.dirname(os.path.realpath(__file__))
    copyCount = 0
    fileCount = 0
    deployCount = 0
    patch_name = next(os.walk(src_dir))[1][0]
    print(f"patch_name: {patch_name}")
    # patch = os.path.join("Patch", patch_name)
    for root, _, files in os.walk(src_dir):

        if patch_name not in root or "Patch_done" in root:
            continue

        for name in files:

            if ".sql" not in name:
                continue

            file = os.path.join(root, name)
            print(name)
            with open(file, "r", encoding="UTF-8") as f:
                sql = f.read()
                deployCount += bqClient.execute(sql)
                f.close()
            # copyCount += mv_file(filename=file,
            #              source_dir=patch, target_dir='DDL' )
            fileCount += 1
    print("_" * 50)
    print(f"fileCount: {fileCount}")
    print(f"deployCount: {deployCount}")
    print(f"copyCount: {copyCount}")


def mv_file(filename, source_dir, target_dir, keep_original=True):
    copied = 0
    new_destinantion = filename.replace(source_dir, target_dir)
    try:
        if keep_original:
            copy2(filename, new_destinantion)
            action = "Copied"
            copied = 1
        else:
            os.replace(filename, new_destinantion)
            action = "Moved"
        print(f"\n{action} from:\n {filename}\nto:\n {new_destinantion}")
    except Exception as ex:
        print(ex)
        pass
    return copied


class BqClient:
    def __init__(self):

        self.project_id = "valiant-striker-272613"
        scopes = [
            "https://www.googleapis.com/auth/bigquery",
        ]
        self.credentials = pydata_google_auth.get_user_credentials(
            scopes,
        )
        self.client = bigquery.Client(
            project=self.project_id, credentials=self.credentials
        )
        print("*************** bq init ***************")

    def execute(self, sql):
        query_job = self.client.query(sql)
        results = query_job.result()  # Waits for job to complete.
        print(results)
        return 1


if __name__ == "__main__":
    main()
