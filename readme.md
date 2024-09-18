# NEAR Watch

NEAR Watch is a powerful tool for building and fast launching custom indexers on the NEAR blockchain. 
It provides an easy-to-use interface for tracking blockchain events and querying data through APIs.

Features:
- Fast setup for custom NEAR indexers
- Real-time event tracking and API support
- Scalable and flexible architecture
- Get all historical data for NEAR blockchain, no need to run archival node
- Small size of data storage - optimised for most-important data only
- NEAR Social support - parse all social.near events for better search and filter
- Clickhouse and Postgresql support

## Requirements

- Rust 1.72+
- [substreams 1.10.4+](https://github.com/streamingfast/substreams/releases)
- [substreams-sink-sql 4.2.1+](https://github.com/streamingfast/substreams-sink-sql/releases)
- [Clickhouse](https://clickhouse.com/docs/en/install) or PostgreSQL database

## Install

Get your SUBSTREAMS_API_KEY from https://app.streamingfast.io/keys

1. Clone repo
2. Copy `.env.example` to `.env` and update with your configurations:
```bash
cp .env.example .env
```

3. Build:
```bash
npm run substreams:build
npm run substreams:init:local
```
4. Update your API TOKEN:
```bash
npm run substreams:rorate_token:local
```
5. Start listener:
```bash
npm run substreams:start:local
```