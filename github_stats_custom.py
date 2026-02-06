import requests
import os

# CONFIGURAÇÃO
USER = "NEXUSCLEO"
TOKEN = os.getenv("GITHUB_TOKEN")

def get_github_data():
    # Esta é a "pergunta" (query) que fazemos para o banco de dados do GitHub
    query = """
    {
      user(login: "%s") {
        repositories(first: 100, ownerAffiliations: OWNER) {
          totalCount
          nodes { stargazerCount }
        }
        contributionsCollection { totalCommitContributions }
      }
    }
    """ % USER
    
    url = 'https://api.github.com/graphql'
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(url, json={'query': query}, headers=headers)
    data = response.json()['data']['user']
    
    return {
        "commits": data['contributionsCollection']['totalCommitContributions'],
        "stars": sum(repo['stargazerCount'] for repo in data['repositories']['nodes']),
        "repos": data['repositories']['totalCount']
    }

def generate_svg(stats):
    # Calculando um nível e progresso fictício para o design
    level = (stats['commits'] // 100) + (stats['stars'] // 10)
    progress = stats['commits'] % 100 

    # Aqui desenhamos o visual da sua badge usando código SVG
    svg = f"""
    <svg width="450" height="150" viewBox="0 0 450 150" fill="none" xmlns="http://www.w3.org/2000/svg">
      <style>
        .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #58a6ff; }}
        .stat {{ font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #c9d1d9; }}
        .bold {{ font-weight: 700; fill: #ffffff; }}
      </style>
      <rect x="0.5" y="0.5" rx="10" width="449" height="149" fill="#0d1117" stroke="#30363d"/>
      <text x="25" y="35" class="header">🚀 {USER} Stats (Custom)</text>
      <g transform="translate(25, 65)">
        <text x="0" y="0" class="stat">Commits: <tspan class="bold">{stats['commits']}</tspan></text>
        <text x="0" y="25" class="stat">Stars: <tspan class="bold">{stats['stars']}</tspan></text>
        <text x="0" y="50" class="stat">Repos: <tspan class="bold">{stats['repos']}</tspan></text>
      </g>
      <circle cx="360" cy="75" r="40" stroke="#58a6ff" stroke-width="4" fill="transparent" opacity="0.2"/>
      <text x="360" y="82" text-anchor="middle" class="header" style="font-size: 22px;">Lvl {level}</text>
      <rect x="25" y="130" width="400" height="6" rx="3" fill="#30363d"/>
      <rect x="25" y="130" width="{4 * progress}" height="6" rx="3" fill="#58a6ff"/>
    </svg>
    """
    # Salvamos o desenho com o nome único para não apagar o seu atual
    with open("profile-stats-custom.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    data = get_github_data()
    generate_svg(data)
