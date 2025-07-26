import pandas as pd
import numpy as np
import os
import string
from tqdm import tqdm  # For progress bar
from itertools import islice  # For efficient file reading

def process_password_chunk(chunk):
    """Processes a chunk of passwords to extract features."""
    df = pd.DataFrame(chunk, columns=['password'])

    # Extract basic features
    df['length'] = df['password'].str.len()
    
    df['num_digits'] = df['password'].str.count(r'[0-9]')
    df['num_lower'] = df['password'].str.count(r'[a-z]')
    df['num_upper'] = df['password'].str.count(r'[A-Z]')
    df['num_special'] = df['password'].apply(
        lambda x: sum(1 for char in x if char in string.punctuation or not char.isalnum())
    )
    
    # Binary indicators for character types
    df['has_digit'] = (df['num_digits'] > 0).astype(int)
    df['has_lower'] = (df['num_lower'] > 0).astype(int)
    df['has_upper'] = (df['num_upper'] > 0).astype(int)
    df['has_special'] = (df['num_special'] > 0).astype(int)

    # Calculate character set size
    df['charset_size'] = 0
    df.loc[df['has_digit'] == 1, 'charset_size'] += 10  
    df.loc[df['has_lower'] == 1, 'charset_size'] += 26  
    df.loc[df['has_upper'] == 1, 'charset_size'] += 26  
    df.loc[df['has_special'] == 1, 'charset_size'] += 32  

    # Calculate entropy
    df['entropy'] = df['length'] * np.log2(df['charset_size'].replace(0, np.nan))

    return df[['password', 'length', 'num_digits', 'num_lower', 
               'num_upper', 'num_special', 'has_digit', 'has_lower',
               'has_upper', 'has_special', 'entropy']]

def main():
    """Processes the password dataset and saves features to a CSV file."""
    input_path = os.path.join('..', '..', 'data', 'raw', 'rockyou.txt')
    output_path = os.path.join('..', '..', 'data', 'processed', 'password_features.csv')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    CHUNK_SIZE = 50000
    first_chunk = True

    # Count total lines for progress bar
    with open(input_path, 'r', encoding='latin-1', errors='ignore') as f:
        total_lines = sum(1 for _ in f)

    # Process file in chunks
    with open(input_path, 'r', encoding='latin-1', errors='ignore') as f:
        with tqdm(total=total_lines, unit='password') as pbar:
            while True:
                lines = list(islice(f, CHUNK_SIZE))
                if not lines:
                    break

                passwords = [line.strip() for line in lines]
                passwords = [pwd for pwd in passwords if pwd]

                if not passwords:
                    pbar.update(len(lines))
                    continue

                chunk_df = process_password_chunk(passwords)

                # Save chunk to CSV
                chunk_df.to_csv(
                    output_path,
                    mode='a',
                    header=first_chunk,
                    index=False,
                    encoding='utf-8'
                )

                first_chunk = False
                pbar.update(len(lines))

if __name__ == '__main__':
    main()