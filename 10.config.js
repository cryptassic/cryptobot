
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
    },{
      name: 'BTCUSDC_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'BTCUSDC', '--server', 'ap-southeast-1a'],
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
    },{
      name: 'BTCUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'BTCUSDT', '--server', 'ap-southeast-1a'],
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
    },{
      name: 'ETHUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'ETHUSDT', '--server', 'ap-southeast-1a'],
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
    },{
      name: 'XRPUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'XRPUSDT', '--server', 'ap-southeast-1a'],
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
    },{
      name: 'USDCUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'USDCUSDT', '--server', 'ap-southeast-1a'],
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
    },{
      name: 'XRPUSDC_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'XRPUSDC', '--server', 'ap-southeast-1a'],
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
    },{
      name: 'SUIUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'SUIUSDT', '--server', 'ap-southeast-1a'],
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
    },{
      name: 'MATICUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'MATICUSDT', '--server', 'ap-southeast-1a'],
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
    },{
      name: 'SHIBUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'SHIBUSDT', '--server', 'ap-southeast-1a'],
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
