import datetime
import json
import os
import hashlib
from pickle import TRUE


# main.py

class Block:
    
    def __init__(self, previous_block_hash, transaction_list):

        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = f"{previous_block_hash} - "
        for i in range(len(transaction_list)):
            self.block_data = self.block_data + transaction_list[i].transaction + " - "

        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        self.block_hash = hashlib.sha256(block_string.encode()).hexdigest()
        return self.block_hash
    


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.generate_genesis_block()

    def generate_genesis_block(self):
        self.chain.append(Block("0", [Transaction('Genesis Block')]))
    
    def create_block_from_transaction(self, transaction_list):
        previous_block_hash = self.last_block.block_hash
        block  = Block(previous_block_hash, transaction_list)
        self.chain.append(block)
        print("Nouveau block créé")

    ##Valider la bloc chain
    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash


    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            print(f"Hash {i + 1}: {self.chain[i].block_hash}\n")
    

    ##Check la transaction
    def Check(self, transaction_id):
        condition = False
        for block in self.chain:
            for transaction in block.transaction_list:
                if transaction.transaction_id == transaction_id:
                    print("transaction validated:" + transaction.transaction)
                    condition = TRUE

        if condition == False : 
            print("no transaction with this id")

    ##Afficher les 10 dernières transactions
    def Show(self):
        for transaction in self.last_block.transaction_list:
            print(transaction.transaction)

    ##Altérer un bloc
    def Tamper(self, transaction_id):
        condition = False
        for block in self.chain:
            for transaction in block.transaction_list:
                if transaction.transaction_id == transaction_id:
                    print("transaction validated:" + transaction.transaction)
                    print("tamper the transaction : ")
                    input_user = input()
                    transaction.transaction = input_user
                    condition = TRUE

        if condition == False : 
            print("no transaction with this id")

    ##Ajouter une nouvelle transaction
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)
        if len(self.unconfirmed_transactions) == 5:
            self.create_block_from_transaction(self.unconfirmed_transactions)
            self.unconfirmed_transactions = []



    @property
    def last_block(self):
        return self.chain[-1]

class Transaction:

    def __init__(self, transaction):

        self.transaction = transaction
        self.transaction_date = f"{datetime.datetime.now().date()} {datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}"
        self.transaction_id = hashlib.sha256(self.transaction.encode()).hexdigest()
    
    def get_transaction_name(self):
        return self.transaction

    def get_transaction_id(self):
        return self.transaction_id

    def get_transaction_id(self):
        return self.transaction_date
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)




t1 = f"George sends 3.1 coin(s) to Joe"
t1_obj = Transaction(t1)
t2 = f"Joe sends 2.5 coin(s) to Adam"
t2_obj = Transaction(t2)
t3 = f"Adam sends 1.2 coin(s) to Bob"
t3_obj = Transaction(t3)
t4 = f"Bob sends 0.5 coin(s) to Charlie"
t4_obj = Transaction(t4)
t5 = f"Charlie sends 0.2 coin(s) to David"
t5_obj = Transaction(t5)
t6 = f"David sends 0.1 coin(s) to Eric"
t6_obj = Transaction(t6)

print("zeegheroihg: " + t6_obj.toJSON())



myblockchain = Blockchain()
myblockchain.add_new_transaction(t1_obj)
myblockchain.add_new_transaction(t2_obj)
myblockchain.add_new_transaction(t3_obj)
myblockchain.add_new_transaction(t4_obj)
myblockchain.add_new_transaction(t5_obj)



print("----------------id :" + t5_obj.transaction_id+"\n")
myblockchain.Check(t5_obj.transaction_id)

print("Show function")
myblockchain.Show()


#print("Tamper function")
#myblockchain.Tamper(t5_obj.transaction_id)




myblockchain.display_chain()