# Git commands
| Command | What does it do | Affected Repo |
|---------|-----------------|---------------|
| `git clone {repo}` | Clone the repository from Github to local machine | Local |
| `git checkout {branch}` | Switch the a specific exisiting branch (clone from repo if local does not have that branch) | Local |
| `git checkout -b {branch}` | Create and switch to a new branch (only local) | Local |
| `git add {filename}` | Stage a file name | Local |
| `git add -A` or `git add --all` | Stage all changes (new, modify and deleted files) | Local |
| `git commit -m {message}` | Create a commit that include all staged changes | Local |
| `git push` | Push commits that haven't been pushed yet onto Github | Github |
# Git strategy
We will have following branchs:
- `main`: The main branch used to deploy
- `feature/issue-{number}[-additional message]`: branch associated to an issue on Github, implementation will be on this branch. When the implementation is done, create a PR from this branch to main for reviewing
# Tasks Handling
When an issue is assigned, do the following step
1. Create a branch associated to that issue from the latest commit on branch `main`
2. In local, checkout and start developing on this new branch.
3. In case we need the latest implementation from `main` branch, merge branch `main` into the feature branch.
4. After completing the developing, commit and push the latest changes onto Github.
5. Create a PR for reviewing, assign other 2 developers as reviewers.
# What to do when a PR is created
## Owner of the PR
If you are the owner of the PR, ensure the following points are cleared
- Ensure the application works normally with no serious/critical bugs.
- Ensure the PR has no conflict, solve conflict by merge branch `main` into the feature branch.
- If there is any comment in the PR, please check them, discuss if needed and resolve them by adapting the implementation.
## Reviewer
- Check if any implementation that might cause a bug or not following coding convention.