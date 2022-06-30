# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 20:26:21 2022

@author: Bryan
"""

# Modulo 1 - Crear una cadena de Bloques

# Instalar con Anaconda Pronpt el comando >> pip install Flask==0.12.2

# Instalar las Librerias
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Parte 1 - Crear la Carpeta de Bloques
class Blockchain:
    
    #############################################################
    # Funcion para inicializar el bloque
    #############################################################
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    #############################################################
    # Funcion para Crear el Bloque
    #############################################################
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
            }
        self.chain.append(block)
        return block
    
    
    ##############################################################
    # Funcion que devuelve el ultimo bloque
    #############################################################
    def get_previous_block(self):
        return self.chain[-1]
    
    #############################################################
    # Esta es la funcion de Minado para el Bloque
    #############################################################
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof

    #############################################################
    # Funcion que devuelve el block actual
    #############################################################
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    #############################################################
    # Funcion que valida si la cadena de bloque es valido
    #############################################################
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_block = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_block**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True




# Parte 2 - minando de un Bloque de la Cadena

#############################################################
# Crear una aplicacion web con Flask
# Documnetacion de Flask: 
# https://flask.palletsprojects.com/en/2.1.x/quickstart/
# Running on http://127.0.0.1:5000/
# 1. Funcion para Minar bloques
# 2. Funcion para Obtener los Bloques
#############################################################
app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

#############################################################
# Crear una Blockchain
#############################################################
blockchain = Blockchain()


#############################################################
# Minar un nuevo Bllque
#############################################################
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Uruguay noma! Has minado un nuvo Bloque!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        }
    return jsonify(response), 200

#############################################################
# Obtener la cadena de Bloqueas completa
#############################################################
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        }
    return jsonify(response), 200
    
    
#############################################################
# Ejecutar la App en una ruta accecible dentro de la red
#############################################################
app.run(host = '0.0.0.0', port = 5000)

