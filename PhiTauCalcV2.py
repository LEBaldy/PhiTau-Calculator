import gspread
from oauth2client.service_account import ServiceAccountCredentials
import math
import time

#Getting input
Ft="hi"
while type(Ft)==str:
  Ft=input("What F(t) are you looking up for?\n(only number after ee or log10(log10(F(t))))\n")
  if(Ft.isdigit()): Ft=int(Ft)
  else: 
    print("Please input an integer for F(t).")
    Ft="Fail"

#Sheet Setup
scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Encryption_Key.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Exponential Idle Average Phi (Created by Baldy)')
Equations_of_Doom, Other_Data = sheet.get_worksheet(7), sheet.get_worksheet(8)

def FtSection():
    if(Ft>5000):
        if(Ft>11000):
            if(Ft>int(Other_Data.cell(col=17, row=3).value)): Section=144 #Max Psi 3 Check
            elif(Ft>=14000): Section=247 #R9 to Psi 3
            else: Section=243 #11k to R9
        else: Section=216 #5k to 11k
    else: Section=12 #2k to 5k
    
    return Section

def PrePostCalc(PhiTau, Tau):
    if(Tau>PhiTau): Output=[round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),1] #Tau higher error fix
    elif(Tau==0): Output=[round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),False] #2k to 5k check
    else: Output=[round(10**(PhiTau-math.floor(PhiTau)),2), math.floor(PhiTau),round(10**(Tau-math.floor(Tau)),2), math.floor(Tau),round(10**(PhiTau-Tau-math.floor(PhiTau-Tau)),2), math.floor(PhiTau-Tau)] #5k+ Normal output
    
    return Output

def Theories(Section):
    #Collecting Phi*Tau and Tau
    Equations_of_Doom.update_cell(Section, 4, Ft) #inputting to sheet
    PhiTauCalc, TauCalc=False, False
    while(PhiTauCalc==False):
        time.sleep(0.5) #check every 1 seconds to see if calculator finished as to not to lag out the api
        try:
            PhiTauCalc, TauCalc=float(Equations_of_Doom.cell(col=5, row=Section).value), float(Equations_of_Doom.cell(col=6, row=Section).value) #grabbing numbers
            Equations_of_Doom.update_cell(Section, 4, "awaiting input") #resetting input
            break
        except: continue
    
    return PrePostCalc(PhiTauCalc, TauCalc)

output, UpperLimit=Theories(FtSection()), int(Other_Data.cell(col=17, row=4).value) #For Faster Calculations
#The Actual Output Sorter         
if(Ft<2000): print("You need and are required to hit ee2000 with no Phi or Tau.") #Pre Grad Number
if(Ft<3800): print("Second Graduation is ee3800 or ee4000. Please input a higher number.") #Pre Second Grad Number
elif(Ft>UpperLimit): print("F(t) is outside the range of equations.\nIf you have data to add please fill out: https://forms.gle/myog2rNgdmQJqPsP6\nCurrent Max F(t) Supported: ee", UpperLimit) #Out of Range Check
elif(output[2]==False): print("Estimated Phi for this F(t) is: ",output[0],"e", output[1]) #2k to 5k check
elif(output[4]==1): print("Estimated Phi*Tau for this F(t) is: ", output[0],"e", output[1],"\nEstimated Tau for this F(t) is: ", output[2],"e", output[3],"\nEstimated Phi for this F(t) is: ", output[4]) #Phi=1 check
else: print("Estimated Phi*Tau for this F(t) is: ", output[0],"e", output[1],"\nEstimated Tau for this F(t) is: ", output[2],"e", output[3],"\nEstimated Phi for this F(t) is: ", output[4],"e", output[5]) #normal output
