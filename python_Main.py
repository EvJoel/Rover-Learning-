# -*- coding: utf-8 -*-
"""
Created on Wed Oct 07 12:34:03 2015

@author: ackbe_000
"""
import random as rd
import socket
import re
from math import *
import time
import os.path

#Global variables

NUM_SEQ = 5
NUM_CHROMES = 5
NUM_GEN = 5
CURR_GEN = 5

CHROM_MUTATE_RATE = .
GENE_MUTATE_RATE = .33

host = "10.201.109.60"
port = 1337

k = [0.65, 0.2, 0.1, 0.5]


START = [0,0,0] #Markers for the starting area
GOAL = [0,0,1] #Markers for the finish area
 
########################################################################################
    
def createGeneration():
    generation = [[[rd.randint(0,180), rd.randint(0,180), rd.randint(1,1)] for i in range(NUM_CHROMES)] for i in range(NUM_SEQ)] #Creates a generation with chromosomes ranging between (0,180) and (1,4)
    print "Created Generation with " + str(NUM_SEQ) + " sequences consisting of " + str(NUM_CHROMES) + " Chromosomes" 
    return generation
    
def printSequence(seq):
    for i in range(len(seq)): # prints a sequence in a readable way
        print seq[i]
        
        
        
def writeGeneration(gen, gen_num):
    global CURR_GEN
    os.mkdir("/media/galileo/generation" + str(gen_num))
    genFile = open("/media/galileo/generation" + str(gen_num) + "/generation" + "_" + str(time.strftime("%H_%M_%S")) + ".txt", 'w') #creates a generation file 
    readGenFile = open("/media/galileo/generation.txt", 'w')
    for i in range(len(gen) ):
        for j in range(len(gen[i]) ):
            for m in range(len(gen[i][j])  ):
                genFile.write(str(gen[i][j][m]) + ",")
                readGenFile.write(str(gen[i][j][m]) + ",")
        genFile.write("\n")
        readGenFile.write("\n")
    genFile.close()
    readGenFile.close()
    CURR_GEN += 1
        
def recieveData():
    no_data = True
    data = ""
    start = time.time()
    while no_data:
	try:
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.connect((host,port))
	    s.send("Ready to recieve data")
	    reply = s.recv(1024)
	    s.close()
	    print reply
	    data = reply
	    parsed_data = parseData(data)
	    no_data = False
	    
	except socket.error as msg:
	    print msg
	    elapsed = time.time()
	    if (elapsed-start) >= 1:
		changeState(6)
		print "Data loss too great, sequence data invalid..."
    
	    
	    
        
    return parsed_data
    
def parseData(data):
    no_data = True
    #while no_data:
    try:
	pData = re.findall("\((.*?)\)", data)
	pData = pData[0].split(",")
	for i in range(len(pData)):
	    pData[i] = float(pData[i])
	#no_data = False
    except:
	print "no data"
	time.sleep(.5)
    return pData
    
def createStateFile():
    stateFile = open("/media/galileo/state.txt", 'w')
    print "Created state file"
    stateFile.write("0")
    stateFile.close()
    
def readState():
    no_state = True
    while no_state:
	try:
	    stateFile = open ("/media/galileo/state.txt", 'r')
	    state = stateFile.read()
	    stateFile.close()
	    no_state = False
	except:
	    print "cannot read stateFile"
    return state    

def changeState(state):
    statefile = open ("/media/galileo/state.txt", 'w')
    statefile.write(str(state))
    statefile.close()    

def getFitness(dist_from_goal, dist_traveled, elap_time, dist_goal_final):
    fitness = (float(dist_from_goal) * k[0]) + (float(dist_traveled) * k[1]) + ((float(elap_time) * k[2])/10) + (float(dist_goal_final) * k[3])
    return fitness
    
def mutateSequence(seq):
    global MUTATE_NUM
    new_seq = []
    for i in range(len(seq)):
	new_seq.append(list(seq[i]))
	
    for i in range(len(new_seq)):
        mutate_chance_chromo = 100 * CHROM_MUTATE_RATE #Numbers used to decide whether a chromosome in the sequence is mutated
        mutate_number_chromo = rd.randint(1,100)
        
        if(mutate_number_chromo <= mutate_chance_chromo):
	    #if one is greater, it has the possibility to mutate
            for j in range(3):
		#loops through each gene
                pos_neg = rd.randint(0,100) #add or subtract from gene
                mutate_number_gene = rd.randint(0,100) #Numbers used to decide whether a gene in the sequence is mutated
                mutate_chance_gene = 100 * GENE_MUTATE_RATE
                MUTATE_NUM = rd.randint(1,100)  #amount gene is changed by
                if(mutate_number_gene <= mutate_chance_gene):
                    change = 0
                    if(j < 2):
                        if(mutate_chance_gene <= 50):
                            change =  MUTATE_NUM*.1
                        elif(mutate_chance_gene <= 70 and mutate_rate > 50):
                            change = MUTATE_NUM *.15
                        elif(mutate_chance_gene <= 80 and mutate_rate > 70):
                            change =  MUTATE_NUM*.20
                        elif(mutate_chance_gene <= 85 and mutate_rate > 80):
                            change =  MUTATE_NUM*.25
                        elif(mutate_chance_gene <= 90 and mutate_rate > 85):
                            change =  MUTATE_NUM*.30
                        elif(mutate_chance_gene <= 94 and mutate_rate > 90):
                            change =  MUTATE_NUM*.4   
                        elif(mutate_chance_gene <= 97 and mutate_rate > 94):
                            change =  MUTATE_NUM*.5
                        elif(mutate_chance_gene <= 99 and mutate_rate > 97):
                            change =  MUTATE_NUM*.6
                        else:
                            change =  MUTATE_NUM*.7
                    
                        if(pos_neg >= 50):
                            #print new_seq[i][j]
                            new_seq[i][j]  = new_seq[i][j] + int(change)
                            #print "pos " +str(change)
                        else:
                            new_seq[i][j] = new_seq[i][j] - int(change)
                            #print "neg " +  str(change)
                            
                        if(new_seq[i][j] > 180):
                            new_seq[i][j] = 180
                        if(new_seq[i][j] < 0):
                            new_seq[i][j] = 0          
                        
                    else:
                        #used for mutating time genes
                        if(new_seq[i][j] ==1):
                            if(mutate_chance_gene <= 60):
                                new_seq[i][j] = 2
                            elif(mutate_chance_gene > 60 and mutate_rate <= 90):
                                new_seq[i][j] =  3
                            else:
                                new_seq[i][j] = 4
                                
                        elif(new_seq[i][j] ==2):
                            if(mutate_chance_gene <= 40):
                                new_seq[i][j] = 1
                            elif(mutate_chance_gene > 40 and mutate_rate <= 80):
                                new_seq[i][j] =  3
                            else:
                                new_seq[i][j] = 4
                                
                        elif(new_seq[i][j] ==3):
                            
                            if(mutate_chance_gene <= 60):
                                new_seq[i][j] = 3
                            elif(mutate_chance_gene > 60 and mutate_rate <= 90):
                                new_seq[i][j] =  4
                            else:
                                new_seq[i][j] = 1  
                                
                        else:
                            if(mutate_chance_gene <= 60):
                                new_seq[i][j] = 3
                            elif(mutate_chance_gene > 60 and mutate_rate <= 90):
                                new_seq[i][j] =  2
                            else:
                                new_seq[i][j] = 1                           
                            
                                    
    return new_seq
            
def getDistance(x1,y1,x2,y2):
    distance = sqrt(((x2-x1)**2) + ((y2-y1)**2))
    return distance 

def getTime():
    tfile = open("/media/galileo/tfile.txt", 'r')
    time = tfile.read()
    return time

def record_fitness(gen_num, gen_fitness):
    genFitness = open("/media/galileo/generation" + str(gen_num) + "/fitness_gen.txt", 'w')
    for i in range(len(gen_fitness)):
	genFitness.write(str(gen_fitness[i]) + "%")
    genFitness.close()
    
    
def recordPositionData(genPosition, gen_num):
    gen_position = open("/media/galileo/generation" + str(gen_num) + "/gen_position.txt", 'w')
    for i in range(len(genPosition)):
	gen_position.write(str(genPosition[i]) + "\n")
    gen_position.close()
def printCurrentInfo(gen, seq, state):
    
    print "####################################################"
    print ""
    print "State: " + str(state) + " | " + "Gen: " + str(gen) + " | " + "Seq: " + str(seq) 
    print ""
    print "####################################################"
      
   
def readFitness(gen_num):
    generation_new = [[0,0,0] for i in range(NUM_CHROMES)]
    current_gene = 0
    most_fit = 100000000000
    most_fit_num = 0
    
   # os.chdir('C:\PSCP')
    for filename in os.listdir('/media/galileo'):
	os.chdir('/media/galileo')
	if ("generation" + str(gen_num)) in filename and ".txt" not in filename:
	    os.chdir(os.getcwd() + "/" + filename)
	    print(os.getcwd())
	    fitness = open(os.getcwd() + "/" + "fitness_gen.txt")
	    gen_fitness = (fitness.read()).split('%')
	    print gen_fitness
	    fitness.close()
	    for i in range(len(gen_fitness)-1): #test fitness is wrong, change when actually testing
		parsed_fit = gen_fitness[i].replace("[", "")
		parsed_fit = parsed_fit.replace("]", "")
		parsed_fit = parsed_fit.split(",")
		gen_fitness[i] = parsed_fit
		print gen_fitness[i][1]
		gen_fitness[i][1] = float(gen_fitness[i][1])
		if(gen_fitness[i][1] <= most_fit):
		    most_fit = gen_fitness[i][1]
		    most_fit_num = int(gen_fitness[i][0])
		# parsed_fit    
	    print gen_fitness
	    print most_fit
	    print most_fit_num
			
    for filename in os.listdir(os.getcwd()):
	if "generation" in filename and ".txt" in filename:
	    filepath = str(os.getcwd()) + "/" +  str(filename) 
	    print filepath
	    gen_file = open(filepath, 'r')
	    unparsed = gen_file.read()
	    gen_file.close()
	    parsed = unparsed.split(",")
	    print parsed
	    print len(parsed)
	    print generation_new
	    #print (((most_fit_num + 1) * NUM_CHROMES * NUM_SEQ) - 2)
	    if(most_fit_num == 0):
		#print "hello"
		current_gene = 0
		for i in range(10):
		    
		    while current_gene <= ((NUM_CHROMES * 3) - 2):
			print parsed[15]
			generation_new[i][0] = int(parsed[current_gene]) 
			generation_new[i][1] = int(parsed[current_gene+1])
			generation_new[i][2] = int(parsed[current_gene+2])
			current_gene += 3
			break
	    else:
		current_gene = most_fit_num * NUM_CHROMES * 3
		for i in range(10):
		    while i <= (((most_fit_num + 1) * NUM_CHROMES * 3) - 2):
			generation_new[i][0] = int(parsed[current_gene]) 
			generation_new[i][1] = int(parsed[current_gene+1])
			generation_new[i][2] = int(parsed[current_gene+2])
			current_gene += 3
			break			
	    print generation_new	
		    
	    mutated_gen = []
	    for i in range(NUM_SEQ):
		mutated_gen.append(mutateSequence(generation_new))	    
	    return mutated_gen    

    

    
##########################################################################################################################
#readFitness(1)
test = [[rd.randint(0,180), rd.randint(0,180), rd.randint(1,1)] for i in range(NUM_CHROMES)]
test2 = []
for i in range(len(test)):
    test2.append(mutateSequence(test))
    #print test
    print test2[i]
    
##Main execution loop "
#generation = []
#current_seq = 0
#current_gen = 0
#new_gen = 0
#elapsed_time = 0  
#elapsed_distance = 0
#seq_position = []
#gen_position = []
#old_position = START
#dist_from_goal = getDistance(GOAL[0],GOAL[2],START[0],START[2])
#gen_fitness = []
#goal_dist = 0
#goal_made = False

#not_ready = True
#while not_ready:
    #answer = raw_input("Program Started: Continue previous Experiment (1) or start new experiment (2)? : ")
    #if(answer == '1'):
	#gen_num = raw_input("Enter the number of the generation you would like to continue")
	#print "Starting experiment"
	#current_gen = int(gen_num) + 1
	#new_gen = int(gen_num)
	#write_gen = readFitness(int(gen_num))
	#writeGeneration(write_gen,int(gen_num)+1 )
	#generation = write_gen
	#changeState(0)
	#not_ready = False
	
    #elif(answer == '2'):
	#print "Starting new experiment, make sure previous files are deleted"
	#not_ready = False
    #else: 
	#print "invalid"
	


#while NUM_GEN > 0:
    
    #time.sleep(.25)
    
    #if os.path.isfile("/media/galileo/state.txt") != True:
        #print "No startup files found, creating files..."
        #generation = createGeneration()
        #writeGeneration(generation,current_gen)
	 ##test
        #createStateFile()
        #print "Files Created"
        
    #else:
        #state = int(readState())
	
	#printCurrentInfo(current_gen, current_seq, state)
	##print state
        #if state == 0:
            #if new_gen == current_gen:
                #time.sleep(3)
                #position = recieveData()
		
		#print position
		#print getDistance(START[0], START[0], position[0],position[2])
                #if getDistance(START[0],START[2],position[0],position[2]) < .05:
                    #changeState(1)
                    
            #else:
                #print "Generation Numbers do not match, writing new generation for execution"
                #current_gen = new_gen
                
                
        #elif state == 1:
            #if(new_gen == current_gen):
                #position = recieveData()
		#seq_position.append(position)
                #elapsed_distance += getDistance(position[0], position[2], old_position[0], old_position[2])
                #old_position = position
		#print elapsed_distance
                #if(getDistance(GOAL[0],GOAL[2],position[0],position[2]) < dist_from_goal):
                    #goal_made = True
		    #dist_from_goal = getDistance(GOAL[0],GOAL[2],position[0],position[2])
                
                
        #elif state == 2:
            #elapsed_time = getTime()
	    #gen_position.append(seq_position)
	    #goal_dist = getDistance(GOAL[0],GOAL[2],old_position[0],old_position[2])
            #gen_fitness.append([current_seq, getFitness(dist_from_goal, elapsed_distance, elapsed_time, goal_dist), goal_made])
	    #print "Sequence fitness: " + str(getFitness(dist_from_goal, elapsed_distance, elapsed_time, goal_dist))
	    #time.sleep(2)
            #elapsed_distance = 0
            #goal_made = False
	    #goal_dist = 0
	    #seq_position = []
            #current_seq += 1
            #changeState(3)
		
        #elif state == 3:
	    #print "Waiting for Arduino"

        #elif state == 4:
	    #recordPositionData(gen_position, current_gen)
	    #record_fitness(new_gen,gen_fitness)
            #most_fit = [0,100000000000]
            #for i in range(len(gen_fitness)):
                #if(gen_fitness[i][1] < most_fit[1]):
                    #most_fit = gen_fitness[i]
            #mutated_gen = []
	    #print generation
            #print gen_fitness
            #print "Most fit sequence: " + str(most_fit)
            #for i in range(NUM_SEQ):
                #mutated_gen.append(mutateSequence(generation[most_fit[0]]))
            #generation = mutated_gen
            #new_gen += 1
            #NUM_GEN -= 1
            #gen_fitness = []
	    #gen_position = []
	    #current_seq = 0
	    #writeGeneration(generation, new_gen) 
            #changeState(5)
                    
        #elif state == 5:
            #print "Waiting for Arduino..."
	    
	#elif state == 6:
	    #print "Data loss occurred, sequence must be retested"
	    #elapsed_distance = 0
	    #gen_position[current_seq] = []
	    ##test
	#elif state == 7:
	    #changeState(0)
	    #print "Found previous experiment, rerunning it"
	    
	    
#print "Experiment has finished"
#print "Most fit Sequence: " + str(most_fit) + " in generation " + str(current_gen)
#changeState(7)
            
            


#testGeneration = createGeneration()
#testSeq = testGeneration[0][0:20]
#print testSeq

#start = time.time()
#for i in range(1000000):
    #newSeq = mutateSequence(testSeq)
    #test_seq = newSeq
#elapsed = time.time() - start
#print newSeq
#print "Time: " + str(elapsed)


#printSequence(testSequence)
#writeSequence(testSequence)
#print testSequence[1]
#createStateFile()
#print readState()



    
    
#def mutate():

    
    
    
