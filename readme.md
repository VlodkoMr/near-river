# NEAR River

NEAR River is a powerful tool for building and quickly launching custom indexers on the NEAR blockchain using Substreams.
It provides an easy-to-use interface for get any data (historical or live) on NEAR blockchain: blocks, transactions and receipts.
You can customise to filter and storing any data that you need in a database, and querying through a pre-built, extendable API.

### Key Features:

- Simplest setup for custom NEAR indexer: just edit `.env` files and run docker!
- Pre-build API with endpoints customisation: get transactions, receipts, blocks, and general KPI data.
- Scalable and flexible design: you can extend indexer and API with your custom logic, project is open-source.
- Access to all historical NEAR blockchain data without the need to run a node.
- Optimized data storage for reduced size. All NEAR blockchain data can be stored in 500Gb drive!
- NEAR Social support - parse all `social.near` events for better search and filtering.
- AI to get powerful data analytics and insights.

### Comparison with Existing NEAR Indexer/API Solutions:

- **BigQuery** - Expensive when reading large amounts of data.
- **QueryAPI** - Unstable (under beta testing), no control on indexing (no way to stop or restart indexer).
- **Lake Framework** - Complex setup, relies on AWS. Require archival node to get historical data.
- **Pikespeak API** - A great solution, but not open-source or extendable for custom needs, paid.

## Requirements

- Docker
- huggingface-cli

## Installation

1. Get your `SUBSTREAMS_API_KEY` from https://app.streamingfast.io/keys.

2. Clone the repository:

    ```bash
    git clone https://github.com/VlodkoMr/near-river.git
    ```
3. Copy `.env.example` to `.env` and update it with your configurations:

    ```bash
    cp substreams/.env.example substreams/.env
    cp api/.env.example api/.env
    ```

### Substreams environment (substreams/.env file)

- `SUBSTREAMS_API_KEY` - Your Substreams API key.
- `DB_CONNECTION` - Database connection string.
- `START_BLOCK` - The starting block for the indexer. Use "latest" to start from the latest block at launch.
- `END_BLOCK` - The ending block for the indexer. Leave it empty to track all blocks, or set a block number to stop processing before that block.
- `FILTERED_RECEIVER_IDS` - A comma-separated list of transaction receivers (smart-contract that user call or tx recipient) to filter transactions and receipts.
  Empty string to process all transactions.
- `FILTERED_METHOD_NAMES` - A comma-separated list of method names to filter receipts. Empty string to process all receipts.
- `MAX_ARGS_LENGTH` - The maximum length of the arguments string to store in the database. This helps save disk space by limiting the argument string length.

### API environment (api/.env file)

- `DB_CONNECTION` - Database connection string.

#### Download AI Model:

```bash
huggingface-cli login
huggingface-cli download defog/sqlcoder-7b-2 --local-dir api/config/ai_models/sqlcoder-7b-2
```

## Running the Project

#### Start the Application:

```bash
docker-compose build
docker-compose up
```

#### Stop the Application:

```bash
docker-compose down --remove-orphans
```

#### Reset the Database:

```bash
rm ./substreams/substreams_init.lock
docker-compose up
```

#### Usage

http://localhost:3000/ - API endpoint
http://localhost:3000/docs - API documentation

### Why Choose NEAR River?

NEAR River is easy to set up, letting you run an indexer just in 10 minutes with real-time, stable data flow to your database.
It’s scalable, flexible, and designed to handle any amount of data with real-time updates.
The pre-built API makes querying easy, and data storage is optimized for your data.

API contain AI and event listeners:

- In background tasks we process, transform and store vector data for AI.
- Event listeners can be used to trigger calls to NEAR/EVM chains based on your custom logic.

## TODO

- Add address mask filters to extend filtering capabilities.