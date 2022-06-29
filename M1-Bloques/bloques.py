# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 20:26:21 2022

@author: Bryan
"""

#Modulo 1 - Crear una cadena de Bloques

#Instalar con Anaconda Pronpt el comando >> pip install Flask==0.12.2

#Instalar las Librerias
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Parte 1 - Crear la Carpeta de Bloques
class Blockchain:
    
    #############################################################
    #Funcion para inicializar el bloque
    #############################################################
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    #############################################################
    #Funcion para Crear el Bloque
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
    #Esta es la funcion de Minado para el Bloque
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


# Parte 2 - minando de un Bloque de la Cadena