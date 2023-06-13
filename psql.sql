-- Create hypertable that stores data in 1 day chunks
SELECT create_hypertable(
  'bybit_spot_trade',
  'time',
  chunk_time_interval => INTERVAL '1 day'
);

-- Create index for efficient query
CREATE INDEX ix_symbol_time ON bybit_spot_trade (trade_symbol, time DESC);

CREATE TABLE bybit_spot_trade (
  time TIMESTAMPTZ NOT NULL,
  trade_id BIGINT NOT NULL,
  trade_type TEXT NOT NULL,
  trade_fill_time TIMESTAMPTZ NOT NULL,
  trade_side TEXT NOT NULL,
  trade_symbol TEXT NOT NULL,
  trade_qty REAL NOT NULL,
  trade_price REAL NOT NULL,
  trades_count SMALLINT NOT NULL,
  block_trade BOOLEAN NOT NULL,
  server TEXT NOT NULL,
  exchange TEXT NOT NULL,
  rx_time TIMESTAMPTZ NOT NULL,
  latency REAL NOT NULL
);

CREATE TABLE test_table (
  time TIMESTAMPTZ NOT NULL,
  trade_id BIGINT NOT NULL,
  trade_type TEXT NOT NULL,
  trade_fill_time TIMESTAMPTZ NOT NULL,
  trade_side TEXT NOT NULL,
  trade_symbol TEXT NOT NULL,
  trade_qty REAL NOT NULL,
  trade_price REAL NOT NULL,
  trades_count SMALLINT NOT NULL,
  block_trade BOOLEAN NOT NULL,
  server TEXT NOT NULL,
  exchange TEXT NOT NULL,
  rx_time TIMESTAMPTZ NOT NULL,
  latency REAL NOT NULL
);

 -- Clean table
DELETE FROM bybit_spot_trade;