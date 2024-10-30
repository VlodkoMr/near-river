### Task

Generate one SQL query to answer [QUESTION]{user_question}[/QUESTION].
Return **only** the SQL query without any additional text, symbols, comments, or explanations.

### Instructions

- Generate only read-only SQL queries, ignore any write operations and DDL commands, don't allow any data modification like UPDATE, DELETE, DROP etc, in this case return 'Not allowed'.
- If you cannot answer the question with the available database schema, return text 'I do not know' as SQL query.
- The query should be a valid SQL query that can be run on the provided database schema. Check the database schema section for details about the tables and columns.
- Use "SQL Examples" section to understand the database schema and how to build response SQL by user query.
- The question may contain NEAR blockchain-specific terms, "NEAR Blockchain Overview" section provides an overview of these terms and relations. Use other sections "Fungible Tokens (FT)", "Non-Fungible Tokens (NFT)", "Smart Contract Deployment", "Chain Signatures", "Social Transactions", "Action
  Kinds and Methods columns" for more details about user requests.
- Do **not** include any explanations, comments, or additional responses in the answer.
- Do **not** JOIN tables, each table contain all necessary information for user request: "blocks" table represent blockchain blocks, "transactions" table has sender/recipient of transactions, "receipt_actions" table contain more details about each transaction - if user ask
  about transactions (include tokens, transfer amounts, gas, social or other action kinds) in most cases we should use "receipt_actions" table.
- Do **not** overcomplicate the query and do not generate samples, all SQL queries should be ready to run on the provided database schema.
- If user ask about smart-contract, wallet or user accounts - use "receiver_id" (for recipient and called smart-contracts) and "signer_id" (for sender, who sign transaction) columns for `transactions` table. For detailed information about the actions, use "receiver_id" (for recipient and called
  smart-contracts) and "predecessor_id" (for sender, who sign transaction) columns in the `receipt_actions` table.
- Use comments in the "Database Schema" section to understand each table and column in the database schema.
- For receipt_action always use and `status`="Success" to filter only successful actions, except when user ask about failed actions.

#### NEAR Blockchain Overview

NEAR Protocol core components:

- Blocks: Represented in the "blocks" table, each block has metadata like block number ("block_height"), timestamp ("block_timestamp"), block_hash, producer ("author_account_id") and count of approvals ("approvals").
- Transactions: Represented in the "transactions" table, transactions belong to blocks and contain information like the sender ("signer_id"), receiver("receiver_id"), and transaction hash ("tx_hash"). Transactions have associated receipts in the "receipt_actions" table that contain detailed
  information about the actions performed in the transaction, deposits, staking and other information.
- Receipt Actions: Represented in the "receipt_actions" table, it capture the detailed execution of smart-contracts, action kind, deposits, methods, social activity and call arguments. Each receipt is belongs to transaction by the "transaction_hash" field.

#### Fungible Tokens (FT)

Standard: NEP-141, NEP-148
These methods are recorded in the "receipt_actions" table, within the "method_name" column.
Column "method_name" for FT can include:`create_token` (Creates a new FT),`storage_deposit` (Registers a user account/wallet for owning and transferring tokens), `ft_transfer` (Transfers FT to another account), `ft_transfer_call` (Similar to ft_transfer, but also calls a method on the receiving
contract), `storage_withdraw` (Unregisters a user account/wallet from holding a particular token).
Column "predecessor_id" refers to the sender and "receiver_id" refers to the recipient.

#### Non-Fungible Tokens (NFT)

Standard: NEP-171, NEP-177
These methods are also recorded in the "receipt_actions" table under the "method_name" column.
Column "method_name" for NFT can include:`nft_mint`: (Mints a new NFT),`nft_transfer` (Transfers NFT ownership to another account), `nft_transfer_call` (Transfers an NFT and invokes a method on the receiver contract), `nft_approve` (Approves the transfer of an NFT.
Column "predecessor_id" refers to the sender and "receiver_id" refers to the recipient.

#### Smart Contract Deployment

Smart contracts are deployed using the `deploy` method in the "receipt_actions" table.

#### Chain Signatures (Multi-chain Transactions)

NEAR supports cross-chain transactions via chain signatures.
Such transactions can be identified in the transactions table when the "receiver_id" column contains `v1.signer`.
More details about chain signature-related actions can be found in the "receipt_actions" table by filtering with "receiver_id" for relevant accounts.

#### Social Transactions

NEAR blockchain also supports NEAR Social - a decentralized social media platform.
Actions related to social transactions can be found in the "receipt_actions" table.
These actions are identified by the "social_kind" column, with potential values like: `Post`, `Comment`, `Like`, `Repost`, `Profile`, `Poke`, `Follow`, `UnFollow`, `Widget`, `Notify`.

#### Action Kinds and Methods columns

Receipt actions "receipt_actions" table, "action_kind" column include various methods for different on-chain activities, including:

- Contract Calls: `FunctionCall` (calling a method on a smart-contract)
- Account management: `CreateAccount` (create new wallet / user account), `DeleteAccount` (remove wallet / user account)
- Key management: `AddKey` (add new key), `DeleteKey` (remove key)
- Staking: `Stake` (NEAR native staking)
- Delegation: `Delegate` (delegating actions to another account)
- NEAR token transfers: `Transfer` (only for native NEAR token)
- Deploying a smart-contract: `DeployContract` (deploying a new smart contract)

Each action type can be identified using the "action_kind", and "method_name" column contain the specific method called within the action.

### Database Schema

The query will run on a database with the following schema:

```sql

CREATE TABLE blocks (
    block_height BIGINT UNIQUE NOT NULL, -- Block height
    block_timestamp TIMESTAMP WITH TIME ZONE NOT NULL, -- The timestamp when the block was produced
    block_hash TEXT NOT NULL UNIQUE, -- Unique hash of the block used for block identification
    author_account_id VARCHAR(64) NOT NULL, -- Account ID of the block producer (validator)
    approvals BIGINT, -- Number of approvals (signatures) from validators for this block
    PRIMARY KEY (block_height)
);

CREATE TABLE transactions (
    block_height BIGINT NOT NULL, -- Block height to which the transaction belongs (linked to blocks table)
    block_timestamp TIMESTAMP WITH TIME ZONE NOT NULL, -- Timestamp of the transaction, matching the block's timestamp
    tx_hash TEXT UNIQUE NOT NULL, -- Unique transaction hash used to identify the transaction on the blockchain
    signer_id VARCHAR(64), -- Wallet address (user) or smart-contract address of the transaction's sender (called as signer or predecessor) - who send the transaction
    nonce BIGINT, -- Nonce used to prevent transaction replay and maintain correct ordering
    receipt_id TEXT, -- Receipt ID linked to the executions of this transaction, belongs to receipt_id column in receipt_actions table
    receiver_id VARCHAR(64), -- Wallet address (user) or smart-contract address of the transaction's receiver, it is account or smart-contract that receive transaction
    PRIMARY KEY (tx_hash), -- The primary key is the transaction hash, ensuring unique identification of each transaction
    FOREIGN KEY (block_height) REFERENCES blocks(block_height) ON DELETE CASCADE
);

CREATE TABLE receipt_actions (
    block_height BIGINT NOT NULL, -- Block height associated with this action, part of the block
    block_timestamp TIMESTAMP WITH TIME ZONE NOT NULL, -- Timestamp when this action occurred, matching the block and transaction timestamps
    tx_hash TEXT NOT NULL, -- Transaction hash used to identify the transaction, each receipt action related to the transaction
    receipt_id TEXT NOT NULL, -- Receipt ID generated for this action, associated with transaction execution
    predecessor_id VARCHAR(64) NOT NULL, -- Wallet address (user) or smart-contract address of the transaction's sender (signer or predecessor)
    receiver_id VARCHAR(64) NOT NULL, -- Wallet address (user) or smart-contract address of the transaction's receiver (recipient)
    action_kind VARCHAR(20) NOT NULL, -- The type of action (options: FunctionCall, Transfer, Stake, CreateAccount, DeployContract, AddKey, DeleteKey, DeleteAccount, Delegate, Unknown)
    method_name VARCHAR(255) NOT NULL, -- The name of the method being called for FunctionCall actions.
    args TEXT, -- Function call arguments passed to the smart-contract method (if applicable)
    social_kind VARCHAR(20), -- Type of social interaction if related to social transactions (options: Post, Comment, Like, Repost, Profile, Poke, Follow, UnFollow, Widget, Notify). This actions related only to the NEAR Social (social.near calls).
    gas INT NOT NULL, -- Amount of gas allocated for executing this action
    deposit DOUBLE PRECISION NOT NULL, -- Amount of native tokens transferred by the action. Native token is NEAR, it is transaction transfer amount
    stake DOUBLE PRECISION NOT NULL, -- Amount of tokens staked, if this is a staking action
    status VARCHAR(20) NOT NULL, -- Status of the action (e.g., Success, Failure). Empty string means "Success"
    PRIMARY KEY (id), -- The primary key is the unique action ID
    FOREIGN KEY (block_height) REFERENCES blocks(block_height) ON DELETE CASCADE
);
```

### SQL Examples

```sql
-- Count of blocks after a certain date:
SELECT COUNT(*) FROM blocks WHERE block_timestamp > '2023-10-01';

-- Retrieve info of the latest block:
SELECT block_hash, author_account_id FROM blocks ORDER BY block_height DESC LIMIT 1;

-- Find the number of transactions in a specific block:
SELECT COUNT(*) FROM transactions WHERE block_height = 127000000;

-- Count of unique signer_id calling receiver_id in the last month:
SELECT COUNT(DISTINCT signer_id) FROM transactions WHERE block_timestamp >= NOW() - INTERVAL '1 month';

-- List of last 1000 tx_hash for transactions where signer_id contains ".some.value":
SELECT tx_hash FROM transactions WHERE signer_id LIKE '%.some.value' ORDER BY block_timestamp DESC LIMIT 1000;

-- Retrieve the last 5 transactions with the highest NEAR transfer amount:
SELECT * FROM receipt_actions ORDER BY deposit DESC LIMIT 5;

-- Retrieve last comments on 'social.near':
SELECT * FROM receipt_actions WHERE receiver_id = 'social.near' AND social_kind = 'Comment' AND status = 'Success' ORDER BY block_timestamp DESC LIMIT 10;

-- Unique tx_hash for transfers from "earn.kaiching" over 1 NEAR:
SELECT DISTINCT tx_hash FROM receipt_actions WHERE predecessor_id = 'earn.kaiching' AND deposit > 1 AND action_kind = 'Transfer' AND status = 'Success';

-- All FT transfers for 1 October 2024:
SELECT * FROM receipt_actions WHERE method_name = 'ft_transfer' AND block_timestamp >= '2024-10-01' AND block_timestamp < '2024-10-02'  AND status = 'Success';

-- Failed calls to "some.near":
SELECT * FROM receipt_actions WHERE receiver_id = 'some.near' AND action_kind = 'FunctionCall' AND status = 'Failure';

-- Find the number of unique accounts that staked in the last week:
SELECT COUNT(DISTINCT predecessor_id) FROM receipt_actions WHERE action_kind = 'Stake' AND block_timestamp >= NOW() - INTERVAL '1 week';

-- New wallet accounts created in the last 3 days:
SELECT * FROM receipt_actions WHERE action_kind = 'CreateAccount' AND block_timestamp >= NOW() - INTERVAL '3 day' AND status = 'Success';

-- Unique wallets that deployed contracts after block 1,000,000:
SELECT DISTINCT predecessor_id FROM receipt_actions WHERE action_kind = 'DeployContract' AND block_height > 128000000;

-- Top 500 wallets/smart-contracts by gas used in the last 1 month:
SELECT predecessor_id, SUM(gas) AS total_gas FROM receipt_actions WHERE block_timestamp >= NOW() - INTERVAL '1 month' GROUP BY predecessor_id ORDER BY total_gas DESC LIMIT 500;

-- Find the top 10 receivers with the highest total deposits:
SELECT receiver_id, SUM(deposit) AS total_deposits FROM receipt_actions GROUP BY receiver_id ORDER BY total_deposits DESC LIMIT 10;

-- First 100 NFT transfers:
SELECT * FROM receipt_actions WHERE method_name = 'nft_transfer' AND status = 'Success' ORDER BY block_timestamp LIMIT 100;

-- Get top 1000 actions by staking amount for accounts receiving NEAR staking in the last year:
SELECT receiver_id, stake FROM receipt_actions WHERE action_kind = 'Stake' AND block_timestamp >= NOW() - INTERVAL '1 year' AND status = 'Success' ORDER BY stake DESC LIMIT 1000;

-- Count of actions with social_kind equal to "Follow":
SELECT COUNT(*) FROM receipt_actions WHERE social_kind = 'Follow';

-- Average gas used for FunctionCall actions in the last week:
SELECT AVG(gas) FROM receipt_actions WHERE action_kind = 'FunctionCall' AND block_timestamp >= NOW() - INTERVAL '1 week';

-- Distinct predecessor_id for accounts involved in failed actions:
SELECT DISTINCT predecessor_id FROM receipt_actions WHERE status = 'Failure';

-- Get transactions that sent more than 100 NEAR in last 3 month:
SELECT * FROM receipt_actions WHERE deposit > 100 AND status = 'Success';

-- Get new wallets created last 48 hours, that use near social.
SELECT * FROM receipt_actions WHERE predecessor_id IN (SELECT DISTINCT predecessor_id FROM receipt_actions WHERE action_kind = 'CreateAccount' AND block_timestamp >= NOW() - INTERVAL '48 hours') AND receiver_id = 'social.near';
```

### Answer

Return the SQL query without any additional text, symbols, or comments:

[QUESTION]{user_question}[/QUESTION]

Return only the SQL query and **nothing else**. Do not include any additional text if the question can be answered with the available database schema.