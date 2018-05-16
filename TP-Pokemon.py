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

# Variables globales
# Maximum d'EV qu'un pokémon peut avoir
MAX_EV = 63

# Nombre de genes (groupe de 6 pokémons)
# Creation de la suite à chercher
NB_PARAMETRES = 42

# on cherche 0 en considérant que tous les pokémons
# auront théoriquement tous 10/10 et 6 fois d'où mon écart = 60
VALEUR_VISEE = 0


# Min et max pour le tirage aleatoire des gênes
INT_MIN = 0
INT_MAX = 1061

# Nombre de generations
NGEN = 75
# Taille HallOfFame
THOF = 1

# Taille population
MU = 1061

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

# fonction de fitness
def evaluate(individual):
    #liste = convertInd(individual)  
    #ndex, species, hp, attack, defense, spattack, spdefense, speed, puissance = l.split(",")
    
    ecart = 60
    groupe = []
    puissanceEV = []
    print(individual)
    
    for i in range(0,1162):
        puissanceEV.append(0)
  
    #permet d'éviter l'ajout de trop d'EV
    for i in range(6,42):
        if individual[i] > 63:
            ecart= ecart + 1000
    
    if (individual[6]+individual[7]+individual[8]+individual[9]+individual[10]+individual[11] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[0]] = (individual[6]/maxAttack) + (individual[7]/maxSpattack) + (individual[8]/maxDefense) + (individual[9]/maxSpdefense) + (individual[10]/maxHp) + (individual[11]/maxSpeed)

    if (individual[12]+individual[13]+individual[14]+individual[15]+individual[16]+individual[17] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[1]] = (individual[12]/maxAttack) + (individual[13]/maxSpattack) + (individual[14]/maxDefense) + (individual[15]/maxSpdefense) + (individual[16]/maxHp) + (individual[17]/maxSpeed)

    if (individual[18]+individual[19]+individual[20]+individual[21]+individual[22]+individual[23] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[2]] = (individual[18]/maxAttack) + (individual[19]/maxSpattack) + (individual[20]/maxDefense) + (individual[21]/maxSpdefense) + (individual[22]/maxHp) + (individual[23]/maxSpeed)

    if (individual[24]+individual[25]+individual[26]+individual[27]+individual[28]+individual[29] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[3]] = (individual[24]/maxAttack) + (individual[25]/maxSpattack) + (individual[26]/maxDefense) + (individual[27]/maxSpdefense) + (individual[28]/maxHp) + (individual[29]/maxSpeed)

    if (individual[30]+individual[31]+individual[32]+individual[33]+individual[34]+individual[35] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[4]] = (individual[30]/maxAttack) + (individual[31]/maxSpattack) + (individual[32]/maxDefense) + (individual[33]/maxSpdefense) + (individual[34]/maxHp) + (individual[35]/maxSpeed)

    if (individual[36]+individual[37]+individual[38]+individual[39]+individual[40]+individual[41] > 127):
        ecart = ecart + 500
    else:
        puissanceEV[individual[5]] = (individual[36]/maxAttack) + (individual[37]/maxSpattack) + (individual[38]/maxDefense) + (individual[39]/maxSpdefense) + (individual[40]/maxHp) + (individual[41]/maxSpeed)
   
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
            
            #print(ndex); 
            #print(indiv);
            if rangPokemon == indiv and compteur < 6:
                #print("Pokémon trouvé : " + str(rangPokemon));
                ecart = ecart - float(puissance)- puissanceEV[rangPokemon]
                compteur = compteur + 1
            
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
    
    #groupe_stats = tools.Statistics(key=lambda ind: ind.fitness.values[0])
    #stats = tools.MultiStatistics(groupe=groupe_stats)    
    #stats.register("avg", numpy.mean, axis=0)
    #stats.register("std", numpy.std, axis=0)
    #stats.register("min", numpy.min, axis=0)
    #stats.register("max", numpy.max, axis=0)
    #stats.register("var", numpy.var, axis=0)
    
    #logbook = tools.Logbook()
    
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
    nomPokemon = []
    compteur = 1
    print("Le groupe des 6 meilleurs pokémons est composé de : ")
    for indiv in hof[0]:
        for pokemon in liste:
            ndex, species, hp, attack, defense, spattack, spdefense, speed, puissance = pokemon.split(",")
            rangPokemon = int(ndex);
            
            if rangPokemon == indiv:
                nomPokemon.append(species)
                if compteur < 7 :
                    print("Pokémon " +compteur + ": id = " +ndex + " nom = " +species)
                    print("avec les EV suivants : point de vie = " + indiv[compteur*6] + " attaque = " + indiv[(compteur*6)+1] + " défense = " + indiv[(compteur*6)+2] + " attaque spéciale = " + indiv[(compteur*6)+3] + " défense spéciale = " + indiv[(compteur*6)+4] + " vitesse = " + indiv[(compteur*6)+5])
                compteur = compteur + 1
     
    #plt.show()    