# NEAR River

NEAR River is a robust solution for quickly building and launching custom indexers with API for the NEAR blockchain.
It offers a user-friendly interface to access any data — whether historical or live, using Substreams for blocks, transactions, and receipts.
You can easily customize filters, store the exact data you need in a database, and query through a pre-built,
extendable API with integrated AI support.

### Key Features:

- **Effortless Custom NEAR Indexer Setup:** Just edit the .env files and run Docker — it's that simple!
- **Pre-built API with Customizable Endpoints:** Access transactions, receipts, blocks, and general blockchain data.
- **Scalable and Flexible Architecture:** Extend both the indexer and API with your custom logic — it's fully open-source.
- **Comprehensive Blockchain Data Access:** Retrieve any historical or real-time data using Substreams without the need to run your own node.
- **Optimized Data Storage:** Efficiently store all useful NEAR blockchain data in just 500GB of drive space.
- **NEAR Social Integration:** Parse `social.near` events for enhanced search and filtering capabilities.
- **AI-Powered Analytics:** Gain valuable insights and data analytics directly from your setup with integrated AI.
- **No External API Usage for AI:** Enjoy unlimited AI queries without rate or data limits, and no extra costs — the AI runs on your own machine!
- **User-defined Event Subscriptions:** Define specific conditions or events to listen for and push these updates through a HTTP or smart-contract, providing real-time, filtered data streams.

## Requirements

- Docker
- CUDA toolkit + NVidia GPU (for AI model), only Linux and Windows are supported for now.

## Installation

1. Get your `SUBSTREAMS_API_KEY` from https://app.streamingfast.io/keys.

2. Clone the repository:

    ```bash
    git clone https://github.com/VlodkoMr/near-river.git
    ```
3. Copy `.env.example` to `.env`, update it with your configurations and run docker build:

    ```bash
    cp substreams/.env.example substreams/.env
    cp api/.env.example api/.env
    docker-compose build
    ```

### Substreams environment (substreams/.env file)

- `SUBSTREAMS_API_KEY` - Your Substreams API key.
- `DB_CONNECTION` - Database connection string.
- `START_BLOCK` - The starting block for the indexer. Use "latest" to start from the latest block at launch.
- `END_BLOCK` - The ending block for the indexer. Leave it empty to track all blocks, or set a block number to stop processing before that block.
- `FILTERED_RECEIVER_IDS` - A comma-separated list of transaction receivers (smart-contract that user call or tx recipient) to filter transactions and receipts. Empty string to process all transactions.
- `FILTERED_METHOD_NAMES` - A comma-separated list of method names to filter receipts. Empty string to store all calls (filter disabled).

### API environment (api/.env file)

- `DB_CONNECTION` - Database connection string.
- `API_SECRET_KEY` - API secret key for authentication. Empty string to make the API public.
- `EVENT_BATCH_BLOCKS_COUNT` - how much blocks process in one batch, set "0" to disable event listeners.
- `EVENT_FILTER_SENDER` - Filter events by sender account ID. Empty string to process all events. In most cases you will need complex rules or logic, this is just for example, customise event listeners in `api/event_subscription_service.py`.
- `EVENT_FILTER_RECIPIENT` - Filter events by recipient account ID. Empty string to process all events.
- `EVENT_NOTIFICATION_TARGET` - Call smart-contract or make http request. For smart-contract use format "some-contract.near|method_name". For HTTP call provide URL like "https://website.com/some_url", it will be called using POST method.
- `EVENT_NEAR_ACCOUNT_ID` - NEAR Account address for event notifications. Required for smart-contract calls.
- `EVENT_NEAR_ACCOUNT_PRIVATE_KEY` - NEAR Account private key for event notifications. Required for smart-contract calls.

#### Download AI Models:

You can use any AI model for this project. In our example, we use "llama-3-sqlcoder-8b" for SQL generation and "Llama-3.2-1B-Instruct" for data analyse from Hugging Face. To download it, follow these steps:

- Install the Hugging Face CLI: https://huggingface.co/docs/huggingface_hub/guides/cli
- Log in to your Hugging Face account:

```bash
huggingface-cli login
```

- Download the model to /api/config/ai_models/ directory:

```bash
cd api/
huggingface-cli download defog/llama-3-sqlcoder-8b --local-dir config/ai_models/llama-3-sqlcoder-8b
huggingface-cli download meta-llama/Llama-3.2-1B-Instruct --local-dir config/ai_models/Llama-3.2-1B-Instruct
```

## Running the Project

#### Start with GPU (see requirements):

```bash
docker-compose -f docker-compose.yml -f docker-compose.gpu.yml up
```

#### Start without GPU:

```bash
docker-compose up
```

#### Reset the Database:

To reset the database, remove the `substreams_init.lock` file and restart docker:

```bash
# stop docker
rm ./substreams/substreams_init.lock
# start docker
```

#### Usage

After running docker - substreams will begin collecting data from the NEAR blockchain, using the configurations from your environment settings.
API endpoints will be available for querying the database, all endpoints are documented in the [http://localhost:3000/docs](http://localhost:3000/docs).

If you run docker with GPU support, you can use the AI-powered API to query the database with AI-generated SQL queries, ask questions about the data, and get insights:

#### AI Usage

To use the AI features, ensure that the API is running with GPU support and that the AI model has been downloaded as described earlier.
The following AI endpoints are available:

- POST `/api/analytics/sql` - Submit a data-related question, and the AI will generate the most relevant SQL query and return both the query and the resulting data. We use the `llama-3-sqlcoder-8b` model for this task to generate SQL query and request data
  from the database.
  > Request: {question: string}
  > Success response: {question: string, sql: string, data: object[]}
  > Error response: {question: string, sql: string, error: string}
- POST `/api/analytics/question` - Ask a general question about the data. The AI will internally use the `/api/analytics/sql` endpoint to retrieve and analyze the data and then process the answer using the `Llama-3.2-1B-Instruct` model.
  > Request: {sql_question: string, data_question: string}. `sql_question` is used to generate SQL query, `data_question` is used to generate the answer based on the data.
  > Success response: {question: string, answer: string}
  > Error response: {question: string, error: string}

Update AI and app settings in `api/config/settings.py` to customize the model behavior - increase the `AI_SQL_NUM_BEAMS` and `AI_SQL_MAX_TOKENS` to get better results at the cost of speed and memory.

### Why Choose NEAR River?

NEAR River is easy to set up, letting you run an indexer just in 7 minutes with real-time, stable data flow to your database.
It’s scalable, flexible, and designed to handle any amount of data with real-time updates.
The pre-built API makes querying easy, and data storage is optimized for reduced size. You can extend the indexer and API with your custom logic.

#### Comparison with Existing NEAR Indexer/API Solutions:

- **BigQuery:** Costly for reading large volumes of data, with no option to export extensive datasets.
- **QueryAPI:** Currently unstable (still in beta), with limited control over the indexing process—no ability to stop or restart the indexer.
- **Lake Framework:** Involves a complex setup, dependent on AWS, and requires an archival node for accessing historical data.
- **Pikespeak API:** A solid solution, but it's not open-source or customizable for unique use cases, and it comes with a price tag.

## TODO

- Add filter masks to extend filtering capabilities.
- Update `receipt_actions`.`args` field to JSON for better data filtering and querying.
- Leverage the integrated AI to not only query data but also to provide predictive insights and alert users about unusual patterns, such as suspicious transaction volumes or unexpected contract behaviors.