use std::env;
use dotenv::dotenv;
use once_cell::sync::Lazy;

static INIT: Lazy<()> = Lazy::new(|| {
    dotenv().ok();
});

// Helper function to get environment variables with a default
fn get_env_var(key: &str, default: &str) -> String {
    Lazy::force(&INIT);
    env::var(key).unwrap_or_else(|_| default.to_string())
}

// Convert comma-separated environment variable to a Vec<String>
fn get_env_array(key: &str, default: &str) -> Vec<String> {
    get_env_var(key, default)
        .split(',')
        .filter(|s| !s.is_empty())
        .map(String::from)
        .collect()
}

// Lazy static variables
pub static FILTERED_RECEIVER_IDS: Lazy<Vec<String>> = Lazy::new(|| get_env_array("FILTERED_RECEIVER_IDS", ""));
pub static FILTERED_METHOD_NAMES: Lazy<Vec<String>> = Lazy::new(|| get_env_array("FILTERED_METHOD_NAMES", ""));

pub static MAX_ARGS_LENGTH: Lazy<usize> = Lazy::new(|| {
    get_env_var("MAX_ARGS_LENGTH", "100000").parse().expect("Invalid MAX_ARGS_LENGTH")
});