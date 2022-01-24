from conftest import *
from brownie import exceptions


def test_set_price_feed_contract(account, non_owner, farm_and_token):
    # Arrange
    skip_if_not_local_env()
    token_farm, dapp_token = get_farm_and_token(farm_and_token)
    # Act
    price_feed_address = get_contract("eth_usd_price_feed")
    token_farm.setPriceFeedContract(
        dapp_token.address, price_feed_address, {"from": account}
    )
    # Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(
            dapp_token.address, price_feed_address, {"from": non_owner}
        )


def test_stake_tokens(account, farm_and_token, amount_staked):
    # Arrange
    skip_if_not_local_env()
    token_farm, dapp_token = get_farm_and_token(farm_and_token)
    # Act
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})
    # Assert
    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    return token_farm, dapp_token


def test_issue_tokens(account, farm_and_token, amount_staked):
    # Arrange
    skip_if_not_local_env()
    token_farm, dapp_token = test_stake_tokens(account, farm_and_token, amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)
    # Act
    token_farm.issueTokens({"from": account})
    # Arrange
    # mocked price of price feeds is 2000 for both 1 DAI and 1 ETH
    assert (
        dapp_token.balanceOf(account.address)
        == starting_balance + INITIAL_PRICE_FEED_VALUE
    )
