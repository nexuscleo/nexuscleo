import requests
import os

# Configurações
USER = "NEXUSCLEO"
TOKEN = os.getenv("GITHUB_TOKEN") # Pega automaticamente do GitHub Actions

def get_github_data():
    query = """
    {
      user(login: "%s") {
        repositories(first: 100, ownerAffiliations: OWNER) {
          totalCount
          nodes {
            stargazerCount
          }
        }
        contributionsCollection {
          totalCommitContributions
        }
      }
    }
    """ % USER
    
    url = 'https://api.github.com/graphql'
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(url, json={'query': query}, headers=headers)
    res_json = response.json()
    
    user_data = res_json['data']['user']
    total_stars = sum(repo['stargazerCount'] for repo in user_data['repositories']['nodes'])
    total_commits = user_data['contributionsCollection']['totalCommitContributions']
    total_repos = user_data['repositories']['totalCount']
    
    # Lógica simples de "Level" (Ex: 1 level a cada 100 commits + 50 estrelas)
    level = (total_commits // 100) + (total_stars // 10)
    progress = total_commits % 100 # Progresso para o próximo nível (0-100)
    
    return {
        "commits": total_commits,
        "stars": total_stars,
        "repos": total_repos,
        "level": level,
        "progress": progress
    }

def generate_svg(stats):
    # Cores e Dimensões
    bg_color = "#0d1117"
    border_color = "#30363d"
    text_color = "#c9d1d9"
    accent_color = "#58a6ff" # Azul GitHub
    
    svg = f"""
    <svg width="450" height="150" viewBox="0 0 450 150" fill="none" xmlns="http://www.w3.org/2000/svg">
      <style>
        .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {accent_color}; }}
        .stat {{ font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {text_color}; }}
        .bold {{ font-weight: 700; fill: #ffffff; }}
        .level-text {{ font: italic 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: {text_color}; }}
      </style>
      
      <rect x="0.5" y="0.5" rx="10" width="449" height="149" fill="{bg_color}" stroke="{border_color}"/>
      
      <text x="25" y="35" class="header">🚀 {USER} Stats</text>
      
      <g transform="translate(25, 60)">
        <text x="0" y="0" class="stat">Total Commits: <tspan class="bold">{stats['commits']}</tspan></text>
        <text x="0" y="25" class="stat">Total Stars: <tspan class="bold">{stats['stars']}</tspan></text>
        <text x="0" y="50" class="stat">Public Repos: <tspan class="bold">{stats['repos']}</tspan></text>
      </g>
      
      <g transform="translate(320, 45)">
        <circle cx="40" cy="40" r="35" stroke="{accent_color}" stroke-width="4" fill="transparent" opacity="0.2"/>
        <text x="40" y="47" text-anchor="middle" class="header" style="font-size: 24px;">Lvl {stats['level']}</text>
      </g>
      
      <text x="25" y="125" class="level-text">Progress to Next Level</text>
      <rect x="25" y="130" width="400" height="6" rx="3" fill="{border_color}"/>
      <rect x="25" y="130" width="{4 * stats['progress']}" height="6" rx="3" fill="{accent_color}"/>
      
    </svg>
    """
    
    with open("stats.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    data = get_github_data()
    generate_svg(data)
