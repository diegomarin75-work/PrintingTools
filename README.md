# Printing tools library

Tools for text printing on the screen, messages, formatting, tables, etc.

## Purpose

This library provides a set of utilities for printing formatted text and tables to the console.  
It supports silent mode, dynamic console width detection, text wrapping with indentation, volatile (in-place) messages, and formatted table rendering with alignment and truncation support.  
It is especially useful for creating clean command-line interfaces, progress updates, or log-like outputs.

## Installation

1. Clone the repository containing this library:

```bash
git clone <repository_url>
```

Make the library available in your Python environment by adding its path to your PYTHONPATH:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/library
```

or on Windows:

```cmd
set PYTHONPATH=%PYTHONPATH%;C:\path\to\library
```

## Functions in the Library

### GetConsoleWidth()

#### Description:
Determines the current width of the console window in characters.
If the output is redirected (for example, to a file), it returns 9999.

#### Returns:
int — The console width or 9999 if redirected.

#### Example:
```python
width = GetConsoleWidth()
print(f"Console width: {width}")
```

### SetSilentMode(Enabled)

#### Description:
Enables or disables silent mode. When silent mode is active, no messages are printed to the console.

#### Parameters:
Enabled (bool): True to suppress all print outputs, False to enable printing.

#### Example:

```python
SetSilentMode(True)
Print("This will not be displayed.")
SetSilentMode(False)
Print("This will be displayed.")
```

### FormatParagraph(Str, Width, Indentation=0)

#### Description:
Formats a long string into multiple lines that fit within the specified width, optionally indenting each line.

#### Parameters:

Str (str): The input text to wrap.

Width (int): The maximum line width.

Indentation (int, optional): Number of spaces to indent each wrapped line (default: 0).

#### Returns:
str — The formatted, wrapped text.

#### Example:
```python
text = "This is a long string that will be wrapped nicely within the given width."
print(FormatParagraph(text, Width=40, Indentation=4))
```

### Print(Text, Wheel=False, Volatile=False, Partial=False, Class="")

##### Description:
Prints a formatted message to the console.
Supports rotating wheel animation, class tags, volatile output (overwriting previous text), and partial line printing.

#### Parameters:

Text (str): The message to display.

Wheel (bool, optional): If True, a rotating character (- \ | /) is prefixed (useful for progress indicators).

Volatile (bool, optional): If True, the line is overwritten by the next call (for live-updating messages).

Partial (bool, optional): If True, the line is printed without a newline (for incremental output).

Class (str, optional): Adds a tag like [INFO], [ERROR], etc. Output is redirected to stderr for error classes (ERR, ERROR, FAIL, FAILURE).

#### Example:

```python
Print("Processing data...", Wheel=True, Volatile=True)
```

### PrintTable(Heading1, Heading2, ColAttributes, Rows)

##### Description:
Prints a formatted table to the console with optional dual header rows, adjustable column widths, and alignment.
Automatically adapts to console width, truncating columns if needed.

#### Parameters:

Heading1 (list[str]): Primary header row.

Heading2 (list[str] or None): Secondary header row or None if not used.

ColAttributes (list[str]): Column attributes.

"L" for left-aligned

"R" for right-aligned

"C" for centered

"W" for width-resizable when truncation occurs

Rows (list[list]): Table data rows.
Use a row with the constant SEPARATOR_ID (i.e. ["$SEP$"]) to insert a horizontal line.

#### Example:

```python
Heading1 = ["Name", "Age", "Country"]
Heading2 = ["", "", ""]
ColAttributes = ["L", "R", "L"]
Rows = [
    ["Alice", 30, "Spain"],
    ["Bob", 28, "Germany"],
    ["$SEP$"],
    ["Charlie", 35, "France"]
]
PrintTable(Heading1, Heading2, ColAttributes, Rows)
```