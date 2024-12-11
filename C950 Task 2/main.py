#Student ID: 012255895
#Student name: David Hernandez
###############
###############
#A. Develop hash table, without using...
# Source: WGU's "C950-Webinar-1-Let's Go Hashing"
###############
###############

import csv
from datetime import datetime, timedelta
from fileinput import close



# HashTable class using chaining.
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=39):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])

class Package:
    def __init__(self, packageID, packageAddress, packageCity, packageZip,
                 packageDeadline, packageWeight, packageStatus, packageDeliveryTime):
        self.packageID = packageID
        self.packageAddress = packageAddress
        self.packageCity = packageCity
        self.packageZip = packageZip
        self.packageDeadline = packageDeadline
        self.packageWeight = packageWeight
        self.packageStatus = packageStatus
        self.packageDeliveryTime = packageDeliveryTime
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
            self.packageID, self.packageAddress, self.packageCity,
            self.packageZip, self.packageDeadline, self.packageWeight,
            self.packageStatus, self.packageDeliveryTime)


def loadPackageData(fileName):
    with open(fileName) as packageInfo:
        packageData = csv.reader(packageInfo, delimiter=',')
        for truckPackage in packageData:
            pID = int(truckPackage[0])
            pAddress = truckPackage[1]
            pCity = truckPackage[2]
            pZip = truckPackage[3]
            pDeadline = truckPackage[4]
            pWeight = truckPackage[5]
            pStatus = "at the hub"
            pDeliveryTime = None
            packageObject = Package(pID, pAddress, pCity, pZip, pDeadline, pWeight, pStatus, pDeliveryTime)
            # Insert it into the hash table
            myHash.insert(pID, packageObject)

# Hash table instance
myHash = ChainingHashTable()

# Load packages into Hash Table
loadPackageData('packageInformation.csv')


# Fetch data from Hash Table
#for i in range (len(myHash.table)+1):
 #   print("Key: {} and Package: {}".format(i + 1, myHash.search(i+1)))

# Define distance data list
distanceDataList = []

# Define function to load csv file into distanceDataList
def loadDistanceData(distanceFile):
    with open(distanceFile) as distanceInfo:
        distanceData = csv.reader(distanceInfo)
        for distance in distanceData:
            distanceDataList.append(distance)

# Call the function with the csv file as the parameter
loadDistanceData('distance.csv')
#-----------------------------------------------------------------------
# Define address data list
addressDataList = []

# Define function to load csv file into addressDataList
def loadAddressData(addressFile):
    with open(addressFile) as addressInfo:
        addressData = csv.reader(addressInfo, delimiter=',')
        for address in addressData:
            addressDataList.append(address[0])


# Call the function with the csv as the parameter
loadAddressData('address.csv')

###############
###############
#B. Develop a look-up function...
###############
###############

def packageLookUp(packageID):
    return (myHash.search(packageID))


###############
# Functions to calculate distance between two addresses and find package with the nearest address
# from our current address
###############

# Function to return distance between two addresses
def distanceBetween(address1, address2):
    indexAddress1 = addressDataList.index(address1)
    indexAddress2 = addressDataList.index(address2)
    if indexAddress1 >= indexAddress2:
        distanceBetweenAddresses = (distanceDataList[indexAddress1][indexAddress2])
        return distanceBetweenAddresses
    elif indexAddress2 > indexAddress1:
        distanceBetweenAddresses = (distanceDataList[indexAddress2][indexAddress1])
        return distanceBetweenAddresses

# Function to find package with the nearest address
def minDistanceFrom(fromAddress, truckObject):
    # Large arbitrary number
    minDistanceAddress = 1000.00
    nearestPackage = None
    # Loop through the packages in the array
    for package in truckObject.listOfPackages:
        # if addresses are the same, set the nearestPackage object to the package object
        if package.packageAddress == fromAddress:
            nearestPackage = package
        # Skip this iteration to compare this same address to all other addresses
            continue

        # Find distance between the currentDistance and all package addresses
        distanceAddress = float(distanceBetween(fromAddress, package.packageAddress))
    # Conditional to check if the package address is less than minDistanceAddress
        if distanceAddress <= minDistanceAddress:
            minDistanceAddress = distanceAddress
            nearestPackage = package
    # return nearest package object as it'll be easier to access/update object attributes later
    return nearestPackage

###############
###############
#C. Write an original program that will deliver all the packages...
###############
###############

# Create Truck class with following parameters
class Truck:
    def __init__(self, name):
        self.name = name
        self.listOfPackages = []


# Defining function to load trucks
def truckLoadPackages(truckObject, packageObject):
    # Checks to see if package limit has been met
    if len(truckObject.listOfPackages) < 16:
        # Append package objects into listOfPackages
        truckObject.listOfPackages.append(packageObject)
    else:
        print("Can't hold anymore!")

# Create truck objects
truck1 = Truck("truck1")
truck2 = Truck("truck2")
truck3 = Truck("truck3")

# Load packages into truck1
truckLoadPackages(truck1, packageLookUp(4))
truckLoadPackages(truck1, packageLookUp(13))
truckLoadPackages(truck1, packageLookUp(39))
truckLoadPackages(truck1, packageLookUp(14))
truckLoadPackages(truck1, packageLookUp(15))
truckLoadPackages(truck1, packageLookUp(16))
truckLoadPackages(truck1, packageLookUp(34))
truckLoadPackages(truck1, packageLookUp(19))
truckLoadPackages(truck1, packageLookUp(20))
truckLoadPackages(truck1, packageLookUp(21))
truckLoadPackages(truck1, packageLookUp(27))
truckLoadPackages(truck1, packageLookUp(35))
truckLoadPackages(truck1, packageLookUp(40))

# Load packages into truck2
truckLoadPackages(truck2, packageLookUp(1))
truckLoadPackages(truck2, packageLookUp(2))
truckLoadPackages(truck2, packageLookUp(33))
truckLoadPackages(truck2, packageLookUp(3))
truckLoadPackages(truck2, packageLookUp(18))
truckLoadPackages(truck2, packageLookUp(22))
truckLoadPackages(truck2, packageLookUp(23))
truckLoadPackages(truck2, packageLookUp(24))
truckLoadPackages(truck2, packageLookUp(7))
truckLoadPackages(truck2, packageLookUp(29))
truckLoadPackages(truck2, packageLookUp(8))
truckLoadPackages(truck2, packageLookUp(30))
truckLoadPackages(truck2, packageLookUp(36))
truckLoadPackages(truck2, packageLookUp(37))
truckLoadPackages(truck2, packageLookUp(38))

# Load packages into truck3
truckLoadPackages(truck3, packageLookUp(5))
truckLoadPackages(truck3, packageLookUp(6))
truckLoadPackages(truck3, packageLookUp(9))
truckLoadPackages(truck3, packageLookUp(10))
truckLoadPackages(truck3, packageLookUp(11))
truckLoadPackages(truck3, packageLookUp(12))
truckLoadPackages(truck3, packageLookUp(17))
truckLoadPackages(truck3, packageLookUp(25))
truckLoadPackages(truck3, packageLookUp(26))
truckLoadPackages(truck3, packageLookUp(28))
truckLoadPackages(truck3, packageLookUp(31))
truckLoadPackages(truck3, packageLookUp(32))

# Function to deliver packages
def deliverTruckPackages(truckObject, startTime):
    totalDistanceTraveled = 0.0
    currentAddress = "HUB"
    currentTime = datetime.strptime(startTime, "%H:%M:%S")

    while truckObject.listOfPackages:
        # Check each package object in truckObject.listOfPackages for package 9
        for package9 in truckObject.listOfPackages:
            # If package 9 is present in the list, update the address after 10:20:00
            if package9.packageID == 9 and currentTime.time() >= datetime.strptime("10:20:00", "%H:%M:%S").time():
                package9.packageAddress = "410 S State St"
                # Update the hash table with the corrected package 9 object
                myHash.insert(9, package9)

        # Starts with getting package object closest to the HUB
        nearestPackage = minDistanceFrom(currentAddress, truckObject)
        # Get address from nearestPackage object
        nearestAddress = nearestPackage.packageAddress

        # If the addresses are the same, put them in this list to be delivered
        # This also handles multiple packages that have the same address
        packagesAtSameAddress = [
            package for package in truckObject.listOfPackages
            if package.packageAddress == nearestAddress
        ]

        # If the two packages do not share the same address
        # The goal here is to travel to the nearestAddress and keep track of time and distance traveled
        if nearestAddress != currentAddress:
            # Get distance between current and nearest addresses
            distanceTraveled = float(distanceBetween(currentAddress, nearestAddress))
            # Get time by dividing distance by speed of truck
            timeToDeliver = distanceTraveled/18
            # Get the change in time
            changeInTime = timedelta(hours=timeToDeliver)

            # Add distanceTraveled to the total distance
            totalDistanceTraveled += distanceTraveled
            # Set currentAddress to nearestAddress to go to nearestAddress
            currentAddress = nearestAddress
            # Add changeInTime to currentTime to start the next delivery at this time
            currentTime += changeInTime

        # Delivers the package after the truck travels to the nearestAddress
        # Delivers packages together if they have the same address
        for package in packagesAtSameAddress:
            # Mark each package object at the same address as delivered and update delivery time
            package.packageStatus = "delivered by " + truckObject.name
            package.packageDeliveryTime = currentTime.strftime("%H:%M:%S")
            # Update hash table
            myHash.insert(package.packageID, package)
            # Remove package from truck list as it was delivered and prevent infinite loop
            truckObject.listOfPackages.remove(package)
            # Then it loops again with the nearest address

    # return distance traveled by this particular truck object
    # this makes calculating total distance traveled by 3 trucks easier
    return totalDistanceTraveled

# Travel to hub from the address of the last package
truck1LastAddressToHub = distanceBetween("2010 W 500 S", "HUB")
timeToReturnToHub = float(truck1LastAddressToHub)/18

# Time it takes to arrive at hub
changeInTime = timedelta(hours=timeToReturnToHub)

# Add changeInTime to the time of the last delivery for truck1
# This is the start time of truck 3 since the driver returned the hub for other packages
newTime = (datetime.strptime("08:59:00", "%H:%M:%S") + changeInTime).time()

# Add distances of deliveries and the distance from the last address back to the hub
truck1Distance = deliverTruckPackages(truck1, "08:00:00") + float(truck1LastAddressToHub)
truck2Distance = deliverTruckPackages(truck2,"08:00:00")
truck3Distance = deliverTruckPackages(truck3, str(newTime))
totalTruckDistance = truck1Distance + truck2Distance + truck3Distance
#print(totalTruckDistance)


###############
# Functions for the UI
###############

def printAllStatusAndMileage():
    for i in range (1, 41):
        print(myHash.search(i))
    print("")
    print("Distance traveled by truck1:", truck1Distance)
    print("Distance traveled by truck2:", truck2Distance)
    print("Distance traveled by truck3:", truck3Distance)
    print("Total distance traveled by the three trucks: ", totalTruckDistance)
    print("")

def printPackagesGivenTime(userTime):
    userTime = datetime.strptime(userTime, "%H:%M:%S").time()

    truck1Packages = []
    truck2Packages = []
    truck3Packages = []

    for i in range(1, 41):
        package = myHash.search(i)
        package.packageDeliveryTime = datetime.strptime(package.packageDeliveryTime, "%H:%M:%S").time()

        if package.packageID == 9 and userTime >= datetime.strptime("10:20:00", "%H:%M:%S").time():
            package.packageAddress = "410 S State St"
        else:
            package.packageAddress = "300 State St"

        # if time is greater than delivery time, it prints time of delivery
        if package.packageDeliveryTime <= userTime:
            print("Package ID", package.packageID, ":", package.packageStatus, " at ", package.packageDeliveryTime)
            print("Full package information:", "Package ID:", package.packageID,",", "Address:", package.packageAddress,",", "City:", package.packageCity,",", "Zip:", package.packageZip,",", "Deadline:", package.packageDeadline,",", "Weight:", package.packageWeight)
            print("")
        elif (package.packageDeliveryTime > userTime) and userTime < datetime.strptime("08:00:00", "%H:%M:%S").time() and (package.packageStatus == "delivered by truck1" or package.packageStatus == "delivered by truck2" or package.packageStatus == "delivered by truck3"):
            print("Package ID", package.packageID, ": is at the hub and will soon be en route")
            print("Full package information:", "Package ID:", package.packageID,",", "Address:", package.packageAddress,",", "City:", package.packageCity,",", "Zip:", package.packageZip,",", "Deadline:", package.packageDeadline,",", "Weight:", package.packageWeight)
            print("")
        # prints truck3 at hub since truck1 hasn't made it back to the hub
        elif package.packageDeliveryTime > userTime and userTime < datetime.strptime("09:14:00", "%H:%M:%S").time() and package.packageStatus == "delivered by truck3":
            print("Package ID", package.packageID, ": is at the hub and will soon be en route by truck3")
            print("Full package information:", "Package ID:", package.packageID,",", "Address:", package.packageAddress,",", "City:", package.packageCity,",", "Zip:", package.packageZip,",", "Deadline:", package.packageDeadline,",", "Weight:", package.packageWeight)
            print("")
        # prints if packageDeliveryTime is greater than userTime. If so, en route
        elif package.packageDeliveryTime > userTime and package.packageStatus == "delivered by truck1":
            print("Package ID", package.packageID, ": is en route by truck1")
            print("Full package information:", "Package ID:", package.packageID,",", "Address:", package.packageAddress,",", "City:", package.packageCity,",", "Zip:", package.packageZip,",", "Deadline:", package.packageDeadline,",", "Weight:", package.packageWeight)
            print("")
        elif package.packageDeliveryTime > userTime and package.packageStatus == "delivered by truck2":
            print("Package ID", package.packageID, ": is en route by truck2")
            print("Full package information:", "Package ID:", package.packageID,",", "Address:", package.packageAddress,",", "City:", package.packageCity,",", "Zip:", package.packageZip,",", "Deadline:", package.packageDeadline,",", "Weight:", package.packageWeight)
            print("")
        elif package.packageDeliveryTime > userTime and package.packageStatus == "delivered by truck3":
            print("Package ID", package.packageID, ": is en route by truck3")
            print("Full package information:", "Package ID:", package.packageID,",", "Address:", package.packageAddress,",", "City:", package.packageCity,",", "Zip:", package.packageZip,",", "Deadline:", package.packageDeadline,",", "Weight:", package.packageWeight)
            print("")
#printAllStatusAndMileage()
#printObjectStatus(23)

#printPackagesGivenTime("09:00:00")

#printPackagesGivenTime("10:00:00")

#printPackagesGivenTime("12:30:00")

#printAllStatusAndMileage()

###############
###############
#D. Provide an intuitive interface for the user...
###############
###############

print("Welcome to the Western Governors University Parcel Service (WGUPS)")
print("Please select one of the following options")
print("1 - Display all package information and total distance traveled by all three trucks")
print("2 - Display all package information at a certain time")
print("3 - Exit")

userInput = input('Enter value:')
userInput = int(userInput)
if userInput != 1 and userInput != 2 and userInput != 3:
    print("Invalid input")
elif userInput == 1:
    printAllStatusAndMileage()
elif userInput == 2:
    userTimeInput = input('Please provide time (HH:MM:SS):')
    printPackagesGivenTime(userTimeInput)
elif userInput == 3:
    exit()
