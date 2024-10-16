### Task

Generate a SQL query to answer [QUESTION]{user_question}[/QUESTION]

### Instructions

- Generate only read-only SQL queries, ignore any write operations and DDL commands.
- If you cannot answer the question with the available database schema, return 'I do not know.'
- The query should be a valid SQL query that can be run on the provided database schema.
- The SQL schema represents NEAR Protocol blockchain data: blocks, transactions, and receipt actions (receipt_actions).
- Make use of available indexes for efficient query generation when necessary.

The question may contain NEAR blockchain-specific terms, especially related to blockchain transactions, receipts, accounts, tokens, contracts, and methods.
Here are some relevant concepts and terms to help generate correct queries:

#### NEAR Blockchain Overview

NEAR Protocol is a layer-1 blockchain focusing on usability, scalability, and smart contract execution.
Its core components are blocks, transactions, and receipts.
Each component is represented in the database schema:

- Blocks: Represented in the blocks table, each block has metadata like height, timestamp, producer (author), and approvals.
- Transactions: Represented in the transactions table, transactions belong to blocks and contain information like the sender (signer), receiver, and transaction hash. Transactions may have associated receipts representing contract actions.
- Receipt Actions: Represented in the receipt_actions table, receipt actions capture the detailed execution of contracts and methods related to transactions.

##### Fungible Tokens (FT)

Standard: NEP-141, NEP-148
These methods are recorded in the `receipt_actions` table, within the `method_name` column.
Each method’s arguments are stored in JSON format in the `args` column.

Key methods:

- `create_token`: Creates a new FT. The `args` field contains the `owner_id`, `total_supply`, and `metadata` fields.
- `storage_deposit`: Registers a user account (wallet) for owning and transferring tokens. Registration is necessary before users can hold tokens.
- `ft_transfer`: Transfers FT to another account. The `args` field contains `receiver_id` and `amount`.
- `ft_transfer_call`: Similar to ft_transfer, but also calls a method on the receiving contract. `args` contains `receiver_id`, `amount`, and `msg`.
- `storage_withdraw`: Unregisters a user account (wallet) from holding a particular token.

Additional details: `predecessor_id` refers to the sender and `receiver_id` refers to the recipient.

##### Non-Fungible Tokens (NFT)

Standard: NEP-171, NEP-177
These methods are also recorded in the receipt_actions table under the method_name column.
Each method’s arguments are stored in JSON format in the `args` column.

Key methods:

- `nft_mint`: Mints a new NFT, recording it to the blockchain. The `args` field contains `token_id`, `receiver_id`, and `token_metadata`.
- `nft_transfer`: Transfers NFT ownership to another account. `args` contains `receiver_id` and `token_id`.
- `nft_transfer_call`: Transfers an NFT and invokes a method on the receiver contract. `args` contains `receiver_id`, `token_id`, and `msg`.
- `nft_approve`: Approves the transfer of an NFT. `args` contains `account_id`, `msg`, and `token_id`.

Additional details: `predecessor_id` refers to the sender and `receiver_id` refers to the recipient.

##### Smart Contract Deployment

Smart contracts are deployed using the deploy method in the `receipt_actions` table.
The `args` field contains details about the deployment in JSON format, including:

- `code_hash`: The hash of the contract code being deployed.
- `storage_deposit`: The amount of storage allocated for the contract.
- `init`: Initialization parameters for the smart contract.

##### Chain Signatures (Multi-chain Transactions)

NEAR supports cross-chain transactions via chain signatures.
Such transactions can be identified in the transactions table when the `receiver_id` column contains "v1.signer".
These transactions allow NEAR accounts (including smart contracts) to sign and execute transactions across multiple blockchain protocols.
More details about chain signature-related actions can be found in the `receipt_actions` table by filtering with `receiver_id` for relevant accounts.

##### Social Transactions

NEAR blockchain also supports NEAR Social - a decentralized social media platform.
Actions related to social transactions can be found in the receipt_actions table.
These actions are identified by the `social_kind` column, with potential values like:
`Post`, `Comment`, `Like`, `Repost`, `Profile`, `Poke`, `Follow`, `UnFollow`, `Widget`, `Notify`.

##### Action Kinds

Receipt actions (`receipt_actions`.`action_kind`) include various methods for different on-chain activities, including:

- Account management: `CreateAccount`, `DeleteAccount`
- Key management: `AddKey`, `DeleteKey`
- Staking: `Stake` (NEAR native staking mechanism)
- Delegation: `Delegate` (delegating actions to another account)
- Fund Transfers: `Transfer` (native token transfers in NEAR)

Each action type can be identified using the `action_kind` column and `method_name` column contain the specific method called within the action.
Specific arguments passed to the method can be found in the `args` column in JSON format.

### Database Schema

The query will run on a database with the following schema:
{table_metadata_string}

### Answer

Given the database schema, here is the SQL query that answers [QUESTION]{user_question}[/QUESTION]
[SQL]