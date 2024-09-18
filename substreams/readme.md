# Substreams for NEAR Watch

## Requirements
- [substreams-sink-sql](https://github.com/streamingfast/substreams-sink-sql)
- Rust 1.72+

## Usage

#### On proto update, regenerate protobuf files:
```bash
make protogen
```

#### Build module:
```bash
cargo build --target wasm32-unknown-unknown --release
```

#### Set JWT key for substreams:
```bash
SUBSTREAMS_API_TOKEN="your-jwt-token"
```
Note: To get SUBSTREAMS_API_TOKEN, you need to follow [Substreams Auth Documentation](https://substreams.streamingfast.io/documentation/consume/authentication).

### Option #1: Postgresql

#### Postgresql create database:
```bash
substreams-sink-sql setup "psql://postgres:secret@127.0.0.1:5432/substreams_example?sslmode=disable" ./substreams.postgresql.yaml
```

#### Postgresql start data sync:
```bash
substreams-sink-sql run "psql://postgres:secret@127.0.0.1:5432/substreams_example?sslmode=disable" ./substreams.postgresql.yaml
```

#### Postgresql resume data sync:
```bash
substreams-sink-sql run "psql://postgres:secret@127.0.0.1:5432/substreams_example?sslmode=disable" ./substreams.postgresql.yaml \
--on-module-hash-mistmatch warn
```

### Option #2: ClickHouse

#### ClickHouse create database:
```bash
substreams-sink-sql setup "clickhouse://default:@127.0.0.1:9000/default" ./substreams.clickhouse.yaml
```

#### ClickHouse start data sync / use $SUBSTREAMS_API_TOKEN:
```bash
substreams-sink-sql run "clickhouse://default:@127.0.0.1:9000/default" ./substreams.clickhouse.yaml \
--undo-buffer-size 50000
```

#### ClickHouse start data sync / use API Key:
```bash
SUBSTREAMS_API_KEY="your-api-key"

substreams-sink-sql run "clickhouse://default:@127.0.0.1:9000/default" ./substreams.clickhouse.yaml \
--header "x-api-key:$SUBSTREAMS_API_KEY" --undo-buffer-size 50000
```
Note: Replace "your-api-key" to your substreams API key.

#### ClickHouse resume data sync:
```bash
substreams-sink-sql run "clickhouse://default:@127.0.0.1:9000/default" ./substreams.clickhouse.yaml \
--undo-buffer-size 50000 --on-module-hash-mistmatch warn
```

Note: Replace DB connection credentials.
Read more: https://substreams.streamingfast.io/documentation/consume/authentication