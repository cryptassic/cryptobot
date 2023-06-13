def get_app(symbol: str):
    return """{{
      name: '{0}_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', '{0}', '--server', 'ap-southeast-1a'],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      restart_delay: 30000,
      env_prod: {{
        ENV: "production",
      }},
      env_dev: {{
        ENV: "development",
      }},
      interpreter: "./venv/bin/python",
    }}""".format(
        symbol.upper()
    )


def load_tokens():
    with open("./tokens.txt", "r") as f:
        tokens = f.read().splitlines()

    return tokens


size = 10
tokens = [token.split(":")[0] for token in load_tokens()][:size]

apps = [get_app(symbol) for symbol in tokens]

result = ",".join(apps)

javascript_code = """
module.exports = {{
  apps: [{0}]
}};
""".format(
    result
)


with open(f"{size if size > 0 else 'full'}.config.js", "w") as f:
    f.write(javascript_code)
