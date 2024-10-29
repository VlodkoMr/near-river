# NEAR River smart-contract example

This smart-contract is a simple example of processing data from NEAR River. We log data and increments the number of times a notification has been set.

# Quickstart

1. Make sure you have installed [rust](https://rust.org/).
2. Install the [`NEAR CLI`](https://github.com/near/near-cli#setup)

### Build and Deploy the Contract

You can automatically compile and deploy the contract in the NEAR testnet by running:

```bash
./deploy.sh
```

Once finished, check the `neardev/dev-account` file to find the address in which the contract was deployed:

```bash
cat ./neardev/dev-account
```
