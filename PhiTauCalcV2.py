import sys
from pathlib import Path
sys.path.insert(0,str(Path().resolve())+'/packages')
from packages.gspread import authorize
from packages.oauth2client.service_account import ServiceAccountCredentials
import math
import time

#Getting input
Ft="hi"
while type(Ft)==str:
  Ft=input("What F(t) are you looking up for?\n")
  try:Ft=float(Ft)
  except:
    print("Please input a number for F(t).\n")

#Additonal Variables
output, FinalOutput, FtSection, UpperLimit, infiniteloop=["N/A","N/A","N/A","N/A","N/A","N/A"], "N/A", "N/A", "N/A", False

#Sheet Setup
scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Encryption_Key.json', scope)
client = authorize(creds)
sheet = client.open('Exponential Idle Average Tau*Phi (Created by Baldy)')
Equations_of_Doom, Error_Collection_PhiTau = sheet.get_worksheet(5), sheet.get_worksheet(7)

try:
  def PhiTauCalcu(Ft):
    output, FinalOutput, FtSection, UpperLimit, infiniteloop=["N/A","N/A","N/A","N/A","N/A","N/A"], "N/A", "N/A", "N/A", False
    def FtSection():
      if(6000>=Ft>5000): Section = 274
      elif(8000>=Ft>6000): Section = 300
      elif(9000>=Ft>8000): Section = 329
      elif(10000>=Ft>9000): Section = 352
      elif(11000>=Ft>10000): Section = 376
      elif(14000>=Ft>11000): Section = 401
      elif(16000>=Ft>14000): Section = 432
      elif(18000>=Ft>16000): Section = 464
      elif(48600>=Ft>18000): Section = 504
      elif(Ft>48600): Section = 136
      else: Section = 9
    
      return Section

    def PrePostCalc(PhiTau, Tau):
      if(Tau>PhiTau): 
        Output=[round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),1] #Tau higher error fix
      elif(Tau==0): 
        Output=[round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),False] #2k to 5k check
      else: 
        Output=[round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),round(10**(Tau-math.floor(Tau)),2), math.floor(Tau),round(10**(PhiTau-Tau-math.floor(PhiTau-Tau)),2), math.floor(PhiTau-Tau)] #5k+ Normal output
      
      return Output

    def Theories(Section, upper_limit):
      #Collecting Phi*Tau and Tau
      if(3800<=Ft<=upper_limit): #don't run if under 3800 because it will be caught 
        if(Ft<=4000):Equations_of_Doom.update_cell(Section, 4, 4000) #inputting to sheet
        else: Equations_of_Doom.update_cell(Section, 4, Ft) #inputting to sheet
        PhiTauCalc, TauCalc, attempts = False, False, 0
        while(PhiTauCalc==False and attempts <50):
            time.sleep(0.5) #check every 1 seconds to see if calculator finished as to not to lag out the api
            try:
                PhiTauCalc, TauCalc=float(Equations_of_Doom.cell(col=5, row=Section).value), float(Equations_of_Doom.cell(col=6, row=Section).value) #grabbing numbers
                Equations_of_Doom.update_cell(Section, 4, "awaiting input") #resetting input
                break
            except: 
              pass
              attempts += 1
        if(attempts>=50 and PhiTauCalc==False):
          Error_Collection_PhiTau.append_row(["Check Loop Timed Out", Ft, "N/A","N/A","N/A","N/A","N/A","N/A", "N/A", FtSection, UpperLimit])
          print("Potential infinite loop stopped.\nBug report has been sent for inspection. Status can be found here:\nhttps://bit.ly/3qOu0mn\n\nHere is the result anyways:\n\n")
          infiniteloop=True
          theoryput = False
        else:theoryput = PrePostCalc(PhiTauCalc, TauCalc)
      else:
        theoryput = [False, False, True]

      return theoryput

    #For Faster Calculations
    UpperLimit=int(Equations_of_Doom.cell(col=6, row=141).value)
    output = Theories(FtSection(), UpperLimit)
    try:
      if(infiniteloop == False and output != False):
        #Output Sorter      
        if(Ft<2000): FinalOutput=str("You need and are required to hit ee2000 with no Phi or Tau.") #Pre Grad Number
        elif(Ft<3800): FinalOutput=str("Second Graduation is ee3800 or ee4000. Please input a higher number.") #Pre Second Grad Number
        elif(Ft>UpperLimit): FinalOutput=str("F(t) is outside the range of equations.\nIf you have data to add please fill out: https://forms.gle/myog2rNgdmQJqPsP6\nCurrent Max F(t) Supported: ee")+str(UpperLimit) #Out of Range Check
        if(output[1]<0 and output[2]==False):
          Error_Collection_PhiTau.append_row(["Negative Result", Ft, output[0], output[1], output[2], "N/A","N/A","N/A", FinalOutput, FtSection, UpperLimit])
          print("An negative result occured.\nBug report has been sent for inspection. Status can be found here:\nhttps://bit.ly/3qOu0mn\n\nHere is the result anyways:\n\n")
        elif(output[1]>100 and output[2]==False): print(bounds_no_theories)
        elif(output[2]==False): FinalOutput=str("Estimated Phi for this F(t) is: ")+str(output[0])+str("e")+str(output[1]) #2k to 5k check
        if(output[2]!=True):
          if(output[4]==1):
            if(output[1]<0 or output[3]<0):
              Error_Collection_PhiTau.append_row(["Negative Result", Ft, output[0], output[1], output[2], output[3], output[4], output[5], FinalOutput, FtSection, UpperLimit])
              print("An negative result occured.\nBug report has been sent for inspection. Status can be found here:\nhttps://bit.ly/3qOu0mn\n\nHere is the result anyways:\n\n")
            elif(output[0]<1 or output[1]>8000 or output[2]<1 or output[3]>6000): print(bounds_theories_tau_fix)
            else: FinalOutput=str("Estimated Phi*Tau for this F(t) is: ")+str(output[0])+str("e")+str(output[1])+str("\nEstimated Tau for this F(t) is: ")+str(output[2])+str("e")+str(output[3])+str("\nEstimated Phi for this F(t) is: ")+str(output[4]) #Phi=1 check
          else:
            if(output[1]<0 or output[3]<0 or output[5]<0):
              Error_Collection_PhiTau.append_row(["Negative Result", Ft, output[0], output[1], output[2], output[3], output[4], output[5], FinalOutput, FtSection, UpperLimit])
              print("An negative result occured.\nBug report has been sent for inspection. Status can be found here:\nhttps://bit.ly/3qOu0mn\n\nHere is the result anyways:\n\n")
            elif(output[0]<1 or output[1]>9000 or output[2]<1 or output[3]>6500 or output[4]<1 or output[5]>3000): print(bounds_theories)
            else: FinalOutput=str("Estimated Phi*Tau for this F(t) is: ")+str(output[0])+str("e")+str(output[1])+str("\nEstimated Tau for this F(t) is: ")+str(output[2])+str("e")+str(output[3])+str("\nEstimated Phi for this F(t) is: ")+str(output[4])+str("e")+str(output[5]) #normal output
        elif(FinalOutput == "N/A"):FinalOutput="HOW??????"
      else:FinalOutput = error_message

      return(FinalOutput)
    except Exception as err:
      pass
      Error_Collection_PhiTau.append_row([str(err), Ft, output[0], output[1], output[2], output[3], output[4], output[5], FinalOutput, FtSection, UpperLimit])
      if(infiniteloop==True):print("An error with the result occured as well.\nBug report has been sent for inspection again.")
      else:print("An error occured.\nBug report has been sent for inspection. Status can be found here:\nhttps://bit.ly/3qOu0mn")
  PhiTauput=PhiTauCalcu(Ft)
  if(type(PhiTauput)==None):
    Error_Collection_PhiTau.append_row([str(err), Ft, output[0], output[1], output[2], output[3], output[4], output[5], FinalOutput, FtSection, UpperLimit])
    if(infiniteloop==True):print("An error with the result occured as well.\nBug report has been sent for inspection again.")
    else:print("An error occured.\nBug report has been sent for inspection. Status can be found here:\nhttps://bit.ly/3qOu0mn")
  else:print("\n"+str(PhiTauput))

except Exception as err:
  pass
  Error_Collection_PhiTau.append_row([str(err), Ft, output[0], output[1], output[2], output[3], output[4], output[5], FinalOutput, FtSection, UpperLimit])
  print("An error occured.\nBug report has been sent for inspection. Status can be found here:\nhttps://bit.ly/3qOu0mn")