mod pb;
mod utils;
pub mod config;

use std::collections::HashMap;
use substreams_near::pb::sf::near::r#type::v1::{Block, BlockHeader, IndexerChunk, IndexerShard, SignedTransaction};
use substreams_database_change::pb::database::{DatabaseChanges, table_change::Operation};
use substreams_near::pb::sf::near::r#type::v1::execution_outcome::Status;
use crate::pb::near::custom::v1::{BlockDataOutput, BlockMeta, ReceiptActionMeta, TransactionMeta};
use substreams_near::pb::sf::near::r#type::v1::receipt::Receipt as ReceiptTypes;
use crate::utils::block_timestamp::BlockTimestamp;
use crate::utils::helpers::{bs58_hash_to_string, generate_hash_pk};
use crate::utils::transform::{transform_action, transform_transaction};
use crate::config::{FILTERED_RECEIVER_IDS, FILTERED_METHOD_NAMES, END_BLOCK};

#[substreams::handlers::map]
fn store_transactions(blk: Block) -> BlockDataOutput {
    // Extract block metadata if available
    let (transactions, receipt_actions, block_meta) = blk.header.as_ref().map_or(
        (Vec::new(), Vec::new(), None),
        |block_header| {
            if let Some(end_block) = *END_BLOCK {
                if block_header.height > end_block {
                    // Return empty data if the block height exceeds END_BLOCK
                    return (Vec::new(), Vec::new(), None);
                }
            }

            let timestamp = BlockTimestamp::from_block(block_header);
            let block_meta = BlockMeta {
                block_height: block_header.height,
                block_timestamp: timestamp.timestamp(),
                block_hash: bs58_hash_to_string(block_header.hash.clone()),
                author_account_id: blk.author.clone(),
                approvals: block_header.approvals.len() as u64,
            };

            let mut all_statuses = HashMap::new();

            // Process transactions and receipt actions from shards
            let (transactions, receipt_actions) = blk.shards.iter().fold(
                (Vec::new(), Vec::new()),
                |(mut all_transactions, mut all_actions), shard| {
                    collect_statuses(shard, &mut all_statuses);
                    if let Some(chunk) = &shard.chunk {
                        process_transactions(chunk, &timestamp, block_header, &mut all_transactions);
                        process_receipt_actions(chunk, &block_meta, &mut all_actions, &all_statuses);
                    }
                    (all_transactions, all_actions)
                }
            );

            (transactions, receipt_actions, Some(block_meta))
        }
    );

    BlockDataOutput {
        block: block_meta,
        transactions,
        receipt_actions,
    }
}

// Collect the status of each receipt execution outcome
fn collect_statuses(shard: &IndexerShard, all_statuses: &mut HashMap<String, String>) {
    shard.receipt_execution_outcomes.iter().filter_map(|outcome| {
        outcome.execution_outcome.as_ref()
    }).for_each(|outcome_with_id| {
        if let Some(status) = outcome_with_id.outcome.as_ref().and_then(|outcome| outcome.status.as_ref()) {
            let status_str = match status {
                Status::Failure(_) => "Failure",
                _ => "Success",
            };
            if let Some(id) = &outcome_with_id.id {
                all_statuses.insert(bs58_hash_to_string(Some(id.clone())), status_str.to_string());
            }
        }
    });
}

// Process transactions in a chunk
fn process_transactions(
    chunk: &IndexerChunk,
    timestamp: &BlockTimestamp,
    block_header: &BlockHeader,
    all_transactions: &mut Vec<TransactionMeta>
) {
    chunk.transactions.iter().filter_map(|tx_with_outcome| {
        tx_with_outcome.transaction.as_ref().and_then(|transaction| {
            if should_process_transaction(transaction) {
                tx_with_outcome.outcome.as_ref()?.execution_outcome.as_ref().and_then(|outcome_with_id| {
                    transform_transaction(timestamp, &block_header.height, transaction, &outcome_with_id.outcome)
                })
            } else {
                None
            }
        })
    }).for_each(|transaction| all_transactions.push(transaction));
}

// Process receipt actions in a chunk
fn process_receipt_actions(
    chunk: &IndexerChunk,
    block_meta: &BlockMeta,
    all_actions: &mut Vec<ReceiptActionMeta>,
    all_statuses: &HashMap<String, String>
) {
    let mut action_index = all_actions.len() as u64 + 1;

    chunk.receipts.iter().filter_map(|receipt| {
        receipt.receipt.as_ref().and_then(|receipt_action| match receipt_action {
            ReceiptTypes::Action(action_receipt) => {
                let actions = action_receipt.actions.iter().filter_map(|action| {
                    let transformed_action = transform_action(action, block_meta, receipt, all_statuses, action_index);
                    action_index += 1;
                    if should_process_action(&transformed_action) {
                        Some(transformed_action)
                    } else {
                        None
                    }
                }).collect::<Vec<_>>();
                if actions.is_empty() { None } else { Some(actions) }
            },
            _ => None,
        })
    }).flatten().for_each(|action| all_actions.push(action));
}

// Check if a transaction should be processed
fn should_process_transaction(transaction: &SignedTransaction) -> bool {
    FILTERED_RECEIVER_IDS.is_empty() || FILTERED_RECEIVER_IDS.contains(&transaction.receiver_id.to_string())
}

// Check if an action should be processed
fn should_process_action(action: &ReceiptActionMeta) -> bool {
    (FILTERED_RECEIVER_IDS.is_empty() || FILTERED_RECEIVER_IDS.contains(&action.receiver_id.to_string()))
        && (FILTERED_METHOD_NAMES.is_empty() || FILTERED_METHOD_NAMES.contains(&action.method_name.to_string()))
}

// Database updates

#[substreams::handlers::map]
fn db_out(block_data_output: BlockDataOutput) -> Result<DatabaseChanges, substreams::errors::Error> {
    let mut database_changes: DatabaseChanges = Default::default();

    if block_data_output.block.is_some() {
        // Save block
        push_block_create(&mut database_changes, &block_data_output.block.unwrap());

        // Save transactions
        for transaction in block_data_output.transactions {
            push_transaction_create(&mut database_changes, &transaction, 0);
        }

        // Save Actions
        for action in block_data_output.receipt_actions.iter() {
            push_action_create(&mut database_changes, &action);
        }
    } else {
        println!("No block data, skipping");
    }

    Ok(database_changes)
}

fn push_block_create(
    changes: &mut DatabaseChanges,
    block: &BlockMeta,
) {
    changes
        .push_change("blocks", &block.block_height.to_string(), 0, Operation::Create)
        .change("block_height", (None, block.block_height))
        .change("block_timestamp", (None, block.block_timestamp))
        .change("block_hash", (None, &block.block_hash))
        .change("author_account_id", (None, &block.author_account_id))
        .change("approvals", (None, block.approvals));
}

fn push_transaction_create(
    changes: &mut DatabaseChanges,
    transaction: &TransactionMeta,
    ordinal: u64,
) {
    changes
        .push_change("transactions", &transaction.tx_hash, ordinal, Operation::Create)
        .change("block_timestamp", (None, transaction.block_timestamp))
        .change("block_height", (None, transaction.block_height))
        .change("tx_hash", (None, &transaction.tx_hash))
        .change("signer_id", (None, &transaction.signer_id))
        .change("nonce", (None, transaction.nonce))
        .change("receipt_id", (None, &transaction.receipt_id))
        .change("receiver_id", (None, &transaction.receiver_id));
}

fn push_action_create(
    changes: &mut DatabaseChanges,
    action: &ReceiptActionMeta,
) {
    let pk = generate_hash_pk(action);

    changes
        .push_change("receipt_actions", &pk.to_string(), action.action_index, Operation::Create)
        .change("block_timestamp", (None, action.block_timestamp))
        .change("block_height", (None, action.block_height))
        .change("receipt_id", (None, &action.receipt_id))
        .change("action_index", (None, action.action_index))
        .change("predecessor_id", (None, &action.predecessor_id))
        .change("receiver_id", (None, &action.receiver_id))
        .change("action_kind", (None, &action.action_kind))
        .change("method_name", (None, &action.method_name))
        .change("args", (None, &action.args))
        .change("social_kind", (None, &action.social_kind))
        .change("status", (None, action.status.to_string()))
        .change("gas", (None, action.gas))
        .change("deposit", (None, action.deposit.to_string()))
        .change("stake", (None, action.stake.to_string()));
}
