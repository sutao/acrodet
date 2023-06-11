acrodet - Acronym Detector
==========================

This is a text processor designed to extract acronyms from a large amount
of texts.

Currently, this tool accepts a single PDF file as its input. In the future,
it may support scanning through a whole directory.

Usage:
```shell
NAME
    acrodet.py - AcroDet - Acronym Detector

SYNOPSIS
    acrodet.py FILE_NAME <flags>

DESCRIPTION
    AcroDet - Acronym Detector

POSITIONAL ARGUMENTS
    FILE_NAME
        Type: str
        Full path to the PDF file to be parsed

FLAGS
    -s, --start_page=START_PAGE
        Type: Optional[int]
        Default: None
        Start page if you want to parse a subsection
    -e, --end_page=END_PAGE
        Type: Optional[int]
        Default: None
        End page if you want to parse a subsection
    -o, --output=OUTPUT
        Type: str
        Default: 'acronyms.csv'
        Output CSV file for the result
    -p, --print_results=PRINT_RESULTS
        Type: bool
        Default: False
        Print result to screen if set

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```