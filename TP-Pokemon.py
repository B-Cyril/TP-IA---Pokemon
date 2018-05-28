#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Permet l'affichage des accents

import random
import numpy
import math
import csv
import time

from deap import algorithms
from deap import base
from deap import creator 
from deap import tools
from math import *
from random import randint

# Heure de démarrage du programme
t = time.time()

# Variables globales
# Maximum d'EV qu'un pokémon peut avoir
MAX_EV = 63
maxHp=0
maxAttack=0
maxSpattack=0
maxDefense=0
maxSpdefense=0
maxSpeed=0

# Nombre de genes (groupe de 6 pokémons)
# Creation de la suite à chercher
NB_PARAMETRES = 42

# on cherche 0 en considérant que tous les pokémons
# auront théoriquement tous 10/10 et 6 fois d'où l'écart = 60
# dans la fonction d'évaluation
VALEUR_VISEE = 0

TRANSFORMATION_EV = 16.59375
# Min et max pour le tirage aleatoire des gênes (nombre de pokémon différents)
INT_MIN = 0
INT_MAX = 1061

# Nombre de generations
NGEN = 5

# Taille HallOfFame
THOF = 1

# Taille population
MU = 100

# Nombre d'enfant produit a chaque generation
LAMBDA = MU
# Probabite de crossover pour 2 individus
CXPB = 0.7
# Probabilite de mutation d'un individu
MUTPB = 0.3

# Algorithme utilise : eaSimple (simple GA), eaMuCommaLambda (evolutionary algorithm mu + lambda), eaGenerateUpdate (ask-tell model), eaMuCommaLambda (evolutionary algorithm mu, lambda),
METHODE = 1

# Creation des outils et population
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", randint, INT_MIN, INT_MAX)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.indices, n=NB_PARAMETRES)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

liste = []
with open('pokemon.csv', newline='', encoding='UTF8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        liste.append(row[0][1:]+","+row[3]+","+row[9]+","+row[10]+","+row[11]+","+row[12]+","+row[13]+","+row[14])
        # enregistre les donnees qui pourront nous servir sur les pokemons (attaque, defense) le [1:] permet de tronquer le " present avant chaque chaine

# permet d'initialiser les maximums de spécialités parmis tous les pokémons pour obtenir un ratio par la suite
for i in liste:
    ndex, species, hp, attack, defense, spattack, spdefense, speed = i.split(",")

    if int(hp) > maxHp:
        maxHp = int(hp)
        
    if int(attack) > maxAttack:
        maxAttack = int(attack)

    if int(spattack) > maxSpattack:
        maxSpattack = int(spattack)
    
    if int(defense) > maxDefense:
        maxDefense = int(defense)

    if int(spdefense) > maxSpdefense:
        maxSpdefense = int(spdefense)
        
    if int(speed) > maxSpeed:
        maxSpeed = int(speed)

maxPuissance=0
i=-1

# calcule la puissance pour chaque pokémon et l'ajoute dans la liste
for l in liste:
    i += 1
    ndex, species, hp, attack, defense, spattack, spdefense, speed = l.split(",")
    puissance= ((((int(hp)/(maxHp+MAX_EV))*1)
                +((int(attack)/(maxAttack+MAX_EV))*1)
                +((int(defense)/(maxDefense+MAX_EV))*1)
                +((int(spattack)/(maxSpattack+MAX_EV))*1)
                +((int(spdefense)/(maxSpdefense+MAX_EV))*1)
                +((int(speed)/(maxSpeed+MAX_EV))*1))*1.6666)
    
    liste[i]=liste[i]+","+str(puissance)
    if puissance > maxPuissance:
        maxPuissance = puissance

# fonction de fitness
def evaluate(individual):
    
    ecart = 60
    groupe = []
    puissanceEV = []
    individu = []
    
    print(individual)

    for i in range(0,1062):
        puissanceEV.append(0)
  
    #permet d'éviter l'ajout de trop d'EV
    for i in range(6,42):
        individu.append(int(individual[i]/TRANSFORMATION_EV))

    if (individu[0]+individu[1]+individu[2]+individu[3]+individu[4]+individu[5] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[0]] = (individu[0]/maxAttack) + (individu[1]/maxSpattack) + (individu[2]/maxDefense) + (individu[3]/maxSpdefense) + (individu[4]/maxHp) + (individu[5]/maxSpeed)
    
    if (individu[6]+individu[7]+individu[8]+individu[9]+individu[10]+individu[11] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[1]] = (individu[6]/maxAttack) + (individu[7]/maxSpattack) + (individu[8]/maxDefense) + (individu[9]/maxSpdefense) + (individu[10]/maxHp) + (individu[11]/maxSpeed)        
    
    if (individu[12]+individu[13]+individu[14]+individu[15]+individu[16]+individu[17] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[2]] = (individu[12]/maxAttack) + (individu[13]/maxSpattack) + (individu[14]/maxDefense) + (individu[15]/maxSpdefense) + (individu[16]/maxHp) + (individu[17]/maxSpeed)

    if (individu[18]+individu[19]+individu[20]+individu[21]+individu[22]+individu[23] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[3]] = (individu[18]/maxAttack) + (individu[19]/maxSpattack) + (individu[20]/maxDefense) + (individu[21]/maxSpdefense) + (individu[22]/maxHp) + (individu[23]/maxSpeed)

    if (individu[24]+individu[25]+individu[26]+individu[27]+individu[28]+individu[29] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[4]] = (individu[24]/maxAttack) + (individu[25]/maxSpattack) + (individu[26]/maxDefense) + (individu[27]/maxSpdefense) + (individu[28]/maxHp) + (individu[29]/maxSpeed)

    if (individu[30]+individu[31]+individu[32]+individu[33]+individu[34]+individu[35] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[5]] = (individu[30]/maxAttack) + (individu[31]/maxSpattack) + (individu[32]/maxDefense) + (individu[33]/maxSpdefense) + (individu[34]/maxHp) + (individu[35]/maxSpeed)
   
    #permet d'éviter les doublons : list(set() vire les doublons et on compare la taille du tableau tronqué avec l'autre
    for i in range(0,6):
        groupe.append(individual[i])
       
    cleanedList = list(set(groupe))
    if len(groupe) != len(cleanedList):
        ecart = ecart + 2000
    
    #initialisation d'un compteur pour enlever la puissance des 6 premiers individus
    compteur = 0   
    for indiv in individual:
        for pokemon in liste:
            ndex, species, hp, attack, defense, spattack, spdefense, speed, puissance = pokemon.split(",")
            rangPokemon = int(ndex);
            
            if rangPokemon == indiv and compteur < 6:
                ecart = ecart - float(puissance)- puissanceEV[rangPokemon]
                compteur = compteur + 1
    
    #print(individu)        
    print(ecart)
        
    return (ecart, individual)

# Suite des outils
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

def main():
    pop = toolbox.population(n=MU)
    hof = tools.HallOfFame(maxsize=THOF)
    stats=0
    if METHODE == 1:
        pop, logbook = algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, NGEN, halloffame=hof)
    
    elif METHODE == 2:
        pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=hof)
        
    elif METHODE == 3:
        pop, logbook = algorithms.eaGenerateUpdate(toolbox, NGEN, stats, hof) 
        
    elif METHODE == 4:
        pop, logbook = algorithms.eaMuCommaLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, halloffame=hof)    

    return pop, hof, logbook
                 
if __name__ == "__main__":
    pop, hof, logbook = main()

    nomPokemon = []
    # tableau de la meilleure equipe
    meilleurPokemon = []

    # stockage des EV de chaque pokémon par tableau
    EVpokemon1 = []
    EVpokemon2 = []
    EVpokemon3 = []
    EVpokemon4 = []
    EVpokemon5 = []
    EVpokemon6 = []
    
    compteur = 1
    compteur2 = 1
    
    for indiv in hof[0]:
        
        for pokemon in liste:
            ndex, species, hp, attack, defense, spattack, spdefense, speed, puissance = pokemon.split(",")
            rangPokemon = int(ndex);
            
            if rangPokemon == indiv:
                nomPokemon.append(species)
                if compteur < 7 :
                    meilleurPokemon.append("Pokémon " +str(compteur) + ": id = " +str(ndex) + " nom = " +str(species))                   
                    compteur = compteur + 1
        
        if compteur2 > 6 and compteur2 < 13:
            EVpokemon1.append(int(indiv/TRANSFORMATION_EV))
        if compteur2 > 12 and compteur2 < 19:
            EVpokemon2.append(int(indiv/TRANSFORMATION_EV))
        if compteur2 > 18 and compteur2 < 25:
            EVpokemon3.append(int(indiv/TRANSFORMATION_EV))
        if compteur2 > 24 and compteur2 < 31:
            EVpokemon4.append(int(indiv/TRANSFORMATION_EV))
        if compteur2 > 30 and compteur2 < 37:
            EVpokemon5.append(int(indiv/TRANSFORMATION_EV))
        if compteur2 > 36:
            EVpokemon6.append(int(indiv/TRANSFORMATION_EV))
        
        compteur2 = compteur2 + 1

    # Affichage
    print("---------------------------------------------------")
    print("Le groupe des 6 meilleurs pokémons est composé de : ")
    print(meilleurPokemon[0])
    print("avec les EV suivants : point de vie = " + str(EVpokemon1[0])
        + " attaque = " + str(EVpokemon1[1]) 
        + " défense = " + str(EVpokemon1[2]) 
        + " attaque spéciale = " + str(EVpokemon1[3]) 
        + " défense spéciale = " + str(EVpokemon1[4]) 
        + " vitesse = " + str(EVpokemon1[5])) 
    print(str(EVpokemon1) + " somme des EV = " +str((EVpokemon1[0]+EVpokemon1[1]+EVpokemon1[2]+EVpokemon1[3]+EVpokemon1[4]+EVpokemon1[5])))
    print(meilleurPokemon[1])
    print(str(EVpokemon2) + " somme des EV = " +str((EVpokemon2[0]+EVpokemon2[1]+EVpokemon2[2]+EVpokemon2[3]+EVpokemon2[4]+EVpokemon2[5])))
    print(meilleurPokemon[2])
    print(str(EVpokemon3) + " somme des EV = " +str((EVpokemon3[0]+EVpokemon3[1]+EVpokemon3[2]+EVpokemon3[3]+EVpokemon3[4]+EVpokemon3[5])))
    print(meilleurPokemon[3])
    print(str(EVpokemon4) + " somme des EV = " +str((EVpokemon4[0]+EVpokemon4[1]+EVpokemon4[2]+EVpokemon4[3]+EVpokemon4[4]+EVpokemon4[5])))
    print(meilleurPokemon[4])
    print(str(EVpokemon5) + " somme des EV = " +str((EVpokemon5[0]+EVpokemon5[1]+EVpokemon5[2]+EVpokemon5[3]+EVpokemon5[4]+EVpokemon5[5])))
    print(meilleurPokemon[5])
    print(str(EVpokemon6) + " somme des EV = " +str((EVpokemon6[0]+EVpokemon6[1]+EVpokemon6[2]+EVpokemon6[3]+EVpokemon6[4]+EVpokemon6[5])))
    
    tempsFinal = (time.time()-t)
    duree = " seconde(s)"
    if ((time.time()-t) > 60 and (time.time()-t) < 3600):
        tempsFinal = tempsFinal/60
        duree = " minute(s)"
    elif ((time.time()-t) > 3600):
        tempsFinal = tempsFinal/3600
        duree = " heure(s)"
    
    print("Temps de calul : " + str(tempsFinal) + duree)
    print("---------------------------------------------------")
    input("Terminé ? Appuyez sur une touche")
