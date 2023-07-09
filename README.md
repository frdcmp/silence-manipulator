# Silence Manipulator

## Overview

SilenceManipulator is a Python-based application designed to manipulate audio clips by removing or adding desired lengths of silence and mixing them with a customizable noise floor. It provides a versatile solution for processing audio files, enabling precise control over the presence of silence and the addition of background noise.

## Key Features

### Silence Removal

SilenceManipulator employs sophisticated algorithms to automatically detect and remove initial and end silence in audio clips, resulting in streamlined audio content.

### Silence Addition

Users can specify the desired length of silence to be added at the beginning or end of audio clips, providing flexibility for various audio processing needs.

### Noise Floor Mixing

SilenceManipulator allows users to introduce a customized noise floor during the manipulation process, enabling a seamless blend of audio content with background noise.

### Batch Processing

SilenceManipulator supports the efficient processing of multiple audio files in bulk, making it suitable for handling large collections of audio data.

### User-Friendly Interface

The program provides an intuitive command-line interface, facilitating easy integration into existing workflows or automation scripts.

## How to Use

1. Install the necessary dependencies by running `pip install -r requirements.txt`.
2. Run the app with Streamlit by executing the command `streamlit run roll_calculator.py`.
3. Use the Streamlit interface to interact with SilenceManipulator and specify the audio files or directories you want to process.
4. Set the desired length of silence to be removed or added.
5. Optionally, specify the characteristics of the noise floor to be mixed with the audio clips.
6. Click the appropriate buttons to process the audio files and view the results.

## Contributing

Contributions to SilenceManipulator are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please submit a pull request.

## License

SilenceManipulator is released under the MIT License. Feel free to use, modify, and distribute the software according to the terms of the license.

---
