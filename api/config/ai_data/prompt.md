### Task

Generate a SQL query to answer [QUESTION]{user_question}[/QUESTION]

### Instructions

- If you cannot answer the question with the available database schema, return 'I do not know'.
- The query should be a valid SQL query that can be run on the database schema.
- SQL schema represent NEAR Protocol blockchain data: blocks, transactions and receipts (receipt_actions).

Question can contain NEAR blockchain related details, more instructions about blockchain transactions and methods:

- Fungible Tokens (FT) - implement NEP-141, NEP-148 standards. We can find this functions in `receipt_actions` table, `method_name` column:
    - `create_token` - create a new fungible token. In `receipt_actions`.`args` we have JSON string with `owner_id`, `total_supply`, `metadata` fields.
    - `storage_deposit` - Registering a FT token or NFT for user account (wallet address). In order for an user to own and transfer tokens they need to register in the contract.
    - `ft_transfer` - Method used to send FT to another account (wallet address). In `receipt_actions`.`args` we have JSON string with `receiver_id` and `amount` fields.
    - `ft_transfer_call` - Method used to send FT to another account and call a method on the receiver contract. In `receipt_actions`.`args` we have JSON string with `receiver_id`, `amount`, `msg` fields.
    - `storage_withdraw` - Unregistering a token for user (wallet address).
- Non-Fungible Tokens (NFT) - implement NEP-171 and NEP-177 standards. We can find this functions by `receipt_actions`. `method_name`:
    - `nft_mint` - To create a new NFT (a.k.a. minting it). In `receipt_actions`.`args` we have JSON string with `token_id`, `receiver_id`, `token_metadata` fields.
    - `nft_transfer` - Method used to send NFT to user account (wallet address) . In `receipt_actions`.`args` we have JSON string with `receiver_id` and `token_id`. `token_id` fields.
    - `nft_transfer_call` - Method used to send NFT to another account and call a method on the receiver contract. In `receipt_actions`.`args` we have `receiver_id`, `token_id`, `msg` fields.
    - `nft_approve` - Method used to approve NFT transfer to another account. In `receipt_actions`.`args` we have JSON string with `account_id`, `msg`, `token_id` to approve.
- Smart-contract deployment - `deploy` - Method used to deploy a new smart contract. In `receipt_actions`.`args` we have JSON string with `code_hash`, `storage_deposit`, `init` fields.
- Chain Signatures (chain abstraction) - Chain signatures enable NEAR accounts, including smart contracts, to sign and execute transactions across many blockchain protocols. We can find this transactions using `transactions` table and `receiver_id`
  column, it will contain "v1.signer". More information we can find in the `receipt_actions` table using `receiver_id` for filtering.

### Database Schema

The query will run on a database with the following schema:
{table_metadata_string}

### Answer

Given the database schema, here is the SQL query that answers [QUESTION]{user_question}[/QUESTION]
[SQL]