import subprocess
import argparse
import os
from openai import OpenAI

def get_git_diff(repo_path):
    try:
        os.chdir(repo_path)
        result = subprocess.run(
            ['git', 'diff', '--staged'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error getting git diff: {e.stderr}")

def generate_commit_message(diff):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    prompt = f"""
    Generate a concise, one-line git commit message in conventional commit format 
    based on these changes. Focus on the main changes and impact.
    The message should follow this pattern: 
    [type]: [description] (max 72 characters)
    
    Diff:
    {diff[:4000]}  # Truncate to avoid token limits
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a senior software engineer writing excellent commit messages."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=60
    )
    
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate smart commit message from git diff')
    parser.add_argument('repo_path', type=str, help='Path to Git repository')
    args = parser.parse_args()

    try:
        if not os.path.isdir(args.repo_path):
            raise Exception("Invalid repository path")
            
        diff = get_git_diff(args.repo_path)
        if not diff:
            print("No staged changes detected")
            exit(0)
            
       # message = generate_commit_message(diff)
        print(f"{diff}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)