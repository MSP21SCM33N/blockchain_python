
from flask import Flask, jsonify, request, send_from_directory #lets us setup a flask application and API endpoints; jsonify takes data and turns it into json
from flask_cors import CORS # only clients running on the server can use the server 
from blockchain import Blockchain
from wallet import Wallet

app = Flask(__name__)
 # we pass public key because it is acting as the hosting node performing a request
CORS(app)

@app.route('/', methods=['GET']) # Decorator is our endpoint
def get_node_ui():
    return send_from_directory('ui', 'node.html')

@app.route('/network', methods=['GET']) # Decorator is our endpoint
def get_network_ui():
    return send_from_directory('ui', 'network.html')

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.balance()
    if balance != None:
        response = {
            'message': 'Fetched balance successfully', 
            'funds': balance
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Loading balance failed', 
            'wallet_set_up': wallet.public_key != None,
        }
        return jsonify(response), 500

@app.route('/transaction', methods=['GET'])
def get_open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200

@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    if 'block' not in values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {'message': 'Block added'}
            return jsonify(response), 201
        else:
            response = {'message': 'Block seems invalid'}
            return jsonify(response), 409 # 409 error represents conflict
    elif block['index'] > blockchain.chain[-1].index:
        response = {
            'message': 'Blockchain seems to differ from local blockchain. Block not added!'
        }
        blockchain.resolve_conflicts = True
        return jsonify(response), 200
    else:
        response = {
            'message': 'Blockchain seems to be shorter. Block not added!'
        }
        return jsonify(response), 409


@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(key in values for key in required): # checks if the required keys are in our values
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    success = blockchain.add_transaction(values['sender'], values['recipient'], values['signature'], values['amount'],  is_receiving=True)
    if success:
        response = {
            'message': 'Successfully added transaction.',
            'transaction': {
                'sender': values['sender'],
                'recipient': values['recipient'],
                'amount': values['amount'],
                'signature': values['signature']
            },
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction failed.'
        }
        return jsonify(response), 500



@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'message': 'No data found',
        }
        return jsonify(response), 400 
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing.'
        }
        return jsonify(response), 400
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(wallet.public_key,recipient,signature,amount)
    if success:
        response = {
            'message': 'Successfully added transaction.',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction failed.'
        }
        return jsonify(response), 500

@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key,port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Saving the keys failed'
        }
        return jsonify(response), 500

@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Loading the keys failed'
        }
        return jsonify(response), 500


@app.route('/mine', methods=['POST']) #Decorator is our endpoint
def mine():
    if blockchain.resolve_conflicts == True:
        response = {'message': 'Resolve conflicts first. Block not added!'}
        return jsonify(response), 409
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Block added successfully',
            'block': dict_block,
            'funds': blockchain.balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a block failed',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500 

@app.route('/resolve-conflicts', methods=['POST'])
def resolve_conflicts(): #this function checks and sees if we replaced our local blockchain
    replaced = blockchain.resolve()
    if replaced:
        response = {'message': 'Chain was replaced.'}
    else:
        response = {'message': 'Local chain was kept!'}
    return jsonify(response), 200


@app.route('/chain', methods=['GET']) # Decorator is our endpoint
def get_chain(): # return data about our blockchain to the user that requested it
    snapshot_chain = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in snapshot_chain]
    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dict_chain), 200

@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json() #get_json() returns a dictionary with values requested
    if not values:
        response = {
            'message': 'No data attached! '
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
            'message': 'No node data found! '
        }
        return jsonify(response), 400

    node = values['node']
    blockchain.add_peer_node(node)
    response = {
        'message': 'Node added successfully! ', 
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201

@app.route('/node/<node_url>', methods=['DELETE']) #node url is the location where we are executing the delete command
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'message': 'No node found!'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Node successfully removed',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200

@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        'all_nodes': nodes
    }
    return jsonify(response), 200



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0', port=port)

