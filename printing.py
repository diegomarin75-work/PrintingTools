# ---------------------------------------------------------------------------------------------------------------------
# Text printing function library
# ---------------------------------------------------------------------------------------------------------------------

# GetConsoleWidth()
# Gets actual width of console (9999 if console is redirected)

# AnsiColor(Str,FgColor,BkColor=ANSI_BD_BLACK)
# Prints string with ANSI colors

# SetSilentMode(Enabled)
# Set silent mode

# FormatParagraph(Str,Width,Indentation=0)
# Formats long string as wrapped paragraph with indentation

# Print(Text,Wheel=False,Volatile=False,Partial=False,Class="")
# Print messages on screen

# PrintTable(Heading1,Heading2,ColAttributes,Rows,MaxWidth,ReturnOutput=False)
# Print formatted table on screen

# ---------------------------------------------------------------------------------------------------------------------
# Import libraries
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import sys

# ---------------------------------------------------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------------------------------------------------

#Table printing
SEPARATOR_ID="$SEP$"
TABLE_HLINE=[SEPARATOR_ID]

#Message printing
WHEEL_CHARS=['-','\\','|','/']

#Ansi colors
ANSI_ESCAPE_PREFIX="\033["
ANSI_FD_BLACK  =30; ANSI_BD_BLACK  =40; ANSI_FB_BLACK  =90; ANSI_BB_BLACK  =100;
ANSI_FD_RED    =31; ANSI_BD_RED    =41; ANSI_FB_RED    =91; ANSI_BB_RED    =101;
ANSI_FD_GREEN  =32; ANSI_BD_GREEN  =42; ANSI_FB_GREEN  =92; ANSI_BB_GREEN  =102;
ANSI_FD_YELLOW =33; ANSI_BD_YELLOW =43; ANSI_FB_YELLOW =93; ANSI_BB_YELLOW =103;
ANSI_FD_BLUE   =34; ANSI_BD_BLUE   =44; ANSI_FB_BLUE   =94; ANSI_BB_BLUE   =104;
ANSI_FD_MAGENTA=35; ANSI_BD_MAGENTA=45; ANSI_FB_MAGENTA=95; ANSI_BB_MAGENTA=105;
ANSI_FD_CYAN   =36; ANSI_BD_CYAN   =46; ANSI_FB_CYAN   =96; ANSI_BB_CYAN   =106;
ANSI_FD_WHITE  =37; ANSI_BD_WHITE  =47; ANSI_FB_WHITE  =97; ANSI_BB_WHITE  =107;

# ---------------------------------------------------------------------------------------------------------------------
# Global variablees
# ---------------------------------------------------------------------------------------------------------------------
_MessageCnt=0
_BarStep=0
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
# Gets string with ANSI colors
# ---------------------------------------------------------------------------------------------------------------------
def AnsiColor(Str,FgColor,BkColor=ANSI_BD_BLACK):
  return f"{ANSI_ESCAPE_PREFIX}{FgColor}m{ANSI_ESCAPE_PREFIX}{BkColor}m{Str}{ANSI_ESCAPE_PREFIX}0m"

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
def Print(Text,Wheel=False,Volatile=False,Partial=False,Class="",BarProgress=None,BarLength=None):
  
  #Declare global variables
  global _LastText
  global _LastVolatile
  global _SilentMode
  global _MessageCnt
  global _BarStep
  
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
  
  #Apply progress bar
  if BarLength!=None:
    if BarProgress!=None:
      OutText="["+"#"*BarProgress+"."*(BarLength-BarProgress)+"] "+OutText
    else:
      _BarStep+=(1 if _BarStep<BarLength else 0)
      OutText="["+"#"*_BarStep+"."*(BarLength-_BarStep)+"] "+OutText

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
def PrintTable(Heading1,Heading2,ColAttributes,Rows,ReturnOutput=False):
  
  # -------------------------------------------------------------------------------------------------------------------
  # Modified length function that takes into acccount escape sequences that do not count for printed length on the screen
  # -------------------------------------------------------------------------------------------------------------------
  def Length(Str):
    
    #URLs
    Match=re.search(r"\x1b\]8;;(.*?)\x1b\\(.*?)\x1b\]8;;\x1b\\",Str)
    if Match!=None:
      _,Name=Match.groups()
      return len(Name)
    
    #Ansi colors
    Match=re.search(r"\033\[\d+m\033\[\d+m(.*?)\033\[0m",Str)
    if Match!=None:
      Text=Match.group(1)
      return len(Text)
    Match=re.search(r"\033\[\d+m(.*?)\033\[0m",Str)
    if Match!=None:
      Text=Match.group(1)
      return len(Text)
    
    #Normal string
    return len(Str)
  
  # -------------------------------------------------------------------------------------------------------------------
  # Calculate max column to print according to data length and maximun width
  # -------------------------------------------------------------------------------------------------------------------
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

  # -------------------------------------------------------------------------------------------------------------------

  #Exit if nothing to print
  if len(Rows)==0:
    if ReturnOutput==False:
      return
    else:
      return []

  #Init output
  Output=[]
  
  #Get console width
  MaxWidth=GetConsoleWidth()

  #Convert all row data to string and remove line breaks
  Rows=[[str(Field).replace("\n","") for Field in Row] for Row in Rows]
  
  #Calculate data column widths
  Lengths=[0]*len(Rows[0])
  for Row in Rows:
    i=0
    for Field in Row:
      if Heading2!=None:
        Lengths[i]=max([Lengths[i],Length(Field),Length(Heading1[i]),Length(Heading2[i])])
      else:
        Lengths[i]=max([Lengths[i],Length(Field),Length(Heading1[i])])
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
  Output.append(Separator)
  Line="|"
  i=0
  for Col in Heading1:
    Line+=Col.center(Lengths[i])+"|"
    if(i>=MaxColumn):
      break
    i+=1
  Output.append(Line)
  if Heading2!=None:
    Line="|"
    i=0
    for Col in Heading2:
      Line+=Col.center(Lengths[i])+"|"
      if(i>=MaxColumn):
        break
      i+=1
    Output.append(Line)
  Output.append(Separator)

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
      Output.append(Separator)
    else:
      i=0
      Line="|"
      for Field in Row:
        if ColAttributes[i].find("A")==-1:
          FieldValue=Field[:Lengths[i]]
          if ColAttributes[i].find("L")!=-1:
            FieldValue=FieldValue.ljust(Lengths[i])
          elif ColAttributes[i].find("R")!=-1:
            FieldValue=FieldValue.rjust(Lengths[i])
          elif ColAttributes[i].find("C")!=-1:
            FieldValue=FieldValue.center(Lengths[i])
          else:
            FieldValue=FieldValue.ljust(Lengths[i])
        else:
          if ColAttributes[i].find("L")!=-1:
            FieldValue=Field+(" "*(Lengths[i]-Length(Field) if Lengths[i]-Length(Field)>0 else 0))
          else:
            FieldValue=(" "*(Lengths[i]-Length(Field) if Lengths[i]-Length(Field)>0 else 0))+Field
        Line+=FieldValue+"|"
        if(i>=MaxColumn):
          break
        i+=1
      if Length(Line.replace(" ","").replace("|",""))!=0:
        Output.append(Line)
  Output.append(Separator)

  #Column count warning
  if(MaxColumn<len(Lengths)-1):
    WarnMessage="Displaying {0} columns out of {1} columns due to console width ({2} columns)".format(str(MaxColumn+1),str(len(Lengths)),MaxWidth)
  else:
    WarnMessage=""

  #Warning
  if(Length(WarnMessage)!=0):
    Output.append(WarnMessage)
  
  #Print or return output
  if ReturnOutput==False:
    for Line in Output:
      print(Line)
  else:
    return Output