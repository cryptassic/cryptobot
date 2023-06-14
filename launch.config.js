module.exports = {
  apps: [
    {
      name: "BYBIT_SPOT_1",
      script: "./src/bybit_spot_trades.py",
      args: ["--index", "0", "--server", "ap-southeast-1a"],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    },
    {
      name: "BYBIT_SPOT_2",
      script: "./src/bybit_spot_trades.py",
      args: ["--index", "1", "--server", "ap-southeast-1a"],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    },
    {
      name: "BYBIT_SPOT_3",
      script: "./src/bybit_spot_trades.py",
      args: ["--index", "2", "--server", "ap-southeast-1a"],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    },
    {
      name: "BYBIT_SPOT_4",
      script: "./src/bybit_spot_trades.py",
      args: ["--index", "3", "--server", "ap-southeast-1a"],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    },
    {
      name: "BYBIT_SPOT_5",
      script: "./src/bybit_spot_trades.py",
      args: ["--index", "4", "--server", "ap-southeast-1a"],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    },
    {
      name: "BYBIT_SPOT_6",
      script: "./src/bybit_spot_trades.py",
      args: ["--index", "5", "--server", "ap-southeast-1a"],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    },
    {
      name: "BYBIT_SPOT_7",
      script: "./src/bybit_spot_trades.py",
      args: ["--index", "6", "--server", "ap-southeast-1a"],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    },
    {
      name: "BYBIT_SPOT_8",
      script: "./src/bybit_spot_trades.py",
      args: ["--index", "7", "--server", "ap-southeast-1a"],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    },
    {
      name: "BYBIT_SPOT_9",
      script: "./src/bybit_spot_trades.py",
      args: ["--index", "8", "--server", "ap-southeast-1a"],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    },
    {
      name: "BYBIT_SPOT_10",
      script: "./src/bybit_spot_trades.py",
      args: ["--index", "9", "--server", "ap-southeast-1a"],
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      env_prod: {
        ENV: "production",
      },
      env_dev: {
        ENV: "development",
      },
      interpreter: "./venv/bin/python",
    },
  ],
};
