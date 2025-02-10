import os
import subprocess

# Configuration
AUDIO_FOLDER = "audio-raw"  # Folder containing the .m4a files
OUTPUT_FOLDER = "audio"  # Folder to save compressed files
BITRATE = "96k"  # Recommended bitrate for podcasts


def compress_audio(input_folder, output_folder, bitrate):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get all .m4a files in the input folder
    audio_files = [f for f in os.listdir(input_folder) if f.endswith(".m4a")]

    for file_name in audio_files:
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        # Skip if file already exists in output folder
        if os.path.exists(output_path):
            print(f"Skipping {file_name} - already exists in output folder")
            continue

        # Compress using ffmpeg
        print(f"Compressing {file_name} to {bitrate}...")
        command = [
            "ffmpeg",
            "-i",
            input_path,  # Input file
            "-b:a",
            bitrate,  # Audio bitrate
            "-y",  # Overwrite output if it exists
            output_path,  # Output file
        ]
        try:
            subprocess.run(command, check=True)
            print(f"Compressed {file_name} successfully. Saved to {output_path}.")
        except subprocess.CalledProcessError as e:
            print(f"Error compressing {file_name}: {e}")

    print("Compression complete.")


if __name__ == "__main__":
    compress_audio(AUDIO_FOLDER, OUTPUT_FOLDER, BITRATE)
