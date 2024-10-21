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
- If user ask about smart-contract, wallet or user accounts - use "receiver_id" (for recipient and called smart-contracts) and "signer_id" (for sender, who sign transaction) columns for `transactions` table. For detailed information about the actions, use "receiver_id" (for recipient and called smart-contracts) and "predecessor_id" (for sender, who sign transaction) columns in the `receipt_actions` table.
- Final result should be as simple as possible, based on user request. Do not overcomplicate the query.

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

{table_metadata_string}

### Answer

Return the SQL query without any additional text, symbols, or comments:

[QUESTION]{user_question}[/QUESTION]

Return only the SQL query and **nothing else**. Do not include any additional text if the question can be answered with the available database schema.