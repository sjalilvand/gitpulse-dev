from github import Github, GithubException
from app.core.config import get_settings

settings = get_settings()

def get_github_client() -> Github:
    if settings.github_token:
        return Github(settings.github_token)
    else:
        return Github()  # anonymous, rate limit very low

def parse_repo_url(url: str):
    """
    از url مثل https://github.com/owner/repo
    owner و repo_name رو استخراج می‌کنه
    """
    url = url.rstrip("/").replace("https://github.com/", "")
    parts = url.split("/")
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None

def fetch_repo_info(url: str):
    owner, repo_name = parse_repo_url(url)
    if not owner or not repo_name:
        raise ValueError("Invalid GitHub URL")

    client = get_github_client()
    try:
        repo = client.get_repo(f"{owner}/{repo_name}")
        return {
            "github_id": repo.id,
            "name": repo.name,
            "full_name": repo.full_name,
            "owner": repo.owner.login,
            "url": repo.html_url,
            "description": repo.description or "",
            "default_branch": repo.default_branch,
            "language": repo.language or "",
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues_count": repo.open_issues_count,
        }
    except GithubException as e:
        raise Exception(f"GitHub API error: {e.data.get('message', 'Unknown error')}")

def fetch_pull_requests(full_name: str, count: int = 20):
    client = get_github_client()
    try:
        repo = client.get_repo(full_name)
        pulls = repo.get_pulls(state='all', sort='updated', direction='desc')[:count]
        result = []
        for pr in pulls:
            result.append({
                "github_pr_id": pr.id,
                "number": pr.number,
                "title": pr.title,
                "body": pr.body or "",
                "state": pr.state,
                "author_username": pr.user.login if pr.user else "",
                "base_branch": pr.base.ref,
                "head_branch": pr.head.ref,
                "merged": bool(pr.merged),
                "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files,
            })
        return result
    except Exception as e:
        raise Exception(f"GitHub API error: {str(e)}")

def fetch_issues(full_name: str, count: int = 20):
    client = get_github_client()
    try:
        repo = client.get_repo(full_name)
        issues = repo.get_issues(state='all', sort='updated', direction='desc')[:count]
        result = []
        for issue in issues:
            # ignore pull requests (GitHub treats PRs as issues)
            if issue.pull_request is not None:
                continue
            labels = ",".join([l.name for l in issue.labels]) if issue.labels else ""
            result.append({
                "github_issue_id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "body": issue.body or "",
                "state": issue.state,
                "author_username": issue.user.login if issue.user else "",
                "labels": labels,
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
                "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
            })
        return result
    except Exception as e:
        raise Exception(f"GitHub API error: {str(e)}")