from brownie import accounts, network, config, MockV3Aggregator


FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
# If you close ganache-local deployment, delete the 1337 folder and map.json 1337 element before restarting
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
# The number of decimals depends of the price feed format
DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
        # Arr[-1] gives the last/latest item
    print("Mocks Deployed!")
