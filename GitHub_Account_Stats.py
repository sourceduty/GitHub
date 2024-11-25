import requests
import json

# Replace with your GitHub personal access token
GITHUB_TOKEN = '000000000000000000000000000000000000000000000'

# GitHub API URL
GITHUB_API_URL = 'https://api.github.com'

# Function to get user data
def get_user_data(username):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    url = f'{GITHUB_API_URL}/users/{username}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to get user repositories
def get_user_repositories(username):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    url = f'{GITHUB_API_URL}/users/{username}/repos'
    all_repos = []
    
    # To handle pagination (GitHub API returns 30 results per page)
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}", headers=headers)
        if response.status_code == 200:
            repos = response.json()
            if not repos:
                break
            all_repos.extend(repos)
            page += 1
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break
    
    # Sort repositories by the number of stars in descending order
    sorted_repos = sorted(all_repos, key=lambda repo: repo['stargazers_count'], reverse=True)
    return sorted_repos

# Function to get user contributions
def get_user_contributions(username):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    url = f'{GITHUB_API_URL}/users/{username}/events/public'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to save the statistics into a text file
def save_statistics_to_txt(username, filename="github_report.txt"):
    user_data = get_user_data(username)
    if not user_data:
        return
    
    with open(filename, 'w') as file:
        file.write(f"User: {user_data['login']}\n")
        file.write(f"Name: {user_data['name']}\n")
        file.write(f"Bio: {user_data['bio']}\n")
        file.write(f"Public Repositories: {user_data['public_repos']}\n")
        file.write(f"Followers: {user_data['followers']}\n")
        file.write(f"Following: {user_data['following']}\n\n")
        
        # Get repositories sorted by stars
        repositories = get_user_repositories(username)
        if repositories:
            file.write(f"Repositories Sorted by Stars:\n")
            for repo in repositories:
                file.write(f"- {repo['name']} (Stars: {repo['stargazers_count']}, Forks: {repo['forks_count']})\n")
        
        # Get contributions (events)
        contributions = get_user_contributions(username)
        if contributions:
            file.write(f"\nRecent Contributions:\n")
            for event in contributions[:5]:  # Display last 5 contributions
                file.write(f"- {event['type']} at {event['created_at']}\n")
        
    print(f"Report saved to {filename}")

# Example usage
username = input("Enter GitHub username: ")
save_statistics_to_txt(username, filename="github_report.txt")
