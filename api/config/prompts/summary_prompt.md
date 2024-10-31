### Task

Generate a response to answer the user question: `{user_question}`.
Use `Instructions` and other sections for context and the provided data in the `Data to Analyze` section for analyze data.

### Instructions

- The question relay on NEAR blockchain-specific terms, particularly can include blockchain transactions, receipts, accounts, tokens, smart-contracts, and called methods or arguments.
- The answer can include a detailed analysis of patterns, insights, or summaries based on the user's query.
- Do not repeat user request, include only the answer to the user's question. Do not tell that information related to NEAR blockchain, user already knows that, provide only the answer to the user's question.
- Do not describe data structures or blockchain related terms, the user is already familiar with them - main focus on the answer to the user's question based on provided data.
- The `NEAR Blockchain Overview` section outlines relevant terms and relationships. Use it as a reference to generate accurate answers.
- The `Token Transactions`, `Smart Contract`, `Cross-Chain Transactions`, `Social Transactions` sections describe specific transaction types and their attributes.
- If there is no data provided in the `Data to Analyze` section - respond "No data to analise".

#### NEAR Blockchain Overview

NEAR Protocol is a layer-1 blockchain. Key components include:

- Blocks: Captured in the "blocks" table.
- Transactions: Stored in the "transactions" table.
- Receipt Actions: Found in the "receipt_actions" table.

More details about each component described in the "Database Schema" section.

#### Token Transactions

Fungible Tokens (FT) actions follow NEP-141 or NEP-148 standards and are recorded in the "receipt_actions" table:

Common methods include "ft_transfer", "ft_transfer_call", and "storage_deposit".
The args column contains information like the "recipient account" and "amount" (referring to the FT amount).
For Non-Fungible Tokens (NFTs), actions follow NEP-171 and NEP-177 standards and include methods like "nft_transfer", "nft_mint", and "nft_approve".

#### Smart Contract

Smart contracts are deployed and managed via FunctionCall actions, captured in the receipt_actions table.
Smart contract details (e.g., code hash, initialization parameters) are available in the args column.

#### Cross-Chain Transactions

- Cross-chain activity can be identified using specific receiver accounts like v1.signer in the transactions table.

#### Social Transactions

NEAR blockchain also supports NEAR Social - a decentralized social media platform.
Actions related to social transactions can be found in the `receipt_actions` table.
These actions are identified by the "social_kind" column, with potential values like:

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

### Data to Analyse

{data}

### Answer

The following answer for the question `{user_question}`: