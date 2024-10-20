### Task

Generate a response to answer the user’s question by using the instructions and the provided data in the `Data to Analyze` section. 
The data represents the result of data from the NEAR Protocol blockchain database.

### Instructions

- The question relay on NEAR blockchain-specific terms, particularly can include blockchain transactions, receipts, accounts, tokens, smart-contracts, and called methods or arguments. 
- The answer can include a detailed analysis of patterns, insights, or summaries based on the user's query.
- Do not repeat user request, include only the answer to the user's question. Do not tell that information related to NEAR blockchain, user already knows that, provide only the answer to the user's question.
- Do not describe data structures or blockchain related terms, the user is already familiar with them - main focus on the answer to the user's question based on provided data.
- The `NEAR Blockchain Overview` section outlines relevant terms and relationships. Use it as a reference to generate accurate answers.
- The `Token Transactions`, `Smart Contract`, `Cross-Chain Transactions`, `Social Transactions` sections describe specific transaction types and their attributes.

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

{table_metadata}

### Data to Analyse

{data}
