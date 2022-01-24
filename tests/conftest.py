from scripts.helpful_scripts import *
from scripts.deploy import deploy_token_farm_and_dapp_token
from web3 import Web3
import pytest


@pytest.fixture
def amount_staked():
    return Web3.toWei(1, "ether")


@pytest.fixture
def account():
    return get_account()


@pytest.fixture
def non_owner():
    return get_account(index=1)


@pytest.fixture
def farm_and_token():
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    return (token_farm, dapp_token)


def get_farm_and_token(farm_and_token):
    return farm_and_token[0], farm_and_token[1]


def skip_if_not_local_env():
    if not is_local_env():
        pytest.skip("Only for local testing")


def skip_if_local_env():
    if is_local_env():
        pytest.skip("Only for integration testing")


def is_local_env():
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
