from flask import Flask, request, send_file, render_template
import pandas as pd
import os
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_csv(input_files):
    # Define the column mapping
    column_mapping = {
        "Linkedin Url(FullEnrich)": "contact linkedin url",
        "Full Name (Linkedin)": "contact name",
        "Headline (Linkedin)": "contact title",
        "First Name (Linkedin)": "contact first name",
        "Last Name (Linkedin)": "contact last name",
        "Company Name (Linkedin)": "account name",
        "Company Website (Linkedin)": "account website",
        "All Valid Emails (FullEnrich)": "contact email",
        "All Mobile Phone Numbers (FullEnrich)": "mobile phone",
    }
    
    # List to store all dataframes
    all_dfs = []
    
    # Process each input file
    for input_file in input_files:
        try:
            # Load the CSV file
            df = pd.read_csv(input_file)
            
            # Filter and rename columns
            df_selected = df[list(column_mapping.keys())].rename(columns=column_mapping)
            
            # Add to list of dataframes
            all_dfs.append(df_selected)
            print(f"Processed: {input_file}")
            
        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")
    
    if not all_dfs:
        print("No files were processed successfully!")
        return None
    
    # Combine all dataframes
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # Remove any duplicate rows
    combined_df = combined_df.drop_duplicates()
    
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'combined_clean.csv')
    combined_df.to_csv(output_path, index=False)
    print(f"\nCleaned and combined CSV saved to: {output_path}")
    print(f"Total rows in combined file: {len(combined_df)}")
    return output_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return 'No files uploaded', 400
    
    files = request.files.getlist('files[]')
    
    if len(files) > 20:
        return 'Maximum 20 files allowed', 400
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    uploaded_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append(filepath)
    
    if not uploaded_files:
        return 'No valid CSV files uploaded', 400
    
    output_path = clean_csv(uploaded_files)
    
    if output_path:
        # Clean up uploaded files
        for file in uploaded_files:
            os.remove(file)
            
        return send_file(output_path,
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name='combined_clean.csv')
    
    return 'Error processing files', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
