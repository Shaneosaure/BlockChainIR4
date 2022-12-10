#Imports des librairies
from hashlib import sha256  # lib essentiel pour la cryptologie des blocks
from datetime import datetime   # fonction pour dater nos création de blocks
import json #utile pour manipuler nos objects en structure json vers des strings
import random
import time
from Crypto.PublicKey import RSA
import os


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
        # on ajoute la transaction à la liste de la blockchaine et au block
        self.unconfirmed_transactions.append(transaction)
        self.last_block.transactions.append(transaction)
        self.proof_of_work(self.last_block) # on revalide la PoW du block
        if len(self.last_block.transactions) == 10: #condition pour créer un block au bout de 10 transactions
            newBlock = Block(self.last_block.index + 1, [], datetime.now(), self.last_block.hash)
            proof=self.proof_of_work(newBlock)
            self.add_block(newBlock,proof)

    # Fonction pour afficher la blockchaine: les caractéristiques des blocks...
    def afficher(self):
        for i in range(len(self.chain)):
            print('Block {} ajouté à {}'.format(self.chain[i].index, self.chain[i].temps))
            print('Hash précédent: {}'.format(self.chain[i].hashPrecedent))
            print('Contient {} transactions'.format(len(self.chain[i].transactions)))
            print('Hash actuel: {}\n'.format(self.chain[i].hash))

    # Fonction pour vérifier la bonne signature d'un block
    def check(self, transaction_id, key):
        for i in range(len(self.unconfirmed_transactions)): # on cherche la transaction dans l'historique de la blockchaine
            if transaction_id == self.unconfirmed_transactions[i].transaction_id : # on vérifie si trouvé
                # on recalcule le hash de la transaction qu'on vérifie avec la signature
                if  pow(self.unconfirmed_transactions[i].signature, key.e, key.n) ==  int.from_bytes(sha256(self.unconfirmed_transactions[i].transaction.encode()).digest(),byteorder='big'):
                    print("Transaction ",transaction_id, "validée !")   
                    return True # on casse la fonction pour arreter les loops
                else:
                    print("Transaction ",transaction_id," corrompue")
                    return False # on casse la fonction pour arreter les loops
        print("La transaction ",transaction_id,"  n'existe pas") # cas où aucunes transaction est trouvée

    # Fonction pour altérer une transaction en changeant l'intitulé
    def tamper(self, transaction_id): 
        for i in range(len(self.unconfirmed_transactions)):
            if transaction_id == self.unconfirmed_transactions[i].transaction_id :
                self.unconfirmed_transactions[i].transaction="Alice envoie 5000 pièces à Eve"
                

    def show(self):
        for i in range(1, 11):
            transaction = self.unconfirmed_transactions[len(self.unconfirmed_transactions)-i]
            print('{} à {}'.format(transaction.transaction, transaction.transaction_date))
            print('ID de transaction: {}\n'.format(transaction.signature))

# Définition de la classe transaction
class Transaction:

    def __init__(self, transaction, key):
        self.transaction = transaction
        self.transaction_date = datetime.now()
        self.transaction_id= int.from_bytes(sha256(self.transaction.encode()).digest(),byteorder='big') #on hash
        self.signature = pow(self.transaction_id, key.d, key.n) # on la signe
    

def attendre():
    for i in range(15):
        time.sleep(0.3)
        print(".", sep=' ', end='', flush=True)

# Fonction test pour la classe transaction
def testTransac():
    myblockchain = Blockchain()
    for i in range(40):
        transac ='George envoie {} à Joe'.format(random.uniform(0.1, 75.5))
        objet = Transaction(transac)
        myblockchain.add(objet)
    for i in range(40): 
        print('{} à {}'.format(myblockchain.unconfirmed_transactions[i].transaction, myblockchain.unconfirmed_transactions[i].transaction_date))
        print('ID de transaction: {}\n'.format(myblockchain.unconfirmed_transactions[i].signature))


# Fonction test pour la classe blockchaine
def testBlockchain():
    while True:
        os.system('clear')
        os.system('cls')
        print("--------------------------------------------------------------------")
        #On initialise notre blockchaine
        blockchain= Blockchain()
        
        #On génère une pair de clé pour Alice
        print("Créons des cléfs pour une Alice:")
        keyPairAlice = RSA.generate(bits=1024)
        print("Cléfs d'Alice:")
        print(f"Public key:  (n={hex(keyPairAlice.n)}, e={hex(keyPairAlice.e)})\n")
        print(f"Private key: (n={hex(keyPairAlice.n)}, d={hex(keyPairAlice.d)})\n")
        print("--------------------------------------------------------------------\n")

        attendre()

        transac ='Alice envoie {} à Bob'.format(random.uniform(0.1, 75.5))
        objet = Transaction(transac,keyPairAlice)
        blockchain.add(objet)
        newBlock = Block(blockchain.last_block.index + 1, [], datetime.now(), blockchain.last_block.hash)
        proof=blockchain.proof_of_work(newBlock)
        blockchain.add_block(newBlock,proof)
        for i in range(5):
            newBlock = Block(blockchain.last_block.index + 1, [], datetime.now(), blockchain.last_block.hash)
            proof=blockchain.proof_of_work(newBlock)
            blockchain.add_block(newBlock,proof)
        print("\n--------------------------------------------------------------------\n")

        print(
            " 1. Affiche le block initial\n",
            "2. Afficher toute la blockchaine\n",
            "3. Retourner au menu précédent\n",
        )
        choix = input("Veuillez choisir parmis les options:")
        if choix =="1":
            os.system('clear')
            os.system('cls')
            print("--------------------------------------------------------------------\n")
            print('Block {} ajouté à {}'.format(blockchain.chain[0].index, blockchain.chain[0].temps))
            print('Hash précédent: {}'.format(blockchain.chain[0].hashPrecedent))
            print('Contient {} transactions'.format(len(blockchain.chain[0].transactions)))
            print('Hash actuel: {}\n'.format(blockchain.chain[0].hash))
            print('Valeur du nonce: {}\n'.format(blockchain.chain[0].nonce))
            attendre()
            attendre()
        elif choix == "2":
            blockchain.afficher()
            attendre()
            attendre()
        elif choix == "3":  
            break          
        else:
            print("Veuillez mettre un choix correct")
   

# Fonction test pour la condition "Toutes les dix transactions un nouveau bloc est créé"
def testCondition():
    os.system('clear')
    myblockchain = Blockchain() # on crée une blockchaine
    for i in range(41): # on crée pleins de transactions aléatoires
        transac ='George envoie {} à Joe'.format(random.uniform(0.1, 75.5))
        objet = Transaction(transac)
        myblockchain.add(objet)
    for i in range(41): # on les affiche
        print('{} à {}'.format(myblockchain.unconfirmed_transactions[i].transaction, myblockchain.unconfirmed_transactions[i].transaction_date))
        print('ID de transaction: {}\n'.format(myblockchain.unconfirmed_transactions[i].signature))
    
    myblockchain.afficher() # on affiche notre blockchaine pour vérifier les blocks crée



def testTransactions():
    #On génère une pair de clé pour Alice
    keyPairAlice = RSA.generate(bits=1024)
    print("Cléfs d'Alice:")
    print(f"Public key:  (n={hex(keyPairAlice.n)}, e={hex(keyPairAlice.e)})")
    print(f"Private key: (n={hex(keyPairAlice.n)}, d={hex(keyPairAlice.d)})")
    myblockchain = Blockchain() # on crée une blockchaine
    for i in range(41): # on crée pleins de transactions aléatoires
        transac ='Alice envoie {} à Bob'.format(random.uniform(0.1, 75.5))
        objet = Transaction(transac,keyPairAlice)
        myblockchain.add(objet)
    myblockchain.check(myblockchain.unconfirmed_transactions[15].transaction_id, keyPairAlice)
    myblockchain.tamper(myblockchain.unconfirmed_transactions[15].transaction_id)
    myblockchain.check(myblockchain.unconfirmed_transactions[15].transaction_id, keyPairAlice)

def main():
    while True:
        print("--------------------------------------------------------------------")
        print("Bienvenue dans le programme Blockchain rédigé par:\nAymeric BOURDIN, Rémi JARDRET,Stéphane SIMON & Thomas PERRAULT")
        print("--------------------------------------------------------------------")
        print(
            " 1. Créér une blockchaine, 5 blocks et les afficher\n",
            "2. Tester les transactions\n",
            "3. Tester la Proof Of Work de notre blockchaine\n",
            "4. Fermer le programme"
        )
        choix = input("Veuillez choisir parmis les options:")
        if choix =="1":
            testBlockchain()
        elif choix == "2":
            testBlockchain()
        elif choix == "3":
            testBlockchain()
        elif choix == "4":
            break
        else:
            print("Veuillez mettre un choix correct")



main()
