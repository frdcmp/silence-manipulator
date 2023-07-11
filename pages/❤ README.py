import streamlit as st

def main():
    st.title('Silence Manipulator')
    st.markdown('## GitHub Repository')
    st.markdown('[GitHub Repository](https://github.com/frdcmp/silence-manipulator)')


    st.markdown('## Overview')
    st.markdown('SilenceManipulator is a Python-based application designed to manipulate audio clips by removing or adding desired lengths of silence and mixing them with a customizable noise floor. It provides a versatile solution for processing audio files, enabling precise control over the presence of silence and the addition of background noise.')

    st.markdown('## Overview')
    st.markdown('SilenceManipulator is a Python-based application designed to manipulate audio clips by removing or adding desired lengths of silence and mixing them with a customizable noise floor. It provides a versatile solution for processing audio files, enabling precise control over the presence of silence and the addition of background noise.')

    st.markdown('## Key Features')
    st.markdown('### Silence Removal')
    st.markdown('SilenceManipulator employs sophisticated algorithms to automatically detect and remove initial and end silence in audio clips, resulting in streamlined audio content.')

    st.markdown('### Silence Addition')
    st.markdown('Users can specify the desired length of silence to be added at the beginning or end of audio clips, providing flexibility for various audio processing needs.')

    st.markdown('### Noise Floor Mixing')
    st.markdown('SilenceManipulator allows users to introduce a customized noise floor during the manipulation process, enabling a seamless blend of audio content with background noise.')

    st.markdown('### Batch Processing')
    st.markdown('SilenceManipulator supports the efficient processing of multiple audio files in bulk, making it suitable for handling large collections of audio data.')

    st.markdown('### User-Friendly Interface')
    st.markdown('The program provides an intuitive command-line interface, facilitating easy integration into existing workflows or automation scripts.')

    st.markdown('## How to Use')
    st.markdown('1. Install the necessary dependencies by running `pip install -r requirements.txt`.')
    st.markdown('2. Run the app with Streamlit by executing the command `streamlit run app.py`.')
    st.markdown('3. Use the Streamlit interface to interact with SilenceManipulator and specify the audio files or directories you want to process.')
    st.markdown('4. Set the desired length of silence to be removed or added.')
    st.markdown('5. Optionally, specify the characteristics of the noise floor to be mixed with the audio clips.')
    st.markdown('6. Click the appropriate buttons to process the audio files and view the results.')

    st.markdown('## Contributing')
    st.markdown('Contributions to SilenceManipulator are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please submit a pull request.')

    st.markdown('## License')
    st.markdown('SilenceManipulator is released under the MIT License. Feel free to use, modify, and distribute the software according to the terms of the license.')

# Create the Streamlit app
if __name__ == '__main__':
    main()
