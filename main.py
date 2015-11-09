import os
from os.path import join, dirname
import json
import yaml
import subprocess
import sqlalchemy as sa
import csv
from slugify import slugify
from dotenv import load_dotenv

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get('DATABASE_URL')

# Clean list of headers by removing special chars and spaces
def clean_headers(headers):
	clean_headers = []
	for header in headers:
		clean_headers.append( slugify(header, separator="_") )
	return clean_headers

# Connect to database
eng = sa.create_engine(DATABASE_URL)

# Load control file template
with open('control.template.json') as control_json:
	control_template = json.load(control_json)

# Fetch datasets config
with open('datasets.yaml') as datasets_yaml:
	datasets = yaml.load(datasets_yaml)

# For each dataset in datasets config
for dataset in datasets:
	control_file = control_template.copy()
	
	with open('tmp/' + dataset['table'] + '.csv', 'w') as f:
		# Export to CSV
		query = eng.execute("SELECT * FROM %s" % dataset['table'])
		writer = csv.writer(f)
		headers = query.fetchone().keys()
		writer.writerow(headers)
		writer.writerows(query.fetchall())
		
		# Put clean headers into control file template
		control_file['csv']['columns'] = clean_headers(headers)
	
	# Write control file to disk
	with open('tmp/control.' + dataset['table'] + '.json', 'w') as f:
		json.dump(control_file, f)
		
	print 'Pushing', dataset['table'], 'to', dataset['socrata_id']
	
	# Call DataSync w/csv and control file
	subprocess.call([
		'java',
		'-jar', 'bin/DataSync-1.6.jar',
		'-c', 'config.json',
		'-f', 'tmp/' + dataset['table'] + '.csv',
		'-i', dataset['socrata_id'],
		'-m', 'replace',
		'-ph', 'true',
		'-cf', 'tmp/control.' + dataset['table'] + '.json'
	])