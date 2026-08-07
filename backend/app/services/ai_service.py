from openai import OpenAI
from app.core.config import get_settings

_client = None


def get_client():
    global _client
    if _client is None:
        settings = get_settings()
        _client = OpenAI(
            api_key=settings.avalai_api_key,
            base_url=settings.avalai_base_url
        )
    return _client


def generate_weekly_summary(repo_name: str, commits: list) -> str:
    client = get_client()
    commit_messages = "\n".join([f"- {c['message'].split(chr(10))[0]}" for c in commits[:30]])

    prompt = f"""Generate a brief weekly summary for repository '{repo_name}' based on these commits (write in Persian):
    {commit_messages}
{commit_messages}

Focus on: main changes, new features, bug fixes, and overall progress.
Keep it under 200 words and use bullet points."""

    try:
        response = client.chat.completions.create(
            model="gpt-5.5",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def analyze_pr_risk(pr_data: dict) -> dict:
    client = get_client()
    prompt = f"""Analyze this Pull Request for potential risks:
Title: {pr_data['title']}
Changes: +{pr_data.get('additions', 0)} -{pr_data.get('deletions', 0)} lines, {pr_data.get('changed_files', 0)} files
Base branch: {pr_data.get('base_branch', 'main')}

Return a JSON with:
- risk_score (0-100)
- risk_level (low/medium/high)
- summary (one sentence)
- risks (array of strings)
- suggestions (array of strings)"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        import json
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"risk_score": 0, "risk_level": "unknown", "summary": "AI analysis failed"}


def classify_issue(title: str, body: str = "") -> dict:
    client = get_client()
    prompt = f"""Classify this GitHub issue:
Title: {title}
Body: {body[:500]}

Return a JSON with:
- category: one of [bug, feature, question, documentation, security, performance]
- priority: one of [critical, high, medium, low]
- summary: one sentence summary"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200
        )
        import json
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"category": "unknown", "priority": "medium", "summary": "Classification failed"}