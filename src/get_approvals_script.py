import click

from utils import Utils

INFURA_KEY = 'f7db56ffa69c44acab30f3bd83252d8e'
DECIMALS = 18


@click.command()
@click.option('--address', required=True, help='Ethereum address to retrieve data for.')
@click.option('--start-block', required=False, type=int, help='Start block number.')
@click.option('--end-block', required=False, type=int, help='End block number.')
def run(address, start_block, end_block):
    utils = Utils(INFURA_KEY)
    click.echo(f"Retrieving data for address: {address}")
    if start_block or end_block:
        if not start_block:
            raise Exception('Start block was not given, you must enter a start block and an end block')
        elif not end_block:
            raise Exception('end block was not given,  you must enter a start block and an end block')
        else:
            click.echo(f"From block {start_block} to block {end_block}")
    else:
        start_block = end_block = utils.web3.eth.block_number

    logs = utils.get_approval_logs(address, start_block, end_block)
    for log in logs:
        spender = utils.web3.to_checksum_address(log['topics'][2].hex()[-40:])
        # value = int.from_bytes(log['data'], byteorder='big')
        value_hex = log["data"].hex()
        value_decimal = str(int(value_hex, 16)).zfill(2 * DECIMALS)
        value_decimal = value_decimal[:-DECIMALS] + '.' + value_decimal[-DECIMALS:]
        click.echo(f"Approval on {spender} on amount of {value_decimal}")


if __name__ == '__main__':
    run()


#  python get_approvals_script.py --address=0xcd90574bc2ef39bcebbc5561c1c9d8e42110c239 --start-block=20505574 --end-block=20509574
