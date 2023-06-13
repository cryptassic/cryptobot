
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
    },{
      name: 'SOLUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'SOLUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'ADAUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'ADAUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'APTUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'APTUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'ARBUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'ARBUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'SOLUSDC_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'SOLUSDC', '--server', 'ap-southeast-1a'],
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
      name: 'DOGEUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'DOGEUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'LTCUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'LTCUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'BNBUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'BNBUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'APEXUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'APEXUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'BUSDUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'BUSDUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'PEPEUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'PEPEUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'AVAXUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'AVAXUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'LINKUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'LINKUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'AXLUSDT_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'AXLUSDT', '--server', 'ap-southeast-1a'],
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
      name: 'ARBUSDC_SPOT',
      script: './src/bybit_spot_trades.py',
      args: ['--symbol', 'ARBUSDC', '--server', 'ap-southeast-1a'],
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
