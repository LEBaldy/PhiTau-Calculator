import sys
from pathlib import Path
sys.path.insert(0,str(Path().resolve())+'/packages')
from packages.gspread import authorize
from packages.oauth2client.service_account import ServiceAccountCredentials
import math
import time
from datetime import datetime


#Getting input
Ft="hi"
print("Input number after ee only")
while type(Ft)==str:
  Ft=input("What F(t) are you looking up for?\n")
  try:Ft=float(Ft)
  except:
    print("Please input a number for F(t).\n")

#Additonal Variables
output, FinalOutput, UpperLimit, infiniteloop, sectiondict=["N/A","N/A","N/A","N/A","N/A","N/A"], "N/A", "N/A", False, {(5000,6000):274,(6000,8000):300,(8000,9000):329,(9000,10000):352,(10000,11000):376,(11000,14000):401,(14000,16000):432,(16000,18000):464,(18000,48600):504,(48600,math.inf):136,(-math.inf,5000):9}
try:
  #Sheet Setup
  scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_name('Encryption_Key.json', scope)
  client = authorize(creds)
  phitausheet, phitaudatasheet = client.open('Exponential Idle Average Tau*Phi (Created by Baldy)'), client.open('Exponential Idle Phi*Tau Data Collection (Created by Baldy)')
  Equations_of_Doom, Error_Collection_PhiTau, Data_Collection_PhiTau = phitausheet.get_worksheet(2), phitaudatasheet.get_worksheet(6), phitaudatasheet.get_worksheet(4)
except Exception as err:
  print("An error occured contacting the calculation sheet. Please contact Baldy about this. It may be due to too much traffic so try again in 10-20minutes.")
  print("\nExact Error:\n"+str(err))
try:
  def PhiTauCalcu(Ft):
    global output
    global FinalOutput
    global UpperLimit
    global infiniteloop
    def FtSection():
      for (lower, upper), section in sectiondict.items():
        if upper >= Ft > lower:return section
    def PrePostCalc(PhiTau, Tau, Phi=0):
      if(Tau>PhiTau):Output=[round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),1,0] #Tau higher error fix
      elif(Ft<=5000):
        if 5000>=Ft>4800:Output=[round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau), False, round(10**(Phi-math.floor(Phi)),2), math.floor(Phi)] #2k to 5k check
        else:Output=[round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau), False, False] #2k to 5k check
      else:Output=[round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),round(10**(Tau-math.floor(Tau)),2), math.floor(Tau),round(10**(PhiTau-Tau-math.floor(PhiTau-Tau)),2), math.floor(PhiTau-Tau)] #5k+ Normal output
      return Output

    def Theories(Section, upper_limit):
      #Collecting Phi*Tau and Tau
      if(3800<=Ft<=upper_limit): #don't run if under 3800 because it will be caught 
        if(Ft<=4000):Equations_of_Doom.update_cell(Section, 4, 4000) #inputting to sheet
        else: Equations_of_Doom.update_cell(Section, 4, Ft) #inputting to sheet
        PhiTauCalc, TauCalc, attempts, time_start, time_current = False, False, 0, time.time(), 0
        while(PhiTauCalc==False and attempts <50 and time_current <=120):
            time.sleep(0.5) #check every 1 seconds to see if calculator finished as to not to lag out the api
            try:
                PhiTauCalc, TauCalc=float(Equations_of_Doom.cell(col=5, row=Section).value), float(Equations_of_Doom.cell(col=6, row=Section).value) #grabbing numbers
                if(5000>=Ft>4800):PhiTauCalc_2 = float(Equations_of_Doom.cell(col=7, row=9).value)
                Equations_of_Doom.update_cell(Section, 4, "awaiting input") #resetting input
                break
            except: 
              pass
              attempts += 1
              time_current=time.time()-time_start
        if((attempts>=50 or time_current>120) and PhiTauCalc==False):
          Error_Collection_PhiTau.append_row(["Check Loop Timed Out", Ft, "N/A","N/A","N/A","N/A","N/A","N/A", "N/A", Section, upper_limit, datetime.now().strftime('%Y/%m/%d %H:%M:%S'), False])
          print("Potential infinite loop stopped.\nBug report has been sent for inspection.\n\n")
          infiniteloop=True
          theoryput = [False]
        elif 5000>=Ft>4800:theoryput = PrePostCalc(PhiTauCalc, TauCalc, PhiTauCalc_2)
        else:theoryput = PrePostCalc(PhiTauCalc, TauCalc)
      else:theoryput = [False, False, True]
      return theoryput

    #For Faster Calculations
    UpperLimit=int(Equations_of_Doom.cell(col=6, row=141).value)
    if(Ft<3800 or Ft>UpperLimit):
        if(Ft<2000): 
          FinalOutput=str("You need and are required to hit ee2000 with no Phi or Tau.") #Pre Grad Number
        elif(Ft<3800): 
          FinalOutput=str("Second Graduation is ee3800 or ee4000. Please input a higher number.") #Pre Second Grad Number
        elif(Ft>UpperLimit): 
          FinalOutput=str("F(t) is outside the range of equations.\nIf you have data to add please fill out: https://forms.gle/myog2rNgdmQJqPsP6\nCurrent Max F(t) Supported: ee")+str(UpperLimit) #Out of Range Check
    else:
      try:
        output = Theories(FtSection(), UpperLimit)
        if(infiniteloop == False and output[0] != False):
          #Output Sorter
          if(type(output[2]) is bool):
            if(output[2]==False):
              if(output[1]<0):
                Error_Collection_PhiTau.append_row(["Negative Result", Ft, output[0], output[1], output[2], "N/A","N/A","N/A", FinalOutput, FtSection(), UpperLimit, datetime.now().strftime('%Y/%m/%d %H:%M:%S'), False])
                print("An negative result occured.\nBug report has been sent for inspection.\n\nHere is the result anyways:\n\n")
              elif(output[1]>100): 
                Error_Collection_PhiTau.append_row(["Theories_No_Bounds", Ft, output[0], output[1], output[2], "N/A","N/A","N/A", FinalOutput, FtSection(), UpperLimit, datetime.now().strftime('%Y/%m/%d %H:%M:%S'), False])
                print("An error with the result occured as well.\nBug report has been sent for inspection again.")
              elif output[3]==False:FinalOutput=str("Estimated Phi for this F(t) is: ")+str(output[0])+str("e")+str(output[1]) #2k to 5k check
              else:FinalOutput="ee4.6k Route -- Estimated Phi for this F(t) is: "+str(output[0])+"e"+str(output[1])+"\nee4.8k Route -- Estimated Phi for this F(t) is: "+str(output[3])+"e"+str(output[4]) #2k to 5k check
            else:
              FinalOutput="You have triggered the \"Baldy is a fuck-up Switch\".\nBaldy has been send his punishment."
              Error_Collection_PhiTau.append_row(["Negative Result", Ft, output[0], output[1], output[2], output[3], output[4], output[5], FinalOutput, FtSection(), UpperLimit, datetime.now().strftime('%Y/%m/%d %H:%M:%S'), False])
          else:
            if(output[1]<0 or output[3]<0 or output[5]<0):
              Error_Collection_PhiTau.append_row(["Negative Result", Ft, output[0], output[1], output[2], output[3], output[4], output[5], FinalOutput, FtSection(), UpperLimit, datetime.now().strftime('%Y/%m/%d %H:%M:%S'), False])
              print("An negative result occured.\nBug report has been sent for inspection.\n\nHere is the result anyways:\n\n")
            elif(output[0]<1 or output[1]>9000 or output[2]<1 or output[3]>6500 or output[4]<1 or output[5]>3000): print(bounds_theories)
            elif(output[5]==0): FinalOutput=str("Estimated Phi*Tau for this F(t) is: ")+str(output[0])+str("e")+str(output[1])+str("\nEstimated Tau for this F(t) is: ")+str(output[2])+str("e")+str(output[3])+str("\nEstimated Phi for this F(t) is: ")+str(output[4]) #phi=1 check
            else:FinalOutput=str("Estimated Phi*Tau for this F(t) is: ")+str(output[0])+str("e")+str(output[1])+str("\nEstimated Tau for this F(t) is: ")+str(output[2])+str("e")+str(output[3])+str("\nEstimated Phi for this F(t) is: ")+str(output[4])+str("e")+str(output[5]) #normal output
        else: FinalOutput = error_message
      except Exception as err:
        pass
        Error_Collection_PhiTau.append_row([str(err), Ft, output[0], output[1], output[2], output[3], output[4], output[5], FinalOutput, FtSection(), UpperLimit, datetime.now().strftime('%Y/%m/%d %H:%M:%S'), False])
        if(infiniteloop==True):print("An error with the result occured as well.\nBug report has been sent for inspection again.")
        else:print("An error occured.\nBug report has been sent for inspection.")
    return (FinalOutput)
  PhiTauput=PhiTauCalcu(Ft)
  if(type(PhiTauput)==None):
    Error_Collection_PhiTau.append_row([str(err), Ft, output[0], output[1], output[2], output[3], output[4], output[5], "outside", "outside", "outside", datetime.now().strftime('%Y/%m/%d %H:%M:%S'), False])
    print("An error occured.\nBug report has been sent for inspection.")
  elif PhiTauput == "Timed out":print("\n")
  else:
    print("\n"+str(PhiTauput)+"\n")
    Data_Collection_PhiTau.append_row([Ft, PhiTauput, datetime.now().strftime('%Y/%m/%d %H:%M:%S')])
except Exception as err:
  pass
  Error_Collection_PhiTau.append_row([str(err), Ft, output[0], output[1], output[2], output[3], output[4], output[5], "full outside", "full outside", "full outside", datetime.now().strftime('%Y/%m/%d %H:%M:%S'), False])
  print("An error occured.\nBug report has been sent for inspection.")