### Task

Generate response to answer [QUESTION]{user_question}[/QUESTION] using instructions and provided data in section `Data to Analyse`.
Provided data is SQL-query results from NEAR Protocol blockchain database.

### Instructions

The question related NEAR blockchain-specific terms, especially related to blockchain transactions, receipts, accounts, tokens, contracts, and methods.
"NEAR Blockchain Overview" section provides an overview of these terms and relations.

##### NEAR Blockchain Overview

NEAR Protocol is a layer-1 blockchain with core components:

- Blocks: Represented in the "blocks" table, each block has metadata like block number ("block_height"), timestamp ("block_timestamp"), block_hash, producer ("author_account_id") and count of approvals ("approvals").
- Transactions: Represented in the "transactions" table, transactions belong to blocks and contain information like the sender ("signer_id"), receiver("receiver_id"), and transaction hash ("tx_hash"). Transactions have associated receipts in the "
  receipt_actions" table that contain detailed information about the actions performed in the transaction, deposits, staking and other information.
- Receipt Actions: Represented in the "receipt_actions" table, it capture the detailed execution of smart-contracts, action kind, deposits, methods, social activity and call arguments. Each receipt is belongs to transaction by the "transaction_hash"
  field.

##### Fungible Tokens (FT)

Standard: NEP-141, NEP-148
These methods are recorded in the "receipt_actions" table, within the "method_name" column. Each method’s arguments are stored in JSON format in the "args" column.

Column "method_name" for FT can include:`create_token` (Creates a new FT),`storage_deposit` (Registers a user account/wallet for owning and transferring tokens), `ft_transfer` (Transfers FT to another account), `ft_transfer_call` (Similar to
ft_transfer, but
also calls a method on the receiving contract), `storage_withdraw` (Unregisters a user account/wallet from holding a particular token).

Column "predecessor_id" refers to the sender and "receiver_id" refers to the recipient.

#### Non-Fungible Tokens (NFT)

Standard: NEP-171, NEP-177
These methods are also recorded in the "receipt_actions" table under the "method_name" column.
Each method’s arguments are stored in JSON format in the "args" column.

Column "method_name" for NFT can include:`nft_mint`: (Mints a new NFT),`nft_transfer` (Transfers NFT ownership to another account), `nft_transfer_call` (Transfers an NFT and invokes a method on the receiver contract), `nft_approve` (Approves the
transfer of
an NFT.
Column "predecessor_id" refers to the sender and "receiver_id" refers to the recipient.

#### Smart Contract Deployment

Smart contracts are deployed using the deploy method in the "receipt_actions" table.
The "args" column contains details about the deployment in JSON format, including:

- `code_hash`: The hash of the contract code being deployed.
- `storage_deposit`: The amount of storage allocated for the contract.
- `init`: Initialization parameters for the smart contract.

#### Chain Signatures (Multi-chain Transactions)

NEAR supports cross-chain transactions via chain signatures.
Such transactions can be identified in the transactions table when the "receiver_id" column contains `v1.signer`.
More details about chain signature-related actions can be found in the "receipt_actions" table by filtering with "receiver_id" for relevant accounts.

#### Social Transactions

NEAR blockchain also supports NEAR Social - a decentralized social media platform.
Actions related to social transactions can be found in the receipt_actions table.
These actions are identified by the "social_kind" column, with potential values like:
`Post`, `Comment`, `Like`, `Repost`, `Profile`, `Poke`, `Follow`, `UnFollow`, `Widget`, `Notify`.

#### Action Kinds and Methods columns

Receipt actions "receipt_actions" table, "action_kind" column include various methods for different on-chain activities, including:

- Contract Calls: `FunctionCall` (calling a method on a smart-contract)
- Account management: `CreateAccount`, `DeleteAccount`
- Key management: `AddKey`, `DeleteKey`
- Staking: `Stake` (NEAR native staking)
- Delegation: `Delegate` (delegating actions to another account)
- NEAR token transfers: `Transfer` (only for native NEAR token)
- Deploying a smart-contract: `DeployContract` (deploying a new smart contract)

Each action type can be identified using the "action_kind", and "method_name" column contain the specific method called within the action.
Specific arguments passed to the method can be found in the "args" column, it use JSON format.

### Data to Analyse

{data}

### Answer

Given the data and instructions, here is the answers [QUESTION]{user_question}[/QUESTION]
