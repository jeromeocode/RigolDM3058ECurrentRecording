#this script just takes current data from the RIGOL DM3058E over an allotted time
import visa
import time
import csv
from visa import constants


#modify test time in seconds
testTime = 90*60

#setting up dmm conection
rm = visa.ResourceManager()

#you can receive the instrument's ID if you use print(rm.list_resources())
print(rm.list_resources())

#wait for keypress to start the timer
start = input("Enter a key to start the program")

# dmm = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R194201991::INSTR') #TODO: Figure this out
dmm = rm.open_resource('GPIB1::5::INSTR')

#timed loop
timeEnd = time.time() + testTime

print('Experiment has started. DO NOT CLOSE THIS WINDOW.')

count = 0
psVoltage = 0
psCurrent = 0

timeStart = time.time()
#writes data in a csv
with open('results_1.csv', 'w', newline='') as csvfile:
  fields = ['time', 'voltage', 'current']
  writer = csv.DictWriter(csvfile, fieldnames=fields)

  #outputs headers
  writer.writeheader()

  #loops until time runs out
  while True:
    currTime = float(time.time())
    psVoltage = float(dmm.query(":MEASure:VOLTage:DC?"))
    psCurrent = float(dmm.query(":MEASure:CURRent:DC?"))

    writer.writerow({'time': currTime, 'voltage': psVoltage, 'current': psCurrent})

    #console printouts so that the user has a visible timer
    print(time.time())
    print(count)
    print(psVoltage)
    print(psCurrent)
    count = count+1
    csvfile.flush()
    time.sleep(1)