#Imports des librairies
from hashlib import sha256  # lib essentiel pour la cryptologie des blocks
from datetime import datetime   # fonction pour dater nos création de blocks
import json #utile pour manipuler nos objects en structure json vers des strings
import random

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

# Définition de la blockchaine
class Blockchain: 
    #Constructeur d'une blockchaine
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block() 
    
    # fonction de création du block initial
    def create_genesis_block(self):
        genesis_block = Block(0, [], datetime.now(), "0") # appel du constructeur block avec 0 en hash précédent
        self.proof_of_work(genesis_block)   #On effectue la PoW sur notre premier bloc
        genesis_block.hash = genesis_block.HashBlock()
        self.chain.append(genesis_block)    #On le rajoute à la liste chaine
    @property
    def last_block(self):   #propriété pour connaitre facilement le dernier block de notre chaine
        return self.chain[-1]

    difficulty = 2 # difficulté de la PoW

    #Fonction de la PoW
    def proof_of_work(self, block):
            block.nonce = 0     #On force le nonce à 0 par précaution, surement pas nécessaire (!)
            computed_hash = block.HashBlock()
            while not computed_hash.startswith('0' * Blockchain.difficulty): #on vérifie la PoW, si invalide, on incrémente nonce
                block.nonce += 1
                computed_hash = block.HashBlock()
            return computed_hash

    #Fonction pour ajouter un block en vérifiant son PoW
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.hashPrecedent:    #Pour éviter les doublons (cas très rare)            
            return False
        if not self.is_valid_proof(block, proof):   #Vérification de la PoW
            return False
        block.hash = proof
        self.chain.append(block) #Ajout à la chaine

        return True

    #Fonction pour verifier la PoW
    def is_valid_proof(self, block, block_hash): 
        return (block_hash.startswith('0' * Blockchain.difficulty) and #Vérifie la difficulté respecté
            block_hash == block.HashBlock())    #Vérifie la PoW est bien le HashBlock

    #Fonction d'ajout des transactions
    def add(self, transaction):
        self.unconfirmed_transactions.append(transaction)
        self.last_block.transactions.append(transaction)
        self.proof_of_work(self.last_block)
        if len(self.last_block.transactions) == 10:
            newBlock = Block(self.last_block.index + 1, [], datetime.now(), self.last_block.hash)
            proof=self.proof_of_work(newBlock)
            self.add_block(newBlock,proof)


    def afficher(self):
        for i in range(len(self.chain)):
            print('Block {} ajouter à {}'.format(self.chain[i].index, self.chain[i].temps))
            print('Hash précédent: {}'.format(self.chain[i].hashPrecedent))
            print('Contient {} transactions'.format(len(self.chain[i].transactions)))
            print('Hash actuel: {}\n'.format(self.chain[i].hash))



# Définition de la classe transaction
class Transaction:

    def __init__(self, transaction):
        self.transaction = transaction
        self.transaction_date = datetime.now()  # on la date
        self.transaction_id = sha256(self.transaction.encode()).hexdigest() # on la hash
    


def testTransac():
    myblockchain = Blockchain()
    for i in range(40):
        transac ='George envoie {} à Joe'.format(random.uniform(0.1, 75.5))
        objet = Transaction(transac)
        myblockchain.add(objet)
    for i in range(40): 
        print('{} à {}'.format(myblockchain.unconfirmed_transactions[i].transaction, myblockchain.unconfirmed_transactions[i].transaction_date))
        print('ID de transaction: {}\n'.format(myblockchain.unconfirmed_transactions[i].transaction_id))


# Fonction test pour afficher un block initial
def testBlockchain():
    blockchain= Blockchain()
    newBlock = Block(blockchain.last_block.index + 1, [], datetime.now(), blockchain.last_block.hash)
    proof=blockchain.proof_of_work(newBlock)
    blockchain.add_block(newBlock,proof)
    transac ='George envoie {} à Joe'.format(random.uniform(0.1, 75.5))
    objet = Transaction(transac)
    blockchain.add(objet)
    for i in range(5):
        newBlock = Block(blockchain.last_block.index + 1, [], datetime.now(), blockchain.last_block.hash)
        proof=blockchain.proof_of_work(newBlock)
        blockchain.add_block(newBlock,proof)
        print(blockchain.chain[i].__dict__)
    blockchain.afficher()

# Fonction test pour la condition "Toutes les dix transactions un nouveau bloc est créé"
def testCondition():
    myblockchain = Blockchain() # on crée une blockchaine
    for i in range(41): # on crée pleins de transactions aléatoires
        transac ='George envoie {} à Joe'.format(random.uniform(0.1, 75.5))
        objet = Transaction(transac)
        myblockchain.add(objet)
    for i in range(41): # on les affiche
        print('{} à {}'.format(myblockchain.unconfirmed_transactions[i].transaction, myblockchain.unconfirmed_transactions[i].transaction_date))
        print('ID de transaction: {}\n'.format(myblockchain.unconfirmed_transactions[i].transaction_id))
    
    myblockchain.afficher() # on affiche notre blockchaine pour vérifier les blocks crée

testCondition()