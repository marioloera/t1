
# run
 - python src/flights.py
 - python src/flights.py --output_file=output_data\output.csv

# to measure time in unix or windows git bash:
 - time python src/flights.py
 - time python src/flights_pd.py

# profile using cProfile:
 - python -m cProfile src/flights.py ..\output_data\output.csv
 - python -m cProfile -o output_data/flights_profile.out src/flights.py
 - python -m cProfile -o output_data/flights_pd_profile.out src/flights_pd.py

# test
 - make test
 - python -m pytest

# creating new credentials BigQuery:
run the command below, open the url link and login with the credentiasl
you will get a token and a button to copy,
paste the tocken in the command line and credentials will be generated
# python -m pydata_google_auth login file_path.json
# python -m pydata_google_auth login ~/keys/google_credentials.json
python -m pydata_google_auth login --scopes https://www.googleapis.com/auth/bigquery ~/keys/google_credentials.json
