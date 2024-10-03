DROP TABLE IF EXISTS blocks;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS receipt_actions;
DROP TABLE IF EXISTS cursors;

CREATE TABLE blocks
(
    block_height Int64,
    block_timestamp DateTime('UTC'),
    block_hash String,
    author_account_id String,
    approvals Int64,

    INDEX idx_transactions_block_height block_height TYPE minmax GRANULARITY 1,
    INDEX idx_transactions_block_timestamp block_timestamp TYPE minmax GRANULARITY 1
)
    ENGINE = MergeTree()
ORDER BY (block_height)
PRIMARY KEY block_height;


CREATE TABLE transactions
(
    block_height Int64,
    block_timestamp DateTime('UTC'),
    tx_hash String,
    signer_id String,
    nonce Int64,
    receipt_id String,
    receiver_id String,

    INDEX idx_transactions_block_height block_height TYPE minmax GRANULARITY 1,
    INDEX idx_transactions_block_timestamp block_timestamp TYPE minmax GRANULARITY 1,
    INDEX idx_transactions_signer_id signer_id TYPE bloom_filter() GRANULARITY 1,
    INDEX idx_transactions_receiver_id receiver_id TYPE bloom_filter() GRANULARITY 1
)
    ENGINE = MergeTree()
ORDER BY (tx_hash)
PRIMARY KEY (tx_hash);


CREATE TABLE receipt_actions
(
    id String,
    receipt_id String,
    block_height Int64,
    block_timestamp DateTime('UTC'),
    predecessor_id String,
    receiver_id String,
    action_kind String,
    action_index Int64,
    method_name String,
    args String,
    social_kind String,
    gas Int32,
    deposit Float64,
    stake Float64,
    status String,

    INDEX idx_receipt_actions_block_height block_height TYPE minmax GRANULARITY 1,
    INDEX idx_receipt_actions_block_timestamp block_timestamp TYPE minmax GRANULARITY 1,
    INDEX idx_receipt_actions_predecessor_id predecessor_id TYPE bloom_filter() GRANULARITY 1,
    INDEX idx_receipt_actions_receiver_id receiver_id TYPE bloom_filter() GRANULARITY 1,
    INDEX idx_receipt_actions_action_kind action_kind TYPE bloom_filter() GRANULARITY 1
)
    ENGINE = MergeTree()
ORDER BY (id, block_height, predecessor_id, receiver_id)
PRIMARY KEY (id);


CREATE TABLE api_queries
(
    id String,
    name String,
    query_type String,
    query_text String
)
    ENGINE = MergeTree()
ORDER BY (id)
PRIMARY KEY (id);
