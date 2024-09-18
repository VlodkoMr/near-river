use chrono::{DateTime, Utc};
use substreams_near::pb::sf::near::r#type::v1::BlockHeader;

#[derive(Debug, PartialEq)]
pub struct BlockTimestamp(DateTime<Utc>);

impl BlockTimestamp {

    pub fn from_block(block_header: &BlockHeader) -> Self {
        let timestamp = block_header.timestamp;

        BlockTimestamp(
            DateTime::<Utc>::from_timestamp_millis((timestamp / 1_000_000) as i64)
                .unwrap_or_else(|| panic!("invalid date for timestamp {}", timestamp)),
        )
    }

    pub fn timestamp(&self) -> u64 {
        self.0.timestamp() as u64
    }

}