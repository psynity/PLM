from web3 import Web3

# L2 RPC 연결 (예: Alchemy, Infura)
w3 = Web3(Web3.HTTPProvider('https://arb-sepolia.g.alchemy.com/v2/your_key'))
contract = w3.eth.contract(address='VAULT_CONTRACT_ADDRESS', abi=CONTRACT_ABI)

def anchor_to_blockchain(researcher_address, node_hash, project_id, ktii_score):
    # 트랜잭션 구성 및 서명 (개인키 보안 주의)
    txn = contract.functions.anchorKnowledge(
        node_hash, project_id, ktii_score, b'' # ZKP 생략 시 빈 바이트
    ).build_transaction({
        'from': researcher_address,
        'nonce': w3.eth.get_transaction_count(researcher_address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    # 서명 및 전송 로직...
