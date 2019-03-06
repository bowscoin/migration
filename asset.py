#!/usr/bin/python
# -*- coding: utf-8 -*-

from stellar_base.keypair import Keypair
from stellar_base.asset import Asset
from stellar_base.builder import Builder

def generate_random_keypair():
    print 'Generate random keypair'
    keypair = Keypair.random()
    address = keypair.address().decode()
    if raw_input('Activation account address: {}'.format(address)) != 'n':
        issue_asset(keypair)


def issue_asset(keypair):
    print 'Generate asset'
    issuing_secret = keypair.seed().decode()
    issuing_public = keypair.address().decode()

    my_asset = Asset(raw_input('Name asset: '), issuing_public)

    #create trust
    receiving_secret = raw_input('Secret trusting address: ')
    network = raw_input('TESTNET/PUBLIC: ')
    builder = Builder(receiving_secret, network=network).append_trust_op(destination=my_asset.issuer, code=my_asset.code)
    builder.sign()
    resp = builder.submit()
    print(resp)

    #set_flag AUTH_REQUIRED = 0x1, AUTH_REVOCABLE = 0x2, AUTH_IMMUTABLE = 0x4 (https://www.stellar.org/developers/guides/concepts/accounts.html#flags)
    flag = 0x4
    if flag != 0:
        builder = Builder(issuing_secret, network=network).append_set_options_op(set_flags=flag, source=my_asset)
        builder.sign()
        resp = builder.submit()
        print(resp)

    #send asset
    receiving_public = Keypair.from_seed(receiving_secret).address().decode()
    amount = raw_input('Amount: ')
    builder = Builder(issuing_secret, network=network).append_payment_op(destination=receiving_public, amount=amount, asset_code=my_asset.code, asset_issuer=my_asset.issuer)
    builder.sign()
    resp = builder.submit()
    print(resp)

if __name__ == "__main__":
    generate_random_keypair()
