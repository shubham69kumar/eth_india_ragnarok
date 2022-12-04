from brownie import FundMe, accounts, network, MockV3Aggregator
from distutils.command.config import config
from web3 import Web3

LOCAL_BLOCKCHAIN_ENV = ["deployment", "ganache-local"]


def deploy_fund_me():
    account = accounts.add(config["wallets"]["from_key"])

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
    )
    print(fund_me)


def deploy_mocks():
    print(f"the current active network is {network.show_active()}")
    print("deploying MockV3Aggregator")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(18, Web3.toWei(2000, "ether"), {"from": get_account()})
    print("mock deployed")


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        return accounts[0]
    else:
        return accounts.load("myweb3")


def main():
    deploy_fund_me()
