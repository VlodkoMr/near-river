DROP TABLE IF EXISTS receipt_actions;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS blocks;
DROP TABLE IF EXISTS cursors;
DROP TABLE IF EXISTS substreams_history;
DROP TABLE IF EXISTS api_queries;

CREATE TABLE blocks (
      block_height BIGINT UNIQUE NOT NULL, -- Block height: the sequential block number in the NEAR blockchain
    block_timestamp TIMESTAMP WITH TIME ZONE NOT NULL, -- The timestamp when the block was produced
    block_hash TEXT NOT NULL UNIQUE, -- Unique hash of the block used for block identification
    author_account_id VARCHAR(64) NOT NULL, -- Account ID of the block producer (validator)
    approvals BIGINT, -- Number of approvals (signatures) from validators for this block
    PRIMARY KEY (block_height) -- The primary key is the block height, ensuring uniqueness and fast lookup
);

CREATE INDEX idx_blocks_block_timestamp ON blocks(block_timestamp);

CREATE TABLE transactions (
    block_height BIGINT NOT NULL, -- Block height to which the transaction belongs (linked to blocks table)
    block_timestamp TIMESTAMP WITH TIME ZONE NOT NULL, -- Timestamp of the transaction, matching the block's timestamp
    tx_hash TEXT UNIQUE NOT NULL, -- Unique transaction hash used to identify the transaction on the blockchain
    signer_id VARCHAR(64), -- Account ID of the transaction's sender (signer or predecessor)
    nonce BIGINT, -- Nonce used to prevent transaction replay and maintain correct ordering
    receipt_id TEXT, -- Receipt ID linked to the executions of this transaction, belongs to receipt_actions table
    receiver_id VARCHAR(64), -- Account ID of the transaction's receiver (account or smart-contract that we call)
    PRIMARY KEY (tx_hash), -- The primary key is the transaction hash, ensuring unique identification of each transaction
    FOREIGN KEY (block_height) REFERENCES blocks(block_height) ON DELETE CASCADE -- Foreign key linking to the block
);

CREATE INDEX idx_transactions_block_timestamp ON transactions(block_timestamp);
CREATE INDEX idx_transactions_signer_id ON transactions(signer_id);
CREATE INDEX idx_transactions_receiver_id ON transactions(receiver_id);
CREATE INDEX idx_transactions_signer_receiver ON transactions(signer_id, receiver_id);

CREATE TABLE receipt_actions (
    id TEXT UNIQUE NOT NULL, -- Unique internal action ID, not exposed publicly and not used in queries
    block_height BIGINT NOT NULL, -- Block height associated with this action, part of the block
    block_timestamp TIMESTAMP WITH TIME ZONE NOT NULL, -- Timestamp when this action occurred, matching the block and transaction timestamps
    receipt_id TEXT NOT NULL, -- Receipt ID generated for this action, associated with transaction execution
    predecessor_id VARCHAR(64) NOT NULL, -- Account ID of the transaction's sender (signer or predecessor)
    receiver_id VARCHAR(64) NOT NULL, -- Account ID of the transaction's receiver (account or smart-contract that we call)
    action_kind VARCHAR(20) NOT NULL, -- The type of action (e.g., FunctionCall, Transfer, Stake)
    action_index BIGINT NOT NULL, -- The position of the action within the transaction (used when multiple actions are present)
    method_name VARCHAR(255) NOT NULL, -- The name of the method being invoked for FunctionCall actions
    args TEXT, -- JSON-formatted arguments passed to the method (if applicable)
    social_kind VARCHAR(20), -- Type of social interaction if related to social transactions (e.g., Post, Comment). This actions related only to the NEAR Social (social.near calls)
    gas INT NOT NULL, -- Amount of gas allocated for executing this action
    deposit DOUBLE PRECISION NOT NULL, -- Amount of tokens transferred by the action
    stake DOUBLE PRECISION NOT NULL, -- Amount of tokens staked, if this is a staking action
    status VARCHAR(20) NOT NULL, -- Status of the action (e.g., Success, Failure). Empty string means "Success"
    PRIMARY KEY (id), -- The primary key is the unique action ID
    FOREIGN KEY (block_height) REFERENCES blocks(block_height) ON DELETE CASCADE -- Foreign key linking to the block
);

CREATE INDEX idx_receipt_actions_block_timestamp ON receipt_actions(block_timestamp);
CREATE INDEX idx_receipt_actions_predecessor_id ON receipt_actions(predecessor_id);
CREATE INDEX idx_receipt_actions_receiver_id ON receipt_actions(receiver_id);
CREATE INDEX idx_receipt_actions_method_name ON receipt_actions(method_name);
CREATE INDEX idx_receipt_actions_predecessor_receiver ON receipt_actions(predecessor_id, receiver_id);
