// @generated
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct BlockMeta {
    #[prost(uint64, tag="2")]
    pub block_height: u64,
    #[prost(uint64, tag="3")]
    pub block_timestamp: u64,
    #[prost(string, tag="4")]
    pub block_hash: ::prost::alloc::string::String,
    #[prost(string, tag="5")]
    pub author_account_id: ::prost::alloc::string::String,
    #[prost(uint64, tag="6")]
    pub approvals: u64,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TransactionMeta {
    #[prost(uint64, tag="1")]
    pub block_timestamp: u64,
    #[prost(uint64, tag="2")]
    pub block_height: u64,
    #[prost(string, tag="3")]
    pub tx_hash: ::prost::alloc::string::String,
    #[prost(string, tag="4")]
    pub signer_id: ::prost::alloc::string::String,
    #[prost(uint64, tag="5")]
    pub nonce: u64,
    #[prost(string, tag="6")]
    pub receiver_id: ::prost::alloc::string::String,
    #[prost(string, tag="8")]
    pub receipt_id: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ReceiptActionMeta {
    #[prost(uint64, tag="1")]
    pub block_timestamp: u64,
    #[prost(uint64, tag="2")]
    pub block_height: u64,
    #[prost(string, tag="3")]
    pub receipt_id: ::prost::alloc::string::String,
    #[prost(string, tag="4")]
    pub predecessor_id: ::prost::alloc::string::String,
    #[prost(string, tag="5")]
    pub receiver_id: ::prost::alloc::string::String,
    #[prost(string, tag="6")]
    pub action_kind: ::prost::alloc::string::String,
    #[prost(uint64, tag="7")]
    pub action_index: u64,
    #[prost(string, tag="8")]
    pub method_name: ::prost::alloc::string::String,
    #[prost(string, tag="9")]
    pub args: ::prost::alloc::string::String,
    #[prost(string, tag="10")]
    pub social_kind: ::prost::alloc::string::String,
    #[prost(uint32, tag="11")]
    pub gas: u32,
    #[prost(double, tag="12")]
    pub deposit: f64,
    #[prost(double, tag="13")]
    pub stake: f64,
    #[prost(string, tag="14")]
    pub status: ::prost::alloc::string::String,
    #[prost(string, tag="15")]
    pub tx_hash: ::prost::alloc::string::String,
}
/// General block data output
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct BlockDataOutput {
    #[prost(message, optional, tag="1")]
    pub block: ::core::option::Option<BlockMeta>,
    #[prost(message, repeated, tag="2")]
    pub transactions: ::prost::alloc::vec::Vec<TransactionMeta>,
    #[prost(message, repeated, tag="3")]
    pub receipt_actions: ::prost::alloc::vec::Vec<ReceiptActionMeta>,
}
// @@protoc_insertion_point(module)
