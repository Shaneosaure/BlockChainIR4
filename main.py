import hashlib
from datetime import datetime
import json


# Définition d'un block et ses propriètes

class Block:
    # Constructeur d'un block
    def __init__(self, index, temps, data, hashPrecedent):
        self.index = index
        self.temps = temps
        self.data = data
        self.hashPrecedent = hashPrecedent
        self.hash = self.HashBlock()
    
    # Hashage d'un bloc
    def HashBlock(self):
        sha = hashlib.sha256()
        seq = [str(self.index), str(self.temps), str(self.data), str(self.hashPrecedent)]
        sha.update(''.join(seq).encode('utf-8'))
        return sha.hexdigest()

# function test pour afficher un block initial
def test():
    blockchain=Block(index=0,temps=datetime.now(),data="Test", hashPrecedent="0")
    print('Block {} ajouter à {}'.format(blockchain.index, blockchain.temps))
    print('Hash précédent: {}'.format(blockchain.hashPrecedent))
    print('Hash actuel: {}\n'.format(blockchain.hash))


test()