CREATE TABLE blocks (
      block_height BIGINT UNIQUE NOT NULL,
      block_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
      block_hash TEXT NOT NULL UNIQUE,
      author_account_id VARCHAR(64) NOT NULL,
      approvals BIGINT,
    PRIMARY KEY (block_height)
);

CREATE INDEX idx_blocks_block_timestamp ON blocks(block_timestamp);

CREATE TABLE transactions (
      block_height BIGINT NOT NULL,
      block_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
      tx_hash TEXT UNIQUE NOT NULL,
      signer_id VARCHAR(64),
      nonce BIGINT,
      receipt_id TEXT,
      receiver_id VARCHAR(64),
    PRIMARY KEY (tx_hash),
    FOREIGN KEY (block_height) REFERENCES blocks(block_height) ON DELETE CASCADE
);

CREATE INDEX idx_transactions_block_timestamp ON transactions(block_timestamp);
CREATE INDEX idx_transactions_signer_id ON transactions(signer_id);
CREATE INDEX idx_transactions_receiver_id ON transactions(receiver_id);

CREATE TABLE receipt_actions (
      id TEXT UNIQUE NOT NULL,
      block_height BIGINT NOT NULL,
      block_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
      receipt_id TEXT,
      predecessor_id VARCHAR(64) NOT NULL,
      receiver_id VARCHAR(64) NOT NULL,
      action_kind VARCHAR(20) NOT NULL,
      action_index BIGINT NOT NULL,
      method_name VARCHAR(255) NOT NULL,
      args TEXT,
      social_kind VARCHAR(20),
      gas INT NOT NULL,
      deposit DOUBLE PRECISION NOT NULL,
      stake DOUBLE PRECISION NOT NULL,
      status VARCHAR(20) NOT NULL,
      PRIMARY KEY (id),
      FOREIGN KEY (block_height) REFERENCES blocks(block_height) ON DELETE CASCADE
);

CREATE INDEX idx_receipt_actions_block_timestamp ON receipt_actions(block_timestamp);
CREATE INDEX idx_receipt_actions_predecessor_id ON receipt_actions(predecessor_id);
CREATE INDEX idx_receipt_actions_receiver_id ON receipt_actions(receiver_id);