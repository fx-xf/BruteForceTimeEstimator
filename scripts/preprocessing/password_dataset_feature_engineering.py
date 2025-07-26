import pandas as pd
import numpy as np
import os
import string
from tqdm import tqdm
from itertools import islice

def process_password_chunk(chunk):
    """Processes the password chunk and returns a DataFrame with the following attributes"""
    df = pd.DataFrame(chunk, columns=['password'])

    # Basic features
    df['length'] = df['password'].str.len()
    
    # Character type counters
    df['num_digits'] = df['password'].str.count(r'[0-9]')
    df['num_lower'] = df['password'].str.count(r'[a-z]')
    df['num_upper'] = df['password'].str.count(r'[A-Z]')
    df['num_special'] = df['password'].apply(
        lambda x: sum(1 for char in x if char in string.punctuation or not char.isalnum())
    )
    
    # Binary flags for the presence of characters
    df['has_digit'] = (df['num_digits'] > 0).astype(int)
    df['has_lower'] = (df['num_lower'] > 0).astype(int)
    df['has_upper'] = (df['num_upper'] > 0).astype(int)
    df['has_special'] = (df['num_special'] > 0).astype(int)

    # Calculating entropy
    df['charset_size'] = 0
    df.loc[df['has_digit'] == 1, 'charset_size'] += 10  # 0-9
    df.loc[df['has_lower'] == 1, 'charset_size'] += 26  # a-z
    df.loc[df['has_upper'] == 1, 'charset_size'] += 26  # A-Z
    df.loc[df['has_special'] == 1, 'charset_size'] += 32  # Special characters

    #Entropy calculation (the basis of hacking complexity)
    df['entropy'] = df['length'] * np.log2(df['charset_size'].replace(0, np.nan))

    return df[['password', 'length', 'num_digits', 'num_lower', 
               'num_upper', 'num_special', 'has_digit', 'has_lower',
               'has_upper', 'has_special', 'entropy']]


def main():
    input_path = os.path.join('..', '..', 'data', 'raw', 'rockyou.txt')
    output_path = os.path.join('..', '..', 'data', 'processed', 'password_features.csv')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    CHUNK_SIZE = 50000
    first_chunk = True

    with open(input_path, 'r', encoding='latin-1', errors='ignore') as f:
        total_lines = sum(1 for _ in f)

    
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