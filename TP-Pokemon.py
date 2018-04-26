#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Permet l'affichage des accents

import random
import numpy
import math
import csv

from deap import algorithms
from deap import base
from deap import creator 
from deap import tools
from math import *
from random import randint

# Maximum d'EV qu'un pokémon peut avoir [variable globale]
MAX_EV = 63

# Nombre de genes (groupe de6 pokémons)
# Creation de la suite Ã  chercher
NB_PARAMETRES = 6

# est ce que la valeur n'est pas plutôt 0 car on cherche une équipe de pokémons 
# ayant théoriquement tous 10/10 et 6 fois d'où mon écart = 60
VALEUR_VISEE = 10


# Min et max pour le tirage aleatoire des genes
# METTRE UNE CONDITION POUR NE PAS POUVOIR CHOISIR 2 FOIS LE MEME
INT_MIN = 0
INT_MAX = 1061
# Nombre de generations
NGEN = 1
# Taille HallOfFame
THOF = 6

# Taille population
MU = 1061

# Nombre d'enfant produit a chaque generation
LAMBDA = MU
# Probabite de crossover pour 2 individus
CXPB = 0.7
# Probabilite de mutation d'un individu
MUTPB = 0.2

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
        liste.append(row[0][1:]+","+row[2]+","+row[9]+","+row[10]+","+row[11]+","+row[12]+","+row[13]+","+row[14])
        # enregistre les donnees qui pourront nous servir sur les pokemons (attaque, defense) le [1:] permet de tronquer le " present avant chaque chaine
maxHp=0
maxAttack=0
maxSpattack=0
maxDefense=0
maxSpdefense=0
maxSpeed=0

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


# fonction de conversion d'un individu
#def convertInd(individual):
    
    #ECRIRE ICI SI BESOIN DE RAJOUTER DES COEFFICIENTS
   
    #return liste

# fonction pour l'affichage d'un individu
def readResult(individual):
    chaine = convertInd(individual)
    
    texte = liste[individual[1]]
    
    resultat1, resultat2 = evaluate(liste)
    print (resultat2)
    
    
    return texte, resultat1, resultat2                                          

# fonction de fitness
def evaluate(individual):
    #liste = convertInd(individual)  
    #ndex, species, hp, attack, defense, spattack, spdefense, speed, puissance = l.split(",")
    
    ecart = 60
    print(individual)
    
    
    #permet d'éviter les doublons : list(set() vire les doublons et on compare la taille du tableau tronqué avec l'autre
    cleanedList = list(set(individual))
    if len(individual) != len(cleanedList):
        ecart=2000
                

    
    for indiv in individual:
        for pokemon in liste:
            ndex, species, hp, attack, defense, spattack, spdefense, speed, puissance = pokemon.split(",")
            rangPokemon = int(ndex);
            
            #print(ndex); 
            #print(indiv);
            if rangPokemon == indiv:
                #print("Pokémon trouvé : " + str(rangPokemon));
                #print(indiv)                
                ecart = ecart - float(puissance)
    print(ecart);
    return (ecart, individual) 

# Suite des outils
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

def main():    
    pop = toolbox.population(n=MU)
    hof = tools.HallOfFame(maxsize=THOF)
    
    groupe_stats = tools.Statistics(key=lambda ind: ind.fitness.values[0])
    stats = tools.MultiStatistics(groupe=groupe_stats)    
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    stats.register("var", numpy.var, axis=0)
    
    logbook = tools.Logbook()
    
    if METHODE == 1:
        pop, logbook = algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, NGEN, stats, halloffame=hof)
    
    elif METHODE == 2:
        pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=hof)
        
    elif METHODE == 3:
        pop, logbook = algorithms.eaGenerateUpdate(toolbox, NGEN, stats, hof) 
        
    elif METHODE == 4:
        pop, logbook = algorithms.eaMuCommaLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=hof)    
        
    record = stats.compile(pop)

    return pop, stats, hof, logbook
                 
if __name__ == "__main__":
    pop, stats, hof, logbook = main()
    """   
    import matplotlib.pyplot as plt
    
    gen = logbook.select("gen")
    dist_mins = logbook.chapters["groupe"].select("min")  
    dist_maxs = logbook.chapters["groupe"].select("max")
    dist_avgs = logbook.chapters["groupe"].select("avg")
    
    nrj_mins = logbook.chapters["energie"].select("min")  
    nrj_maxs = logbook.chapters["energie"].select("max")    
    nrj_avgs = logbook.chapters["energie"].select("avg")
    
    dist_var = logbook.chapters["groupe"].select("var")
    nrj_var = logbook.chapters["energie"].select("var")
    velocite = logbook.chapters["velocite"].select("max")
    alpha = logbook.chapters["alpha"].select("max")
    
    fig = plt.figure()
    
    ax1 = plt.subplot(1,2,1)
    line1 = ax1.plot(gen, dist_avgs, "blue", linewidth=2.5, label="Valeur")
    plt.fill_between(gen, dist_mins, dist_maxs, color='blue',  alpha=.25)
    plt.ylim(0,VALEUR_VISEE*4)
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Valeur", color="b")
          
    ax3 = plt.subplot(1,2,2)
    line3 = ax3.plot(gen, dist_var, "blue", label="Variance (groupe)")
    ax3.set_xlabel("Generation")
    ax3.set_ylabel("Variance", color="blue")    
"""
    
    for i in range(THOF):
        texte, resultat1, resultat2 = readResult(hof[i])
        print('text = ' + str(texte))
        print('group = '+ str(resultat1))
        print('ecart = '+ str(resultat2))
        
    plt.show()    