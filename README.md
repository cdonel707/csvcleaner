# CSV-cleaner

A Python script to clean and standardize CSV files containing contact information. The script:

1. Takes CSV files from a "dirty" folder
2. Standardizes column names
3. Combines multiple files into one
4. Removes duplicates
5. Saves the cleaned result in a "clean" folder

## Usage

1. Place your CSV files in the `dirty` folder
2. Run the script:
   ```bash
   python clean.py
   ```
3. Find your cleaned and combined CSV in the `clean` folder as `combined_clean.csv`

## Column Mapping

The script standardizes the following columns:
- LinkedIn URL
- Full Name
- Job Title
- First Name
- Last Name
- Company Name
- Company Website
- Email
- Mobile Phone # CSV-cleaner
