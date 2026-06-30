# Hello World GitHub Action

A simple GitHub Action that posts "Hello World" on every push to the repository.

## How it works

This action triggers on `push` events to the `main` or `master` branches and:
1. Posts a "Hello World" message as a comment on the commit
2. If a Pull Request is associated, it also posts as a PR comment
3. Includes repository details, commit SHA, and timestamp

## Files

- `.github/workflows/hello-world.yml` - GitHub Action workflow definition
- `hello_world.py` - Python script that posts the message

## Setup

1. Add these files to your repository
2. Push to GitHub
3. The action will run automatically

## Permissions

The action uses the built-in `GITHUB_TOKEN` with default permissions. 
If you need to post comments on Pull Requests, ensure the token has 
`issues: write` and `pull-requests: write` permissions.

## License

MIT
