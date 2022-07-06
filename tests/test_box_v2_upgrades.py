from brownie import Box, TransparentUpgradeableProxy, ProxyAdmin, Contract, BoxV2, exceptions
from scripts.helpful_scripts import get_account, encode_function_data, upgrade
import pytest 

def test_proxy_upgrades():
    account = get_account()
    box = Box.deploy({"from": account}, publish_source=True)
    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(box.address, proxy_admin.address, box_encoded_initializer_function, {"from": account, "gas_limit": 1000000}, publish_source=True)
    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})

    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1