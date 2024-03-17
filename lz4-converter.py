import os
import sys
import zipfile
import patoolib
import lz4.frame as lz4

# Function to compress files within an archive with LZ4
def compress_archive_with_lz4(input_file, output_file):
    _, ext = os.path.splitext(input_file)
    if ext.lower() == ".zip":
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            with lz4.open(output_file, 'wb') as f_out:
                for file_info in zip_ref.infolist():
                    with zip_ref.open(file_info) as f_in:
                        f_out.write(f_in.read())
    elif ext.lower() == ".rar":
        for item in patoolib.extract_archive(input_file, outdir=None):
            if os.path.isfile(item):
                with open(item, 'rb') as f_in:
                    with lz4.open(output_file, 'wb') as f_out:
                        f_out.write(f_in.read())

# Main function to orchestrate the compression process
def compress_archives_to_tar_lz4(archive_dir, output_dir):
    for file_name in os.listdir(archive_dir):
        file_path = os.path.join(archive_dir, file_name)
        if os.path.isfile(file_path) and (file_name.endswith(".zip") or file_name.endswith(".rar")):
            output_file_name = os.path.splitext(file_name)[0] + ".tar.lz4"
            output_file_path = os.path.join(output_dir, output_file_name)
            compress_archive_with_lz4(file_path, output_file_path)

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py input_dir output_dir")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print("Input directory does not exist.")
        sys.exit(1)
    
    # Check if output directory exists, if not create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Perform the compression
    compress_archives_to_tar_lz4(input_dir, output_dir)
