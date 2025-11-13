# ---------------------------------------------------------------------------------------------------------------------
# Text printing function library
# ---------------------------------------------------------------------------------------------------------------------

# GetConsoleWidth()                                             # Gets actual width of console (9999 if console is redirected)
# SetSilentMode(Enabled)                                        # Set silent mode
# FormatParagraph(Str,Width,Indentation=0)                      # Formats long string as wrapped paragraph with indentation
# Print(Text,Wheel=False,Volatile=False,Partial=False,Class="") # Print messages on screen
# PrintTable(Heading1,Heading2,ColAttributes,Rows,MaxWidth)     # Print formatted table on screen

# ---------------------------------------------------------------------------------------------------------------------
# Import libraries
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import sys

# ---------------------------------------------------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------------------------------------------------
SEPARATOR_ID="$SEP$"
TABLE_HLINE=[SEPARATOR_ID]
WHEEL_CHARS=['-','\\','|','/']

# ---------------------------------------------------------------------------------------------------------------------
# Global variablees
# ---------------------------------------------------------------------------------------------------------------------
_MessageCnt=0
_LastText=""
_LastVolatile=False  
_SilentMode=False

# ---------------------------------------------------------------------------------------------------------------------
# Get console width
# ---------------------------------------------------------------------------------------------------------------------
def GetConsoleWidth():
  if(sys.stdout.isatty()):
    Console=os.get_terminal_size()
    ConsoleWidth=Console.columns-1
  else:
    ConsoleWidth=9999
  return ConsoleWidth

# ---------------------------------------------------------------------------------------------------------------------
# Set silent mode
# ---------------------------------------------------------------------------------------------------------------------
def SetSilentMode(Enabled):
  global _SilentMode
  _SilentMode=Enabled

# ----------------------------------------------------------------------------------
# Format paragraphn
# ----------------------------------------------------------------------------------
def FormatParagraph(Str,Width,Indentation=0):
  WorkStr=Str
  WorkStr=WorkStr.replace("\n"," ").replace("\r","").replace("\t"," ")
  while WorkStr.find("  ")!=-1:
    WorkStr=WorkStr.replace("  "," ")
  Words=WorkStr.split(" ")
  OutLines=[]
  Line=""
  for Word in Words:
    if len(Line+Word)<=Width:
      Line+=Word+" "
    else:
      OutLines.append(Line)
      Line=" "*Indentation+Word+" "
  if len(Line)!=0:
    OutLines.append(Line)
  Output="\n".join(OutLines)
  return Output

# ---------------------------------------------------------------------------------------------------------------------
# Print message
# ---------------------------------------------------------------------------------------------------------------------
def Print(Text,Wheel=False,Volatile=False,Partial=False,Class=""):
  
  #Declare global variables
  global _LastText
  global _LastVolatile
  global _SilentMode
  global _MessageCnt
  
  #Do nothing on silent mode
  if _SilentMode==True:
    return
  
  #Initializations
  ConsoleWidth=GetConsoleWidth()
  OutText=Text
  File=sys.stdout
  
  #Switch to stderr for errors
  if Class.upper() in ["ERR","ERROR","FAIL","FAILURE"]:
    File=sys.stderr
  
  #Apply wheel
  if Wheel==True: 
    OutText="["+WHEEL_CHARS[_MessageCnt%4]+"] "+OutText
    _MessageCnt+=1
  
  #Apply class
  if len(Class)!=0:
    OutText="["+Class.upper()+"] "+OutText
  
  #Clean last output of last message was volatile
  if _LastVolatile==True:
    print("\r",end="",flush=True,file=File)
    print(" "*len(_LastText),end="\r",flush=True,file=File)
  
  #Output message
  if Volatile==True or Partial==True:
    OutText=OutText[:ConsoleWidth-2]
    print(OutText,end="",flush=True,file=File)
  else:
    print(OutText,file=File)
  
  #Save output
  _LastText=OutText
  _LastVolatile=Volatile

#----------------------------------------------------------------------------------------------------------------------
# PrintTable
#----------------------------------------------------------------------------------------------------------------------
def PrintTable(Heading1,Heading2,ColAttributes,Rows):
  
  #Modified length function that takes into acccount escape sequences that do not count for printed length on the screen
  def Length(Str):
    Match=re.search(r"\x1b\]8;;(.*?)\x1b\\(.*?)\x1b\]8;;\x1b\\",Str)
    if Match!=None:
      _,Name=Match.groups()
      return len(Name)
    else:
      return len(Str)
  
  #Calculate max column to print according to data length and maximun width
  def CalculateTableWidth(Lengths):
    i=0
    TableWidth=1
    MaxColumn=0
    Truncated=False
    for Len in Lengths:
      TableWidth+=Len+1
      MaxColumn=i
      if(TableWidth>MaxWidth):
        Truncated=True
        MaxColumn-=1
        TableWidth-=(Len+1)
        break
      i+=1
    return TableWidth,MaxColumn,Truncated

  #Exit if nothing to print
  if len(Rows)==0:
    return

  #Get console width
  MaxWidth=GetConsoleWidth()

  #Calculate data column widths
  Lengths=[0]*len(Rows[0])
  for Row in Rows:
    i=0
    for Field in Row:
      if Heading2!=None:
        Lengths[i]=max(max(max(Lengths[i],Length(str(Field).replace("\n",""))),Length(Heading1[i])),Length(Heading2[i]))
      else:
        Lengths[i]=max(max(Lengths[i],Length(str(Field).replace("\n",""))),Length(Heading1[i]))
      i+=1

  #Calculate max column to print according to data length and maximun width
  TableWidth,MaxColumn,Truncated=CalculateTableWidth(Lengths)

  #Adjust lengths if table is truncated and has resizeable columns
  RESIZABLE_COLUMNS=["W","M"]
  if Truncated==True and any(c for c in "".join(ColAttributes) if c in RESIZABLE_COLUMNS):
    while(True):
      Resized=False
      i=0
      for ColHeader in Heading1:
        if Lengths[i]>Length(ColHeader) and any(c for c in ColAttributes[i] if c in RESIZABLE_COLUMNS):
          Lengths[i]-=1
          Resized=True
        i+=1
      if Heading2!=None:
        i=0
        for ColHeader in Heading2:
          if Lengths[i]>Length(ColHeader) and any(c for c in ColAttributes[i] if c in RESIZABLE_COLUMNS):
            Lengths[i]-=1
            Resized=True
          i+=1
      if Resized==False:
        break
      TableWidth,MaxColumn,Truncated=CalculateTableWidth(Lengths)
      if Truncated==False:
        break

  #Separator line
  Separator="-"*TableWidth

  #Print column headings
  print(Separator)
  print("|",end="",flush=True)
  i=0
  for Col in Heading1:
    print(Col.center(Lengths[i])+"|",end="",flush=True)
    if(i>=MaxColumn):
      break
    i+=1
  if Heading2!=None:
    print("")
    print("|",end="",flush=True)
    i=0
    for Col in Heading2:
      print(Col.center(Lengths[i])+"|",end="",flush=True)
      if(i>=MaxColumn):
        break
      i+=1
  print("")
  print(Separator)

  #Format data for multiline columns
  LeveledRows=[]
  for Row in Rows:
    if Row[0]==SEPARATOR_ID:
      LeveledRows.append(Row)
    else:
      
      #Calculate multilines
      i=0
      MultiRow=[]
      for Field in Row:
        if ColAttributes[i].find("M")!=-1:
          Values=FormatParagraph(Field,Lengths[i]).split("\n")
        else:
          Values=[Field]
        MultiRow.append(Values)
        i+=1
      MaxValues=max([len(Values) for Values in MultiRow])
      
      #Make all columns same multiline
      for c in range(0,MaxValues):
        LeveledRow=[]
        for Field in MultiRow:
          if c<=len(Field)-1:
            LeveledRow.append(Field[c])
          else:
            LeveledRow.append("")
        LeveledRows.append(LeveledRow)

  #Print data
  for Row in LeveledRows:
    if Row[0]==SEPARATOR_ID:
      print(Separator)
    else:
      i=0
      Line="|"
      for Field in Row:
        if ColAttributes[i].find("L")!=-1:
          if ColAttributes[i].find("U")!=-1:
            FieldValue=str(Field).replace("\n","").ljust(Lengths[i])
          else:
            FieldValue=str(Field).replace("\n","")[:Lengths[i]].ljust(Lengths[i])
        elif ColAttributes[i].find("R")!=-1:
          if ColAttributes[i].find("U")!=-1:
            FieldValue=str(Field).replace("\n","").rjust(Lengths[i])
          else:
            FieldValue=str(Field).replace("\n","")[:Lengths[i]].rjust(Lengths[i])
        elif ColAttributes[i].find("C")!=-1:
          if ColAttributes[i].find("U")!=-1:
            FieldValue=str(Field).replace("\n","").center(Lengths[i])
          else:
            FieldValue=str(Field).replace("\n","")[:Lengths[i]].center(Lengths[i])
        else:
          if ColAttributes[i].find("U")!=-1:
            FieldValue=str(Field).replace("\n","").ljust(Lengths[i])
          else:
            FieldValue=str(Field).replace("\n","")[:Lengths[i]].ljust(Lengths[i])
        Line+=FieldValue+"|"
        if(i>=MaxColumn):
          break
        i+=1
      if Length(Line.replace(" ","").replace("|",""))!=0:
        print(Line)
  print(Separator)

  #Column count warning
  if(MaxColumn<len(Lengths)-1):
    WarnMessage="Displaying {0} columns out of {1} columns due to console width ({2} columns)".format(str(MaxColumn+1),str(len(Lengths)),MaxWidth)
  else:
    WarnMessage=""

  #Warning
  if(Length(WarnMessage)!=0):
    print(WarnMessage)    