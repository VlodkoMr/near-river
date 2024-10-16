use std::collections::HashMap;
use substreams_near::pb::sf::near::r#type::v1::{Action, ExecutionOutcome, Receipt, SignedTransaction};
use crate::pb::near::custom::v1::{TransactionMeta, BlockMeta, ReceiptActionMeta};
use substreams_near::pb::sf::near::r#type::v1::action::Action as ActionTypes;
use crate::utils::block_timestamp::BlockTimestamp;
use crate::utils::helpers::{bs58_hash_to_string, bytes_to_near_amount, extract_function_call_args, extract_social_kind};

pub fn transform_action(
    action: &Action,
    block: &BlockMeta,
    receipt: &Receipt,
    all_statuses: &HashMap<String, String>,
    action_index: u64,
    receipt_to_tx_map: &HashMap<String, String>,
) -> ReceiptActionMeta {
    let receipt_id_hash = bs58_hash_to_string(receipt.receipt_id.clone());

    let action_kind = match &action.action {
        Some(ActionTypes::FunctionCall(_)) => "FunctionCall",
        Some(ActionTypes::Transfer(_)) => "Transfer",
        Some(ActionTypes::Stake(_)) => "Stake",
        Some(ActionTypes::CreateAccount(_)) => "CreateAccount",
        Some(ActionTypes::DeployContract(_)) => "DeployContract",
        Some(ActionTypes::AddKey(_)) => "AddKey",
        Some(ActionTypes::DeleteKey(_)) => "DeleteKey",
        Some(ActionTypes::DeleteAccount(_)) => "DeleteAccount",
        Some(ActionTypes::Delegate(_)) => "Delegate",
        None => "Unknown",
    };

    let status = all_statuses.get(&receipt_id_hash).cloned().unwrap_or_else(|| "".to_string());

    let method_name = match &action.action {
        Some(ActionTypes::FunctionCall(function_call)) => function_call.method_name.clone(),
        _ => "".to_string(),
    };

    let args = match &action.action {
        Some(ActionTypes::FunctionCall(function_call)) => extract_function_call_args(&function_call.args),
        _ => "".to_string(),
    };

    let social_kind = match &action.action {
        Some(ActionTypes::FunctionCall(function_call)) => extract_social_kind(&method_name, &function_call.args),
        _ => "".to_string(),
    };

    let gas: u32 = match &action.action {
        Some(ActionTypes::FunctionCall(function_call)) => {
            function_call.gas.checked_div(1_000_000_000_000).unwrap_or(0) as u32
        }
        _ => 0,
    };

    let deposit: f64 = match &action.action {
        Some(ActionTypes::FunctionCall(function_call)) => bytes_to_near_amount(function_call.clone().deposit.unwrap().bytes),
        Some(ActionTypes::Transfer(transfer)) => bytes_to_near_amount(transfer.clone().deposit.unwrap().bytes),
        _ => 0.0,
    };

    let stake: f64 = match &action.action {
        Some(ActionTypes::Stake(stake)) => bytes_to_near_amount(stake.stake.clone().unwrap().bytes),
        _ => 0.0,
    };

    let tx_hash = receipt_to_tx_map.get(&receipt_id_hash)
        .cloned()
        .or_else(|| Some(bs58_hash_to_string(receipt.receipt_id.clone())))
        .unwrap_or_else(|| "".to_string());

    ReceiptActionMeta {
        block_timestamp: block.block_timestamp,
        block_height: block.block_height,
        receipt_id: receipt_id_hash,
        predecessor_id: receipt.predecessor_id.clone(),
        receiver_id: receipt.receiver_id.clone(),
        action_kind: action_kind.to_string(),
        action_index,
        method_name,
        args,
        social_kind,
        gas,
        deposit,
        stake,
        status,
        tx_hash,
    }
}

pub fn transform_transaction(
    blk_timestamp: &BlockTimestamp,
    height: &u64,
    transaction: &SignedTransaction,
    outcome: &Option<ExecutionOutcome>,
) -> Option<TransactionMeta> {
    let tx_hash = bs58_hash_to_string(transaction.hash.clone());

    let receipts: Vec<String> = if let Some(execution_outcome) = outcome {
        execution_outcome.receipt_ids.iter().map(|receipt_id| {
            bs58_hash_to_string(Some(receipt_id.clone()))
        }).collect()
    } else {
        vec![]
    };

    Some(TransactionMeta {
        block_timestamp: blk_timestamp.timestamp(),
        block_height: *height,
        tx_hash,
        receipt_id: receipts.join(","),
        signer_id: transaction.signer_id.to_string(),
        nonce: transaction.nonce,
        receiver_id: transaction.receiver_id.to_string(),
    })
}


