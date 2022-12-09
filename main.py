from hashlib import sha256
from datetime import datetime
import json


# Définition d'un block et ses propriètes
class Block:
    # Constructeur d'un block
    def __init__(self, index, transactions, temps, hashPrecedent):
        self.index = index
        self.transactions = transactions
        self.temps = temps
        self.hashPrecedent = hashPrecedent
        self.nonce = 0

        
    # Hashage d'un bloc
    def HashBlock(self):
        string = json.dumps(self.__dict__,default=str) # on convertit le json en string exploitable
        return sha256(string.encode()).hexdigest()

    
class Blockchain: 
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
 
    def create_genesis_block(self):
        genesis_block = Block(0, [], datetime.now(), "0")
        
        genesis_block.hash = genesis_block.HashBlock()
        self.chain.append(genesis_block)
        print('Block {} ajouter à {}'.format(genesis_block.index, genesis_block.temps))
        print('Hash précédent: {}'.format(genesis_block.hashPrecedent))
        print('Hash actuel: {}\n'.format(genesis_block.hash))
    @property
    def last_block(self):
        return self.chain[-1]

    difficulty = 2

    def proof_of_work(self, block):
            block.nonce = 0
            computed_hash = block.HashBlock()
            while not computed_hash.startswith('0' * Blockchain.difficulty):
                block.nonce += 1
                computed_hash = block.HashBlock()
            return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.HashBlock()
        if previous_hash != block.hashPrecedent:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
            block_hash == block.hash())

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)


# function test pour afficher un block initial
def test():
    #blockchain=Block(index=0,temps=datetime.now(),data="Test", hashPrecedent="0")
    blockchain= Blockchain()
    newBlock = Block(blockchain.last_block.index + 1, [], datetime.now(), blockchain.last_block.HashBlock)
    proof=blockchain.proof_of_work(newBlock)
    blockchain.add_block(newBlock,proof)
    for i in range(len(blockchain.chain)):
        print(blockchain.chain[i].__dict__)


test()