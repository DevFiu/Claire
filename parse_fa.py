"""
This module provides functions for processing FASTA files.

Functions:
1. save_ids_to_file(ids: List[str], filename: str, delimiter: str = '\t', columns: Optional[List[int]] = None, sequences: Optional[List[str]] = None) -> None:
    Save IDs and optionally sequences to a file.

2. parse_fasta_file(fasta_file: str) -> Tuple[List[str], List[str]]:
    Parse a FASTA file and return lists of IDs and corresponding sequences.

3. validate_input(fasta_file: str, sequence_id: Optional[str] = None) -> None:
    Validate input parameters.

4. slice_sequence(sequence: str, start: Optional[int] = None, end: Optional[int] = None) -> str:
    Slice a sequence.

5. save_sequences_to_file(ids: List[str], sequences: List[str], id_output_file: Optional[str], delimiter: str, columns: Optional[List[int]], write_sequence: bool) -> None:
    Save IDs and optionally sequences to a file.

6. get_sequence_by_id(fasta_file: str, sequence_id: Optional[str] = None, start: Optional[int] = None, end: Optional[int] = None, id_output_file: Optional[str] = None, delimiter: str = '\t', columns: Optional[List[int]] = None, write_sequence: bool = True) -> None:
    Get sequence(s) from a FASTA file by ID(s).

 Example usage:
target_ID = "id_name"

# Write only the target ID and its sequence
get_sequence_by_id('all.fasta', target_ID, id_output_file='target_ids.txt')

# Write all IDs and their sequences
get_sequence_by_id('all.fasta', id_output_file='all_ids.txt', columns=[0, 1])

# Write only the target ID, do not write its sequence
get_sequence_by_id('all.fasta', target_ID, id_output_file='target_ids-no_seq.txt', write_sequence=False)

# Write all IDs, do not write their sequences
get_sequence_by_id('all.fasta', id_output_file='all_ids-no_seq.txt', write_sequence=False, columns=[0, 1])

# Write the target ID and its sequence, with ID and sequence in separate lines
get_sequence_by_id('all.fasta', target_ID, start=10, end=60, id_output_file='target_ids-start_end.txt', columns=[0, 2])
"""

import os
from typing import List, Tuple, Optional

def save_ids_to_file(ids: List[str], filename: str, delimiter: str = '\t', columns: Optional[List[int]] = None, sequences: Optional[List[str]] = None) -> None:
    """
    Save IDs and optionally sequences to a file. If columns is specified, only save those columns.
    If the file already exists, it will be deleted before writing the new data.

    :param ids: List of IDs to save
    :param filename: File name to save the IDs to
    :param delimiter: Delimiter to use in the output file (default: tab)
    :param columns: List of column indices to save (0-based index). If None, save all columns.
    :param sequences: Optional list of sequences corresponding to the IDs. If None, do not save sequences.
    """

    # Input validation
    if not isinstance(ids, list) or not ids:
        raise ValueError("ids must be a non-empty list")
    if not isinstance(filename, str) or not filename:
        raise ValueError("filename must be a non-empty string")
    if columns is not None and (not isinstance(columns, list) or any(i < 0 for i in columns)):
        raise ValueError("columns must be a list of non-negative integers or None")

    # Prepare to write to file
    try:
        # Check if the file already exists and delete it
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Deleted existing file: {filename}")

        with open(filename, 'w') as file:
            for index, id_str in enumerate(ids):
                columns_to_write = id_str.split()
                if columns is not None:
                    # Select only the specified columns and validate columns range
                    columns_to_write = [columns_to_write[i] if i < len(columns_to_write) else "" for i in columns]
                file.write(delimiter.join(columns_to_write) + '\n')
                if sequences is not None and sequences[index] if sequences else False:
                    # Only write the sequence if it's not an empty string and sequences list is provided
                    file.write(sequences[index] + '\n')
    except (IOError, OSError) as e:
        print(f"Error opening/writing to the file {filename}: {e}")
        # Remove the file if an error occurs to avoid partial data
        os.remove(filename)  


def parse_fasta_file(fasta_file: str) -> Tuple[List[str], List[str]]:
    """
    Parse a FASTA file and return lists of IDs and corresponding sequences.

    :param fasta_file: Path to the FASTA file
    :return: A tuple containing two lists: IDs and sequences
    """
    # Initialize an empty list to store IDs
    ids = []        
    # Initialize an empty list to store sequences
    sequences = []  

    with open(fasta_file, 'r', encoding="utf-8") as file:
        current_id = None        
        current_sequence = '' 

        for line in file:
            line = line.strip()  

            # Check if the line starts with '>', indicating an ID line
            if line.startswith('>'):   
                if current_id and current_sequence:  
                    ids.append(current_id)  
                    sequences.append(current_sequence)  
                current_id = line[1:]  
                current_sequence = ''  
            else:  # If the line does not start with '>', it contains sequence data
                current_sequence += line  

        # After reaching the end of the file, check if there's any remaining sequence
        if current_id and current_sequence:  
            ids.append(current_id)  
            sequences.append(current_sequence)  

    return ids, sequences  


def validate_input(fasta_file: str, sequence_id: Optional[str] = None) -> None:
    """Validate input parameters"""
    if not os.path.exists(fasta_file):
        raise FileNotFoundError(f"File {fasta_file} does not exist.")
    if sequence_id is not None and not isinstance(sequence_id, str):
        raise ValueError("sequence_id must be a string.")


def slice_sequence(sequence: str, start: Optional[int] = None, end: Optional[int] = None) -> str:
    """Slice a sequence"""
    if start is not None and end is not None:
        if start > end:
            raise ValueError("Start position cannot be greater than end position.")
        return sequence[start:end]
    return sequence


def save_sequences_to_file(ids: List[str], sequences: List[str], id_output_file: Optional[str], delimiter: str, columns: Optional[List[int]], write_sequence: bool) -> None:
    """
    Save IDs and optionally sequences to a file.

    :param ids: List of IDs to save
    :param sequences: List of sequences corresponding to the IDs
    :param id_output_file: Optional file name to save the IDs and sequences to
    :param delimiter: Delimiter to use in the output file
    :param columns: Optional list of column indices to save from the ID string
    :param write_sequence: Whether to write the sequence to the output file
    """
    if id_output_file is not None:  # Check if an output file is specified
        with open(id_output_file, 'w', encoding="utf-8") as file:  
            for id, sequence in zip(ids, sequences):  
                if write_sequence:  # Check if sequence writing is enabled
                    if columns:     # Check if specific columns are specified
                        columns_to_write = [id.split()[i] for i in columns]  
                        file.write(delimiter.join(columns_to_write) + '\n')  
                        file.write(sequence + '\n')  
                    else:  # If no specific columns are specified
                        file.write(f'{id}\n{sequence}\n')  # Write ID and sequence to the file
                else:  # If sequence writing is disabled
                    file.write(f'{id}\n')  # Only write the ID to the file


def get_sequence_by_id(fasta_file: str, sequence_id: Optional[str] = None, start: Optional[int] = None, end: Optional[int] = None, id_output_file: Optional[str] = None, delimiter: str = '\t', columns: Optional[List[int]] = None, write_sequence: bool = True) -> None:
    """
    Get sequence(s) from a FASTA file by ID(s)
    
    :param fasta_file: Path to the FASTA file
    :param sequence_id: Optional specific sequence ID to retrieve
    :param start: Optional start position for slicing the sequence
    :param end: Optional end position for slicing the sequence
    :param id_output_file: Optional file name to save the retrieved IDs to
    :param delimiter: Delimiter to use in the output file (default: tab)
    :param columns: Optional list of column indices to save from the ID string
    :param write_sequence: Whether to write the sequence to the output file (default: True)
    """

    # Validate input parameters
    validate_input(fasta_file, sequence_id)  
    
    # If columns is not empty but has zero length, set it to None
    if columns is not None and len(columns) == 0:
        columns = None

    # Parse the FASTA file
    all_ids, all_sequences = parse_fasta_file(fasta_file)  

    try:
        if sequence_id:  
            target_sequence = ''  
            # Iterate through all sequences to find a matching ID
            for id, sequence in zip(all_ids, all_sequences):
                if id == sequence_id:  
                    target_sequence = slice_sequence(sequence, start, end)  
                    break  
            # If a matching sequence is found, proceed with processing
            if target_sequence:  
                sequence_length = len(target_sequence)  
                print(f'ID: {sequence_id}')  
                if write_sequence:  
                    print(f'Sequence Length: {sequence_length}')  
                # Save the sequence to a file
                save_sequences_to_file([sequence_id], [target_sequence], id_output_file, delimiter, columns, write_sequence)
            else:  
                print(f'ID {sequence_id} not found in the FASTA file.')
        else:  
            # If no specific sequence ID is provided, save all IDs and their sequences to a file
            save_sequences_to_file(all_ids, all_sequences, id_output_file, delimiter, columns, write_sequence)
    except Exception as e:  # Handle exceptions
        print(f'An error occurred while processing the file: {e}')  
