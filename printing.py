# Text printing function library:

# SetSilentMode(Enabled)                                    # Set silent mode
# Print(Text,Volatile=False,Partial=False)                  # Print messages on screen
# PrintTable(Heading1,Heading2,ColAttributes,Rows,MaxWidth) # Print formatted table on screen

#Constants
SEPARATOR_ID="$SEP$"
TABLE_HLINE=[SEPARATOR_ID]

#Global variablees
_LastText=""
_LastVolatile=False  
_SilentMode=False

# ---------------------------------------------------------------------------------------------------------------------
# Set silent mode
# ---------------------------------------------------------------------------------------------------------------------
def SetSilentMode(Enabled):
  global _SilentMode
  _SilentMode=Enabled

# ---------------------------------------------------------------------------------------------------------------------
# Print message
# ---------------------------------------------------------------------------------------------------------------------
def Print(Text,Volatile=False,Partial=False):
  global _LastText
  global _LastVolatile
  global _SilentMode
  if _SilentMode==True:
    return
  if _LastVolatile==True:
    print("\r",end="",flush=True)
    print(" "*len(_LastText),end="\r",flush=True)
  if Volatile==True or Partial==True:
    print(Text,end="",flush=True)
  else:
    print(Text)
  _LastText=Text
  _LastVolatile=Volatile

#----------------------------------------------------------------------------------------------------------------------
# PrintTable
#----------------------------------------------------------------------------------------------------------------------
def PrintTable(Heading1,Heading2,ColAttributes,Rows,MaxWidth):
  
  #Exit if nothing to print
  if len(Rows)==0:
    return

  #Calculate data column widths
  Lengths=[0]*len(Rows[0])
  for Row in Rows:
    i=0
    for Field in Row:
      if Heading2!=None:
        Lengths[i]=max(max(max(Lengths[i],len(str(Field).replace("\n",""))),len(Heading1[i])),len(Heading2[i]))
      else:
        Lengths[i]=max(max(Lengths[i],len(str(Field).replace("\n",""))),len(Heading1[i]))
      i+=1

  #Calculate max column to print according to data length and maximun width
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

  #Adjust lengths if table is truncated and has resizeable columns
  if Truncated==True and "".join(ColAttributes).find("W")!=-1:
    while(True):
      Resized=False
      i=0
      for ColHeader in Heading1:
        if Lengths[i]>len(ColHeader) and ColAttributes[i].find("W")!=-1:
          Lengths[i]-=1
          Resized=True
        i+=1
      if Heading2!=None:
        i=0
        for ColHeader in Heading2:
          if Lengths[i]>len(ColHeader) and ColAttributes[i].find("W")!=-1:
            Lengths[i]-=1
            Resized=True
          i+=1
      if Resized==False:
        break
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

  #Print data
  for Row in Rows:
    if Row[0]==SEPARATOR_ID:
      print(Separator)
    else:
      i=0
      print("|",end="",flush=True)
      for Field in Row:
        if ColAttributes[i].find("L")!=-1:
          print(str(Field).replace("\n","")[:Lengths[i]].ljust(Lengths[i])+"|",end="",flush=True)
        elif ColAttributes[i].find("R")!=-1:
          print(str(Field).replace("\n","")[:Lengths[i]].rjust(Lengths[i])+"|",end="",flush=True)
        elif ColAttributes[i].find("C")!=-1:
          print(str(Field).replace("\n","")[:Lengths[i]].center(Lengths[i])+"|",end="",flush=True)
        if(i>=MaxColumn):
          break
        i+=1
      print("")
  print(Separator)

  #Column count warning
  if(MaxColumn<len(Lengths)-1):
    WarnMessage="Displaying {0} columns out of {1} columns due to console width".format(str(MaxColumn+1),str(len(Lengths)))
  else:
    WarnMessage=""

  #Warning
  if(len(WarnMessage)!=0):
    print(WarnMessage)    