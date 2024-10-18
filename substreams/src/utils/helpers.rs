use serde_json::{Value, json};
use std::string::String;
use xxhash_rust::xxh3::Xxh3;
use substreams_near::pb::sf::near::r#type::v1::CryptoHash;
use crate::pb::near::custom::v1::ReceiptActionMeta;

pub fn bytes_to_near_amount(bytes: Vec<u8>) -> f64 {
    let bytes_array: [u8; 16] = bytes.try_into().expect("slice with incorrect length");
    let yocto_near = u128::from_be_bytes(bytes_array);
    yocto_near as f64 / 1e24
}

pub fn bs58_hash_to_string(hash: Option<CryptoHash>) -> String {
    match hash {
        Some(h) => bs58::encode(h.bytes).into_string(),
        None => "".to_string(),
    }
}

pub fn generate_hash_pk(action: &ReceiptActionMeta) -> u64 {
    let pk = format!("{}:{}:{}", action.block_height, action.action_index, action.receipt_id);
    let mut hash = Xxh3::new();
    hash.update(pk.as_bytes());
    hash.digest()
}

// Extracts the function call arguments from the action
pub fn extract_function_call_args(args: &Vec<u8>) -> Value {
    let args_str = match std::str::from_utf8(args) {
        Ok(str) => str,
        Err(_) => return json!(null), // Return null if it's not valid UTF-8
    };

    match serde_json::from_str(args_str) {
        Ok(json) => json,
        Err(_) => json!(args_str),
    }
}

pub fn extract_social_kind(method_name: &str, args: &[u8]) -> String {
    if method_name != "set" {
        return "".to_string();
    }

    let args_str = match std::str::from_utf8(args) {
        Ok(v) => v,
        Err(_) => return "".to_string(),
    };

    let v: Value = match serde_json::from_str(args_str) {
        Ok(val) => val,
        Err(_) => return "".to_string(),
    };

    let data = match v.get("data").and_then(|d| d.as_object()) {
        Some(data) => data,
        None => return "".to_string(),
    };

    let binding = "".to_string();
    let wallet_address = data.keys().next().unwrap_or(&binding);
    let user_data = data.get(wallet_address).unwrap_or(&Value::Null);

    determine_social_action_type(user_data)
}

fn determine_social_action_type(user_data: &Value) -> String {
    if let Some(post_data) = user_data.get("post") {
        if post_data.get("main").is_some() {
            return "Post".to_string();
        } else if post_data.get("comment").is_some() {
            return "Comment".to_string();
        }
    } else if user_data.get("index").and_then(|x| x.get("like")).is_some() {
        return "Like".to_string();
    } else if user_data.get("index").and_then(|x| x.get("repost")).is_some() {
        return "Repost".to_string();
    } else if user_data.get("profile").is_some() {
        return "Profile".to_string();
    } else if let Some(graph_data) = user_data.get("index").and_then(|x| x.get("graph")) {
        if graph_data.as_str().map_or(false, |s| s.contains("\"poke\"")) {
            return "Poke".to_string();
        }
    } else if user_data.get("graph").and_then(|x| x.get("follow")).is_some() {
        return if user_data.get("graph").and_then(|x| x.get("follow")).and_then(|f| f.as_object()).and_then(|o| o.values().next()).map_or(false, |v| v.is_string()) {
            "Follow"
        } else {
            "Unfollow"
        }.to_string();
    } else if user_data.get("widget").is_some() {
        return "Widget".to_string();
    } else if user_data.get("index").and_then(|x| x.get("notify")).is_some() {
        return "Notify".to_string();
    }

    "".to_string()
}
