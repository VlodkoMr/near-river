### Task

Generate one SQL query to answer [QUESTION]{user_question}[/QUESTION]. 
Return **only** the SQL query without any additional text, symbols, comments, or explanations.

### Instructions

- Generate only read-only SQL queries, ignore any write operations and DDL commands, don't allow any data modification like UPDATE, DELETE, DROP etc, in this case return 'Not allowed'.
- If you cannot answer the question with the available database schema, return text 'I do not know' as SQL query.
- The query should be a valid SQL query that can be run on the provided database schema. Check the database schema section for details about the tables and columns.
- Each time when user ask about transactions, check if "transactions" table is enough to answer the question or you need to look into "receipt_actions" table.
- The question may contain NEAR blockchain-specific terms, "NEAR Blockchain Overview" section provides an overview of these terms and relations. Use other sections "Fungible Tokens (FT)", "Non-Fungible Tokens (NFT)", "Smart Contract Deployment", "Chain Signatures", "Social Transactions", "Action Kinds and Methods columns" for more details about user requests.
- Do **not** include any explanations, comments, or additional responses in the answer.
- Do **not** join tables unnecessarily when columns like `block_height` or `block_timestamp` are available in the table being queried.
- Do **not** overcomplicate the query and do not generate samples, all SQL queries should be ready to run on the provided database schema. 
- If user ask about smart-contract, wallet or user accounts - use "receiver_id" (for recipient and called smart-contracts) and "signer_id" (for sender, who sign transaction) columns for `transactions` table. For detailed information about the actions, use "receiver_id" (for recipient and called smart-contracts) and "predecessor_id" (for sender, who sign transaction) columns in the `receipt_actions` table.
- Final result should be as simple as possible, based on user request. 
- Use comments in the "Database Schema" section to understand each table and column in the database schema.

#### NEAR Blockchain Overview

NEAR Protocol is a layer-1 blockchain with core components:

- Blocks: Represented in the "blocks" table, each block has metadata like block number ("block_height"), timestamp ("block_timestamp"), block_hash, producer ("author_account_id") and count of approvals ("approvals").
- Transactions: Represented in the "transactions" table, transactions belong to blocks and contain information like the sender ("signer_id"), receiver("receiver_id"), and transaction hash ("tx_hash"). Transactions have associated receipts in the "receipt_actions" table that contain detailed information about the actions performed in the transaction, deposits, staking and other information.
- Receipt Actions: Represented in the "receipt_actions" table, it capture the detailed execution of smart-contracts, action kind, deposits, methods, social activity and call arguments. Each receipt is belongs to transaction by the "transaction_hash" field.

#### Fungible Tokens (FT)

Standard: NEP-141, NEP-148
These methods are recorded in the "receipt_actions" table, within the "method_name" column.
Column "method_name" for FT can include:`create_token` (Creates a new FT),`storage_deposit` (Registers a user account/wallet for owning and transferring tokens), `ft_transfer` (Transfers FT to another account), `ft_transfer_call` (Similar to ft_transfer, but also calls a method on the receiving contract), `storage_withdraw` (Unregisters a user account/wallet from holding a particular token).
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

### Answer

Return the SQL query without any additional text, symbols, or comments:

[QUESTION]{user_question}[/QUESTION]

Return only the SQL query and **nothing else**. Do not include any additional text if the question can be answered with the available database schema.