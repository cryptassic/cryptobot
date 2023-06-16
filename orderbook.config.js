const SERVER = "ap-southeast-1a";
const EXCHANGE = "BYBIT";
module.exports = {
  apps: [
    {
      name: `${EXCHANGE}_BOOK_1`,
      script: `./src/${EXCHANGE.toLowerCase()}_spot_orderbook.py`,
      args: ["--index", "0", "--server", SERVER],
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
      name: `${EXCHANGE}_BOOK_2`,
      script: `./src/${EXCHANGE.toLowerCase()}_spot_orderbook.py`,
      args: ["--index", "1", "--server", SERVER],
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
      name: `${EXCHANGE}_BOOK_3`,
      script: `./src/${EXCHANGE.toLowerCase()}_spot_orderbook.py`,
      args: ["--index", "2", "--server", SERVER],
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
      name: `${EXCHANGE}_BOOK_4`,
      script: `./src/${EXCHANGE.toLowerCase()}_spot_orderbook.py`,
      args: ["--index", "3", "--server", SERVER],
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
      name: `${EXCHANGE}_BOOK_5`,
      script: `./src/${EXCHANGE.toLowerCase()}_spot_orderbook.py`,
      args: ["--index", "4", "--server", SERVER],
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
      name: `${EXCHANGE}_BOOK_6`,
      script: `./src/${EXCHANGE.toLowerCase()}_spot_orderbook.py`,
      args: ["--index", "5", "--server", SERVER],
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
      name: `${EXCHANGE}_BOOK_7`,
      script: `./src/${EXCHANGE.toLowerCase()}_spot_orderbook.py`,
      args: ["--index", "6", "--server", SERVER],
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
      name: `${EXCHANGE}_BOOK_8`,
      script: `./src/${EXCHANGE.toLowerCase()}_spot_orderbook.py`,
      args: ["--index", "7", "--server", SERVER],
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
      name: `${EXCHANGE}_BOOK_9`,
      script: `./src/${EXCHANGE.toLowerCase()}_spot_orderbook.py`,
      args: ["--index", "8", "--server", SERVER],
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
      name: `${EXCHANGE}_BOOK_10`,
      script: `./src/${EXCHANGE.toLowerCase()}_spot_orderbook.py`,
      args: ["--index", "9", "--server", SERVER],
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
