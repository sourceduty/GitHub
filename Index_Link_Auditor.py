# This program was developed to audit Sourceduty Repositoty Index links.
# This program reads a list of URLs from a links.tct file, cleans up any unwanted characters, and checks if each URL is accessible by making an HTTP request, printing the result for each link.

import requests
import re

# Read the links from the file
with open('links.txt', 'r') as file:
    links = file.readlines()

# Function to clean up URL
def clean_url(url):
    # Remove any unwanted characters (like parentheses) at the end
    return re.sub(r'[^\w\s:/.-]', '', url)

# Check each link
for link in links:
    link = link.strip()  # Remove any leading/trailing whitespace
    cleaned_link = clean_url(link)  # Clean the link
    try:
        response = requests.get(cleaned_link)
        if response.status_code == 200:
            print(f"Success: {cleaned_link}")
        else:
            print(f"Failed ({response.status_code}): {cleaned_link}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {cleaned_link} -> {e}")
