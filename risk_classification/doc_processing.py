# -*- coding: utf-8 -*-
"""
This .py script parses text from .docx, .pptx, and PDF files into
sentences, and then outputs the data into .txt or .csv files.
@author: Benjamin Walzer
"""

# Install required dependencies
!pip install tika
!pip install os
!pip install nltk
!pip install pandas

# Load packages
from tika import parser
import os
import nltk
import pandas as pd

# Directory path to the folder that contains files to be parsed
# NOTE: Directory path will need to be changed to run locally!

astrobee_path = '/Astrobee Files/'
synbio_path = '/SynBio Files'

# Directory path to folder for the output files
# NOTE: Directory path will need to be changed to run locally!

out_path = '/Risk Data/'

# Get list of all of the files in the directory

astrobee_files = os.listdir(astrobee_path)
synbio_files= os.listdir(synbio_path)

def convert_to_txt(dir_path, file_name):
    '''
	Parses text from XLSX, PDF, and DOCX files.
		Parameters
             dir_path: directory path to folder that contains files   
             file_name: string filepath of file to be parsed
		
		Returns:
            out_string: string containing text from file
	'''
    
    # Use Apache Tika Parser to extract text from file
    parsed = parser.from_file(dir_path + file_name)
    out_string = parsed['content']
    
    # Remove extra whitespace
    # !! NOTE !! Depending on if the document contains periods e.g. PPT, 
    # may want to consider not removing white space and tokenizing by tabs
    # or new lines
    out_string = ' '.join(out_string.split())

    return out_string


def tokenize(in_string):
    '''
    Tokenize string input into senteces using NLTK tokenizer.

    Parameters
    ----------
    in_string : string
        String containing entire text from parsed document

    Returns
    -------
    List containing tokenized sentences from string input.

    '''
    sent_tokens = nltk.sent_tokenize(in_string)
    return sent_tokens


def write_text(tokens, out_dir_path, file_name, outfile_type = '.csv'):
    '''
    Outputs the tokenized sentences to a .csv or .txt file.

    Parameters
    ----------
    tokens : List
        List containing tokenized sentences from document text.
    out_dir_path : String
        DESCRIPTION.
    file_name : String
        DESCRIPTION.
    outfile_type : String, optional
        The type of output file to write to. The default is '.csv'.

    Returns
    -------
    None.

    '''
    
    # Ensure 
    tokens = list(tokens)
    
    assert isinstance(tokens, list)
    
    # Get the original file type
    orig_doctype = file_name[file_name.find('.') : len(file_name)]
    
    # Replace orignal filetype with output file type e.g. .csv
    write_filename = file_name.replace(orig_doctype, outfile_type)
    
    # Wrie output file to directory
    out_df = pd.DataFrame(tokens, columns = ['Sentences'])
    
    # Remove sentenes that are less than 10 characters
    out_df = out_df[out_df['Sentences'].str.len() > 9]
    
    # Write to output file
    out_df.to_csv(out_dir_path + write_filename, index = False, encoding = 'utf-8')
        
    return None

# Loop through files in input directory and output .txt and .csv files in 
# output directory

for f in astrobee_files:
    print('Writing {}.....'.format(f))
    text = convert_to_txt(astrobee_path, f)
    sentences = tokenize(text)
    # Uncomment to include .txt files
    # write_text(sentences, out_path, f, '.txt')
    write_text(sentences, out_path, f, '.csv')
    
for f in synbio_files:
    print('Writing {}.....'.format(f))
    text = convert_to_txt(synbio_path, f)
    sentences = tokenize(text)
    # Uncomment to include .txt files
    # write_text(sentences, out_path, f, '.txt')
    write_text(sentences, out_path, f, '.csv')