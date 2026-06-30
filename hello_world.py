#!/usr/bin/env python3
"""
GitHub Action: Hello World on Push
Posts "Hello World" as a comment on the commit that triggered the action.
"""

import os
import sys
import json
import requests
from datetime import datetime

def get_github_context():
    """Extract GitHub context from environment variables."""
    context = {
        'repository': os.environ.get('GITHUB_REPOSITORY'),
        'sha': os.environ.get('GITHUB_SHA'),
        'ref': os.environ.get('GITHUB_REF'),
        'actor': os.environ.get('GITHUB_ACTOR'),
        'event_name': os.environ.get('GITHUB_EVENT_NAME'),
        'workspace': os.environ.get('GITHUB_WORKSPACE'),
        'token': os.environ.get('GITHUB_TOKEN')
    }
    
    # Check if running in GitHub Actions
    if not context['repository'] or not context['sha']:
        print("❌ Not running in GitHub Actions environment")
        sys.exit(1)
    
    if not context['token']:
        print("❌ GITHUB_TOKEN not found")
        sys.exit(1)
    
    return context

def post_commit_comment(repo, sha, token, message):
    """Post a comment on a specific commit."""
    url = f"https://api.github.com/repos/{repo}/commits/{sha}/comments"
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    data = {
        'body': message
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting comment: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def post_issue_comment(repo, issue_number, token, message):
    """Post a comment on an issue or pull request."""
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    data = {
        'body': message
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting comment: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def get_pr_number_from_push_event():
    """Try to get PR number from push event if available."""
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    if not event_path or not os.path.exists(event_path):
        return None
    
    try:
        with open(event_path, 'r') as f:
            event_data = json.load(f)
        
        # Check if this is a PR event
        if 'pull_request' in event_data:
            return event_data['pull_request']['number']
        
        # For push events, check if there's a PR linked
        # This is a simplified approach - in real scenarios you'd use GitHub API
        return None
    except Exception as e:
        print(f"⚠️ Could not read event data: {e}")
        return None

def main():
    """Main entry point."""
    # Get GitHub context
    context = get_github_context()
    
    print(f"🚀 Hello World Action triggered!")
    print(f"📦 Repository: {context['repository']}")
    print(f"🔑 Commit: {context['sha'][:7]}")
    print(f"👤 Actor: {context['actor']}")
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create the message
    message = f"""# 🌍 Hello World!

Hello, World! 👋

This message was posted automatically by a GitHub Action.

**Details:**
- **Repository:** `{context['repository']}`
- **Commit:** `{context['sha'][:7]}`
- **Triggered by:** @{context['actor']}
- **Branch:** `{context['ref'].replace('refs/heads/', '')}`
- **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*🤖 This is an automated message from the Hello World GitHub Action*
"""
    
    # Try to post as a commit comment
    result = post_commit_comment(
        context['repository'],
        context['sha'],
        context['token'],
        message
    )
    
    if result:
        print("✅ Successfully posted Hello World as a commit comment!")
        print(f"🔗 Comment URL: {result.get('html_url', 'N/A')}")
    else:
        print("⚠️ Failed to post commit comment")
        
        # Try alternative: post as an issue comment if this is a PR
        pr_number = get_pr_number_from_push_event()
        if pr_number:
            print(f"🔄 Attempting to post as PR comment (PR #{pr_number})...")
            result = post_issue_comment(
                context['repository'],
                pr_number,
                context['token'],
                message
            )
            if result:
                print(f"✅ Successfully posted Hello World as a PR comment!")
                print(f"🔗 Comment URL: {result.get('html_url', 'N/A')}")
            else:
                print("❌ Failed to post comment anywhere")
                sys.exit(1)
        else:
            print("❌ Could not post comment")
            sys.exit(1)
    
    print("🎉 Hello World action completed successfully!")

if __name__ == "__main__":
    main()
