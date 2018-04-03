#Author: Corey Thompson
#Date: 3/21/18
#DataAnalysis Capstone Project
#
#Exercises some data tools with a couple datasets concerning endangered species.
#

#definitions
def PrintStep(step):
    line = '############# STEP ' + str(step) + ' ###############################'
    print('\n#---------------------------------------------------')
    print(line)
    print('#---------------------------------------------------')

#---------------------------------------------------
############# STEP 1 ###############################
#---------------------------------------------------
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency
import pandas as pd

currentStep = 0
currentStep += 1    
PrintStep(currentStep)
#---------------------------------------------------
############# STEP 2 ###############################
#---------------------------------------------------
currentStep += 1    
PrintStep(currentStep)

species = pd.read_csv('species_info.csv')
#print(species.head())
#---------------------------------------------------
############# STEP 3 ###############################
#---------------------------------------------------
currentStep += 1    
PrintStep(currentStep)

num_species =  len(set(species['scientific_name']))
#print(num_species)
#5541 species

categories_species = set(species['category'])
#print(categories_species)
#set(['Reptile', 'Fish', 'Amphibian', 'Vascular Plant', 'Mammal', 'Nonvascular Plant', 'Bird'])

status_species = set(species['conservation_status'])
#print(status_species)
#set([nan, 'Endangered', 'In Recovery', 'Threatened', 'Species of Concern'])

#---------------------------------------------------
############# STEP 4 ###############################
#---------------------------------------------------
currentStep += 1    
PrintStep(currentStep)

print("\nUnique species by conservation status:")
print(species.groupby(['conservation_status']).scientific_name.count().reset_index())

species.fillna('No Intervention', inplace=True)
print("\nUnique species by conservation status without empties:")
print(species.groupby(['conservation_status']).scientific_name.count().reset_index())

print("\nUnique species by conservation status, sorted:")
protection_counts = species.groupby('conservation_status')\
    .scientific_name.count().reset_index()\
    .sort_values(by='scientific_name')
print(protection_counts)

print("\nNow let's create a bar chart!")
plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)),protection_counts['scientific_name'])
ax.set_xticks(range(len(status_species)))
ax.set_xticklabels(protection_counts['conservation_status'])
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show()

#---------------------------------------------------
############# STEP 4 ###############################
#---------------------------------------------------
#??? Two step 4's in notebook.
PrintStep(currentStep)

print("\nLet's create a new column in species called is_protected")#, 
#which is True if conservation_status is not equal to No Intervention, and False otherwise.
species['is_protected'] = species['conservation_status'].apply(lambda status: 'True' if status != 'No Intervention' else 'False')
#print(species)

print("\nLet's group by both category and is_protected.")# Save your results to category_counts.
category_counts = species.groupby(['category','is_protected']).scientific_name.nunique().reset_index().sort_values(by='category')
print(category_counts)

print("\nIt's going to be easier to view this data if we pivot it.")# Using pivot, rearange category_counts so that:")
#columns is conservation_status
#index is category
#values is scientific_name
#Save your pivoted data to category_pivot. Remember to reset_index() at the end.
category_pivot = category_counts.pivot(columns='is_protected', index = 'category', values = 'scientific_name').reset_index()
#print(category_pivot)
#   is_protected           category  False  True
#   0                     Amphibian     72     7
#   1                          Bird    413    75
#   2                          Fish    115    11
#   3                        Mammal    146    30
#   4             Nonvascular Plant    328     5
#   5                       Reptile     73     5
#   6                Vascular Plant   4216    46

#Use the .columns property to rename the categories True and False to something more description:
#
#Leave category as category
#Rename False to not_protected
#Rename True to protected

category_pivot.columns = ['category', 'not_protected', 'protected']
#print(category_pivot)

#               category  not_protected  protected
#   0          Amphibian             72          7
#   1               Bird            413         75
#   2               Fish            115         11
#   3             Mammal            146         30
#   4  Nonvascular Plant            328          5
#   5            Reptile             73          5
#   6     Vascular Plant           4216         46

print("\nLet's create a new column of category_pivot called percent_protected") 
#which is equal to protected (the number of species that are protected) 
#divided by protected plus not_protected (the total number of species).

category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)
print(category_pivot)

#               category  not_protected  protected  percent_protected
#   0          Amphibian             72          7           0.088608
#   1               Bird            413         75           0.153689
#   2               Fish            115         11           0.087302
#   3             Mammal            146         30           0.170455
#   4  Nonvascular Plant            328          5           0.015015
#   5            Reptile             73          5           0.064103
#   6     Vascular Plant           4216         46           0.010793

print("\nIt looks like species in category Mammal are more likely to be endangered than species in Bird.\n \
We're going to do a significance test to see if this statement is true.") 
#Before you do the significance test, consider the following questions:
#
#Is the data numerical or categorical?
#How many pieces of data are you comparing?
#Based on those answers, you should choose to do a chi squared test. 
#In order to run a chi squared test, we'll need to create a contingency table. 
#Our contingency table should look like this:
#
#protected	not protected
#Mammal	?	?
#Bird	?	?
#Create a table called contingency and fill it in with the correct numbers

contingency_bird_mammal = [[30, 146],[75, 413]]

#Now run chi2_contingency with contingency.

#chi2_contingency(contingency)
print(chi2_contingency(contingency_bird_mammal))
#(0.1617014831654557, 0.6875948096661336, 1, array([[ 27.8313253, 148.1686747], [ 77.1686747, 410.8313253]]))
print("\nPVal is greater than .05, there is no significant difference between Bird and Mammal!\n")


contingency_reptile_mammal = [[30, 146],[5, 73]]
print(chi2_contingency(contingency_reptile_mammal))
#(4.289183096203645, 0.03835559022969898, 1, array([[ 24.2519685, 151.7480315],[ 10.7480315,  67.2519685]]))
print("\nPVal is less than .05, there is a significant difference between Reptile and Mammal!")

#---------------------------------------------------
############# STEP 5 ###############################
#---------------------------------------------------
currentStep += 1    
PrintStep(currentStep)

print("\nConservationists have been recording sightings of different species at several national parks for the past 7 days.")
#They've saved sent you their observations in a file called observations.csv. 
#Load observations.csv into a variable called observations, then use head to view the data.
observations = pd.read_csv('observations.csv')
observations.head()
print(observations.head(10))

#Some scientists are studying the number of sheep sightings at different national parks. 
#There are several different scientific names for different types of sheep.
#We'd like to know which rows of species are referring to sheep.

#Use apply and a lambda function to 
print("\nCreate a new column in species called is_sheep which is True if the common_names contains 'Sheep', and False otherwise")
species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
print(species.head())

#Select the rows of species where is_sheep is True and examine the results.
#print(species[species.is_sheep])

#Many of the results are actually plants. Select the rows of species where is_sheep is True and category is Mammal. 
#Save the results to the variable sheep_species.
sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]
#print(sheep_species)

#Now merge sheep_species with observations to get a DataFrame with observations of sheep.
#Save this DataFrame as sheep_observations.
sheep_observations = observations.merge(sheep_species)
#print(sheep_observations)

print("\nHow many total sheep observations (across all three species) were made at each national park?")
#Use groupby to get the sum of observations for each park_name. 
#Save your answer to obs_by_park.
#This is the total number of sheep observed in each park over the past 7 days.
obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
print(obs_by_park)

#Create a bar chart showing the different number of observations per week at each park.
#
#Start by creating a wide figure with figsize=(16, 4)
#Start by creating an axes object called ax using plt.subplot.
#Create a bar chart whose heights are equal to observations column of obs_by_park.
#Create an x-tick for each of the bars.
#Label each x-tick with the label from park_name in obs_by_park
#Label the y-axis Number of Observations
#Title the graph Observations of Sheep per Week
#Plot the graph using plt.show()

plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)),obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel("Number of Observations")
plt.title("Observations of Sheep per Week")
plt.show()

#Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.
print("\nPark rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.")
#The scientists want to test whether or not this program is working. 
#They want to be able to detect reductions of at least 5 percentage point. 
#For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
#
#Use the sample size calculator at Optimizely to calculate the number of sheep that they would need to observe from each park. 
#Use the default level of significance (90%).
#
#Remember that "Minimum Detectable Effect" is a percent of the baseline.

print("\nHow many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?")
print("How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?")

wks_at_bryce = 520 / 250.
wks_at_yellowstone = 520 / 507.

print("\nWeeks you need to observe at Bryce National Park:" + str(wks_at_bryce))
print("Weeks you need to observe at Yellowstone National Park:" + str(wks_at_yellowstone))