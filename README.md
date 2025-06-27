# ARES API Tools

This Python project provides tools for querying the Czech ARES (Administrative Register of Economic Subjects) REST API. The scripts allow you to search for businesses by their IČO (company ID) or name, and include legal form resolution using an external dictionary.

## Project Structure

| File                          | Purpose |
|------------------------------|---------|
| `ares_api_tool_ico.py`       | Search for a single subject by IČO (displays name and address). |
| `ares_api_tool_name.py`      | Search subjects by name and display IČO. |
| `ares_api_tool_legal_form.py`| Search subjects by name and display IČO + legal form. |
| `script_ares_all_subjects.py`| A placeholder for combining or testing all functionalities. |

## Features

- **IČO lookup**: Fetch company name and address.
- **Name search**: Get a list of companies with matching names.
- **Legal form decoding**: Display the legal structure using ARES codebook (e.g., “Limited Liability Company”).
- **Error handling**: Detects invalid input and API errors.
- Uses `requests` and parses JSON responses.

## How to Run

1. Make sure Python 3.8+ is installed.
2. Install required package:

   ```bash
   pip install requests

Run the script:
python ares_api_tool_ico.py
python ares_api_tool_name.py
python ares_api_tool_legal_form.py
python script_ares_all_subjects.py
