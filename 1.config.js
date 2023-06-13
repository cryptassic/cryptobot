
module.exports = {
  apps: [{
      name: 'ETHUSDC_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'ETHUSDC', '--server', 'ap-southeast-1a'],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      restart_delay: 30000,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    }]
};
