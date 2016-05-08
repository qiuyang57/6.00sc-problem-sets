# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy as np
import random
import matplotlib.pyplot as plt
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb



    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.resistances:
            return self.resistances[drug]
        else:
            return False


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """

        reproduceProb = self.maxBirthProb * (1 - popDensity)
        ResistBool = True
        OffspringResistances = {}
        for drug in activeDrugs:
            ResistBool = ResistBool and self.isResistantTo(drug)
        if not ResistBool:
            raise NoChildException()
        elif random.random() > reproduceProb:
            raise NoChildException()
        else:
            for drug in self.resistances.keys():
                if random.random() < self.mutProb:
                    OffspringResistances[drug] = not self.resistances[drug]
                else:
                    OffspringResistances[drug] = self.resistances[drug]
        return ResistantVirus(self.maxBirthProb, self.clearProb, OffspringResistances, self.mutProb)











class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        SimplePatient.__init__(self, viruses, maxPop)
        self.drugsUsing = []


    

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # should not allow one drug being added to the list multiple times

        if self.drugsUsing.count(newDrug) == 0:
            self.drugsUsing.append(newDrug)


    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugsUsing
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        ResistPop = 0
        for virus in self.viruses:
            AllResistance = True
            for drug in drugResist:
                AllResistance = AllResistance and virus.isResistantTo(drug)
            if AllResistance:
                ResistPop += 1
        return ResistPop





                   


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        survived_viruses = []
        for virus in self.viruses:
            if not virus.doesClear():
                survived_viruses.append(virus)
        self.viruses = survived_viruses
        popDensity = len(survived_viruses) / float(self.maxPop)
        offsprings = []
        for virus in survived_viruses:
            try:
                offspring = virus.reproduce(popDensity, self.drugsUsing)
                offsprings.append(offspring)
            except NoChildException:
                pass
        self.viruses = survived_viruses + offsprings
        return self.getTotalPop()




#
# PROBLEM 2
#
def generateResistVirusesList(viruses_num, maxBirthProb, clearProb, resistances, mutProb):
    viruses_list = []
    for _ in xrange(viruses_num):
        viruses_list.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
    return viruses_list


def simulationWithDrug():

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    viruses_num = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    maxPop = 1000
    timesteps1 = 150
    timesteps2 = 150
    num_trials = 100
    mutProb = 0.005
    resistances = {'guttagonol': False}
    virusesPopsum = 0
    ResistPopsum = 0
    for i in xrange(num_trials):
        viruses_list = generateResistVirusesList(viruses_num, maxBirthProb, clearProb, resistances, mutProb)
        virusesPop = []
        ResistPop = []
        PatientA = Patient(viruses_list, maxPop)
        for time in xrange(timesteps1):
            virusesPop.append(PatientA.update())
            ResistPop.append(PatientA.getResistPop(['guttagonol']))
        PatientA.addPrescription('guttagonol')
        for time in xrange(timesteps2):
            virusesPop.append(PatientA.update())
            ResistPop.append(PatientA.getResistPop(['guttagonol']))
        virusesPopArray = np.array(virusesPop)
        ResistPopArray = np.array(ResistPop)
        if type(virusesPopsum) == int:
            virusesPopsum = virusesPopArray
            ResistPopsum = ResistPopArray
        else:
            virusesPopsum += virusesPopArray
            ResistPopsum += ResistPopArray
    virusesPopAverage = list(virusesPopsum / float(num_trials))
    ResistPopAverage = list(ResistPopsum / float(num_trials))
    plt.plot(xrange(timesteps1 + timesteps2), virusesPopAverage, 'b-', label="Total")
    plt.plot(xrange(timesteps1 + timesteps2), ResistPopAverage, 'r-', label="ResistantViruses")
    plt.xlabel('Elapsed time steps')
    plt.ylabel('The population of the virus in the patient')
    plt.title('Virus grows in the patient')
    plt.legend(loc="best")
    plt.show()


# simulationWithDrug()


#
# PROBLEM 3
#        

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    delays = [300, 150, 75, 0]
    viruses_num = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    maxPop = 1000
    timesteps = 150
    num_trials = 300
    mutProb = 0.005
    resistances = {'guttagonol': False}
    virusesPop = [[0 for _ in xrange(num_trials)] for _ in xrange(4)]
    for k in xrange(4):
        delay = delays[k]
        for i in xrange(num_trials):
            viruses_list = generateResistVirusesList(viruses_num, maxBirthProb, clearProb, resistances, mutProb)
            PatientA = Patient(viruses_list, maxPop)
            for time in xrange(delay + timesteps):
                if time == delay:
                    PatientA.addPrescription('guttagonol')
                virusesPop[k][i] = PatientA.update()
    for num in xrange(4):
        plt.subplot(2, 2, num+1)
        plt.title("delay: " + str(delays[num]))
        plt.xlabel("final viruses number")
        plt.ylabel("number of trials")
        plt.hist(virusesPop[num], bins=12, range=(0, 600))
    plt.show()

# simulationDelayedTreatment()






#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    delays = [300, 150, 75, 0]
    viruses_num = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    maxPop = 1000
    timesteps = 300
    num_trials = 300
    mutProb = 0.005
    resistances = {'guttagonol': False, 'grimpex': False}
    virusesPop = [[0 for _ in xrange(num_trials)] for _ in xrange(4)]
    for k in xrange(4):
        delay = delays[k]
        for i in xrange(num_trials):
            viruses_list = generateResistVirusesList(viruses_num, maxBirthProb, clearProb, resistances, mutProb)
            PatientA = Patient(viruses_list, maxPop)
            for time in xrange(delay + timesteps):
                if time == 150:
                    PatientA.addPrescription('guttagonol')
                elif time == 150 + delay:
                    PatientA.addPrescription('grimpex')
                virusesPop[k][i] = PatientA.update()
    for num in xrange(4):
        plt.subplot(2, 2, num+1)
        plt.title("time interval: " + str(delays[num]))
        plt.xlabel("final viruses number")
        plt.ylabel("number of trials")
        plt.hist(virusesPop[num], bins=12, range=(0, 600))
    plt.show()

# simulationTwoDrugsDelayedTreatment()




#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    delays = [300, 0]
    viruses_num = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    maxPop = 1000
    timesteps = 300
    num_trials = 100
    mutProb = 0.005
    resistances = {'guttagonol': False, 'grimpex': False}
    virusesPopAverage = [[], []]
    guttagonolResistPopAverage = [[], []]
    grimpexResistPopAverage = [[], []]
    bothPopResistAverage = [[], []]
    for k in xrange(2):
        delay = delays[k]
        virusesPopsum = 0
        guttagonolResistPopsum = 0
        grimpexResistPopsum = 0
        bothResistPopsum = 0
        for i in xrange(num_trials):
            virusesPop = []
            guttagonolResistPop = []
            grimpexResistPop = []
            bothResistPop = []
            viruses_list = generateResistVirusesList(viruses_num, maxBirthProb, clearProb, resistances, mutProb)
            PatientA = Patient(viruses_list, maxPop)
            for time in xrange(timesteps + delay):
                if time == 150:
                    PatientA.addPrescription('guttagonol')
                if time == 150 + delay:
                    PatientA.addPrescription('grimpex')
                virusesPop.append(PatientA.update())
                guttagonolResistPop.append(PatientA.getResistPop(['guttagonol']))
                grimpexResistPop.append(PatientA.getResistPop(['grimpex']))
                bothResistPop.append(PatientA.getResistPop(['guttagonol', 'grimpex']))
            virusesPopArray = np.array(virusesPop)
            guttagonolResistPopArray = np.array(guttagonolResistPop)
            grimpexResistPopArray = np.array(grimpexResistPop)
            bothResistPopArray = np.array(bothResistPop)
            if type(virusesPopsum) == int:
                virusesPopsum = virusesPopArray
                guttagonolResistPopsum = guttagonolResistPopArray
                grimpexResistPopsum = grimpexResistPopArray
                bothResistPopsum = bothResistPopArray
            else:
                virusesPopsum += virusesPopArray
                guttagonolResistPopsum += guttagonolResistPopArray
                grimpexResistPopsum += grimpexResistPopArray
                bothResistPopsum += bothResistPopArray
        virusesPopAverage[k] = list(virusesPopsum / float(num_trials))
        guttagonolResistPopAverage[k] = list(guttagonolResistPopsum / float(num_trials))
        grimpexResistPopAverage[k] = list(grimpexResistPopsum / float(num_trials))
        bothPopResistAverage[k] = list(bothResistPopsum / float(num_trials))

        plt.subplot(1, 2, k + 1)
        plt.plot(xrange(timesteps + delay), virusesPopAverage[k], 'b-', label="Total")
        plt.plot(xrange(timesteps + delay), guttagonolResistPopAverage[k], 'r-', label="Guttagonol-resistant Viruses")
        plt.plot(xrange(timesteps + delay), grimpexResistPopAverage[k], 'g-', label="Grimpex-resistant Viruses")
        plt.plot(xrange(timesteps + delay), bothPopResistAverage[k], 'm-', label="Both drugs resistant Viruses")
        plt.xlabel('Elapsed time steps')
        plt.ylabel('The population of the virus in the patient')
        plt.title('Virus grows in the patient with %d time delay between drugs' % delay)
        plt.legend(loc="upper right", fontsize="x-small")
    plt.show()

simulationTwoDrugsVirusPopulations()


