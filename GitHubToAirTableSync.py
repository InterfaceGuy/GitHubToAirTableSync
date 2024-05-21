import os
from dotenv import load_dotenv
import re
from urllib.parse import urlparse
from pyairtable import Api

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.environ.get('AIRTABLE_API_KEY')

# Replace with your Airtable base ID and table ID
BASE_ID = 'appkelIX4TJy6rmuP'
TABLE_ID = 'tblHTEk3H7ra8zjhk'

# Initialize the Airtable API
api = Api(API_KEY)
table = api.table(BASE_ID, TABLE_ID)

# Define the path to the canvas file
canvas_path = '/Users/davidrug/Library/Mobile Documents/iCloud~md~obsidian/Documents/InterBrain/CRIDreamTalk.canvas'

# Parse the Obsidian canvas file
with open(canvas_path, 'r') as f:
    canvas_content = f.read()

# Extract GitHub remote links from the canvas file
remote_links = re.findall(r'"file":"(.+?)/README.md"', canvas_content)

# Create a set of existing repository URLs in the Airtable table
existing_repo_urls = set(record['fields'].get('Repository URL', '') for record in table.all())

# Define the Reviewer collaborator object
reviewer_collaborator = {
    'email': 'zak@civilizationresearch.org',
    'name': 'Zak Stein'
}

# Iterate over the remote links
for remote_link in remote_links:
    # Extract the repository name from the remote link
    repo_name = os.path.basename(remote_link)

    # Construct the GitHub repository URL
    repo_url = f'https://github.com/InterfaceGuy/{repo_name}'

    # Skip if the repository URL already exists in the Airtable table
    if repo_url in existing_repo_urls:
        continue

    # Create a new record in the Airtable table
    table.create({'Name': repo_name, 'Repository URL': repo_url, 'Reviewer': reviewer_collaborator, 'Status': "In progress"})
    print(f'Added {repo_name} to Airtable')