# Printing tools library

Tools for text printing on the screen, messages, formatting, tables, etc.

## Purpose

This library provides a set of utilities for printing formatted text and tables to the console.  
It supports silent mode, dynamic console width detection, text wrapping with indentation, volatile (in-place) messages, and formatted table rendering with alignment and truncation support.  
It is especially useful for creating clean command-line interfaces, progress updates, or log-like outputs.

## Overview

|Function name|Short description|
|-------------|-----------------|
|Print()          |Prints a formatted message to the console.|
|PrintTable()     |Prints a formatted table to the console|
|SetSilentMode()  |Enables or disables silent mode, for the message output with Print()|
|GetConsoleWidth()|Determines the current width of the console window in characters|
|FormatParagraph()|Formatting of long strings into multiple lines with word wrap and indentation|

## Installation

1. Clone the repository containing this library:

```bash
git clone https://github.com/diegomarin75-work/PrintingTools.git
```

Make the library available in your Python environment by adding its path to your PYTHONPATH environment variable.

Like this on unix-like environments:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/library
```

or like this on Windows:

```cmd
set PYTHONPATH=%PYTHONPATH%;C:\path\to\library
```

## Functions in the Library

### Print(Text, Wheel=False, Volatile=False, Partial=False, Class="")

**Description:**

Prints a formatted message to the console.
Supports rotating wheel animation, class tags, volatile output (overwriting previous text), and partial line printing.

**Parameters:**

- Text (str): The message to display.
- Wheel (bool, optional): If True, a rotating character (- \ | /) is prefixed (useful for progress indicators).
- Volatile (bool, optional): If True, the line is overwritten by the next call (for live-updating messages).
- Partial (bool, optional): If True, the line is printed without a newline (for incremental output).
- Class (str, optional): Adds a tag like [INFO], [ERROR], etc. Output is redirected to stderr for error classes (ERR, ERROR, FAIL, FAILURE).

**Example:**

```python
from printing import Print

Print("Processing data...", Wheel=True, Volatile=True)
```

### PrintTable(Heading1, Heading2, ColAttributes, Rows)

**Description:**

Prints a formatted table to the console with optional dual header rows, adjustable column widths, and alignment.
Automatically adapts to console width, truncating columns if needed.

**Parameters:**

- Heading1 (list[str]): Primary header row.
- Heading2 (list[str] or None): Secondary header row or None if not used.
- ColAttributes (list[str]): Column attributes. "L" for left-aligned, "R" for right-aligned, "C" for centered, "W" for Left-aligned with adjustment to console size (to display last column)
- Rows (list[list[str]]): Table data rows. 

Note: A row in the data (Rows parameter) with a single column that contains constant TABLE_HLINE will print an horizontal line.

**Example:**

```python
from printing import PrintTable,TABLE_HLINE

Heading1 = ["Name", "Age", "Country"]
Heading2 = ["", "", ""]
ColAttributes = ["L", "R", "L"]
Rows = [
    ["Alice", 30, "Spain"],
    ["Frank", 27, "Spain"],
    TABLE_HLINE,
    ["Bob", 28, "Germany"],
    ["John", 32, "Germany"],
    ["Mary", 31, "Germany"],
    TABLE_HLINE,
    ["Calvin", 35, "France"],
    ["Charlie", 36, "France"]
]
PrintTable(Heading1, Heading2, ColAttributes, Rows)
```

That example will print on the console a table like this:
```
---------------------
|Name   |Age|Country|
---------------------
|Alice  | 30|Spain  |
|Frank  | 27|Spain  |
---------------------
|Bob    | 28|Germany|
|John   | 32|Germany|
|Mary   | 31|Germany|
---------------------
|Calvin | 35|France |
|Charlie| 36|France |
---------------------

```

### SetSilentMode(Enabled)

**Description:**

Enables or disables silent mode. When silent mode is active, no messages are printed to the console.

**Parameters:**

Enabled (bool): True to suppress all print outputs, False to enable printing.

**Example:**

```python
from printing import SetSilentMode,Print

SetSilentMode(True)
Print("This will not be displayed.")
SetSilentMode(False)
Print("This will be displayed.")
```

### GetConsoleWidth()

**Description:**

Determines the current width of the console window in characters.
If the output is redirected (for example, to a file), it returns 9999.

**Parameters:**

None

**Returns:**

int — The console width or 9999 if redirected.

**Example:**

```python
from printing import GetConsoleWidth

width = GetConsoleWidth()
print(f"Console width: {width}")
```

### FormatParagraph(Str, Width, Indentation=0)

**Description:**

Formats a long string into multiple lines that fit within the specified width, optionally indenting each line.

**Parameters:**

Str (str): The input text to wrap.

Width (int): The maximum line width.

Indentation (int, optional): Number of spaces to indent each wrapped line (default: 0) after the first one.

#### **Returns:**
str — The formatted, wrapped text.

**Example:**
```python
from printing import FormatParagraph
text = (
  "This is a long string that will be wrapped nicely within the given width. "
  "You can see how to use this function and how it works."
)
print(FormatParagraph("Indented text: "+text, Width=50, Indentation=15))
```

That example will print on the console a text like this this:
```
Indented test: This is a long string that will be
               wrapped nicely within the given
               width. You can see how to use this
               function and how it works.
```
