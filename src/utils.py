from web3 import Web3


class Utils:
    def __init__(self, infura_key: str):
        self.infura_url = f'https://mainnet.infura.io/v3/{infura_key}'
        self.web3 = Web3(Web3.HTTPProvider(self.infura_url))
        self.check_connection()

    def check_connection(self) -> None:
        if not self.web3.is_connected():
            raise Exception("Failed to connect to Ethereum network")

    def get_logs(self, address: str, start_block: int, end_block: int, batch_size: int = 1000) -> list:
        logs = []
        current_start_block = start_block

        approval_event_signature = self.web3.keccak(text="Approval(address,address,uint256)").hex()
        address = address.replace('0x', '0x000000000000000000000000')
        while current_start_block <= end_block:
            current_end_block = min(current_start_block + batch_size - 1, end_block)

            try:
                # Define the Approval event signature
                approval_filter = self.web3.eth.filter({
                    'fromBlock': current_start_block,
                    'toBlock': current_end_block,
                    'topics': [
                        approval_event_signature,
                        address
                    ]
                })

                batch_logs = approval_filter.get_all_entries()
                print(f"Fetched {len(batch_logs)} logs from blocks {current_start_block} to {current_end_block}")
                logs.extend(batch_logs)

            except ValueError as e:
                print(f"Error fetching logs from blocks {current_start_block} to {current_end_block}: {e}")

            current_start_block = current_end_block + 1

        return logs

    def get_approval_logs(self, address: str, start_block: int = None, end_block: int = None):
        if not start_block:
            start_block = end_block = self.web3.eth.block_number

        logs = self.get_logs(address, start_block, end_block)
        return logs
