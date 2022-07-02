import pytest
from brownie import network, accounts, exceptions
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me

# To create a mainnet for using brownie:
# brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.g.alchemy.com/v2/XR71RJjHXO12jAVZnUEYGG1QAD0UOFGv accounts=10 mnemonic=brownie port=8545

# WHERE SHOULD I RUN MY TESTS?
# 1) Brownie Ganache Chain with Mocks: ALWAYS
# 2) Testnet: ALWAYS (but only for integration testing)
# 3) Brownie mainnet-fork: OPTIONAL
# 4) Custom mainnet-fork: OPTIONAL
# 5) Self/Local Ganache: NOT NECESSARY, but good for tinkering


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    transaction = fund_me.fund({"from": account, "value": entrance_fee})
    transaction.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    withdrawal = fund_me.withdraw({"from": account})
    withdrawal.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
