import streamlit as st
import os
import pandas as pd
import base64
import random
from pydub import AudioSegment
from function import calculate_initial_silence_duration, calculate_end_silence_duration, trim_beginning, trim_end, pad_beginning, pad_end, mix_audio_with_noise, process_audio_files, move_files

# Initialize session state variables
if 'trim_beginning' not in st.session_state:
    st.session_state.trim_beginning = False
if 'trim_end' not in st.session_state:
    st.session_state.trim_end = False
if 'pad_beginning' not in st.session_state:
    st.session_state.pad_beginning = False
if 'pad_end' not in st.session_state:
    st.session_state.pad_end = False


def main():
    # Set Streamlit to wide mode
    st.set_page_config(layout="wide")
    
    st.write("# Mazzafrusto")

    # Default folder path
    default_folder_path = "./"

    # File drop input
    uploaded_files = st.file_uploader("Drop audio files here", accept_multiple_files=True)

    # Folder input
    folder_name = st.text_input("Enter folder name", value="audio")

    # Combine default folder path with user-inputted folder name
    folder_path = os.path.join(default_folder_path, folder_name)

    st.write("---")

    # Create a column layout for the inputs
    col1, col2 = st.columns(2)

    # Minimum Silent Length allowed input
    with col1:
        min_silent_length = st.number_input("Minimum Silent Length allowed (s)", value=0.09)

    # Maximum Silent Length allowed input
    with col2:
        max_silent_length = st.number_input("Maximum Silent Length allowed (s)", value=0.1)

    # Add sliders to adjust the dB threshold values
    db_threshold_start = st.slider("dB threshold start (dB)", min_value=-80, max_value=-20, value=-50, format="%.1f dB")
    db_threshold_end = st.slider("dB threshold end (dB)", min_value=-80, max_value=-20, value=-50, format="%.1f dB")


    st.write("---")
    st.write("")
    # Check if results exist
    if "results" not in st.session_state:
        st.session_state.results = None

    if st.button("Calculate Silence"):
        audio_files = []
        st.write("")
        # Process uploaded files
        if uploaded_files:
            for file in uploaded_files:
                # Save the uploaded file to a temporary location
                with open(os.path.join(default_folder_path, file.name), "wb") as f:
                    f.write(file.getbuffer())

                audio_files.append(file.name)

        # Process folder input
        if folder_name:
            folder_path = os.path.join(default_folder_path, folder_name)
            if os.path.isdir(folder_path):
                # Get all audio files in the folder
                audio_files.extend([file for file in os.listdir(folder_path) if file.endswith(".wav")])

        if len(audio_files) > 0:
            results = []

            for file_name in audio_files:
                file_path = os.path.join(folder_path, file_name)

                # Calculate initial silence duration
                initial_silence_duration = calculate_initial_silence_duration(file_path, db_threshold_start)

                # Calculate end silence duration
                end_silence_duration = calculate_end_silence_duration(file_path, db_threshold_end)

                # Check if the silence durations are within the allowed range
                initial_test = True if min_silent_length <= initial_silence_duration <= max_silent_length else False
                end_test = True if min_silent_length <= end_silence_duration <= max_silent_length else False
                
                # Perform logical AND operation
                check_test = initial_test and end_test

                # Add the results to the list
                results.append({
                    "File Name": file_name,
                    "Initial Silence (s)": initial_silence_duration,
                    "End Silence (s)": end_silence_duration,
                    "Initial Check": initial_test,
                    "End Check": end_test,
                    "Check": check_test                 
                })

            # Create a DataFrame from the results list
            df = pd.DataFrame(results, columns=["File Name", "Initial Silence (s)", "End Silence (s)", "Initial Check", "End Check", "Check"])

            # Store the results in session state
            st.session_state.results = df

        else:
            st.write("No audio files found.")



    # Display the results
    if st.session_state.results is not None:
        st.write(st.session_state.results)
        st.write("")
        # Export results to a CSV file and provide a download link
        if st.button("Generate CSV link"):
            csv_file = st.session_state.results.to_csv(index=False)
            b64 = base64.b64encode(csv_file.encode()).decode()  # Encode the CSV file as base64
            download_link = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download CSV</a>'
            st.markdown(download_link, unsafe_allow_html=True)
        st.write("---")
        st.markdown("<h2>Trimming and Padding Section</h2>", unsafe_allow_html=True)
      
        # pre roll input
        st.write("Adjusting the pre-roll and post-roll length")
        pre_roll = st.slider("Pre / Post Roll (ms)", min_value=0, max_value=300, value=95, step=1, format="%.0f ms")
        pre_roll /= 1000  # Convert milliseconds to seconds


        # Create a checkbox container for selecting processing operations
        #st.write("Select Processing Operations:")
        #st.session_state.trim_beginning = st.checkbox("Trim Beginning", value=st.session_state.trim_beginning)
        #st.session_state.trim_end = st.checkbox("Trim End", value=st.session_state.trim_end)
        #st.session_state.pad_beginning = st.checkbox("Pad Beginning", value=st.session_state.pad_beginning)
        #st.session_state.pad_end = st.checkbox("Pad End", value=st.session_state.pad_end)
        st.write("")
        st.write("Process the Files. Files are saved in the output folder")
        # Create a tab
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Trim the beginning of each file
            if st.button("Trim Beginning"):
                if st.session_state.results is not None:
                    for index, row in st.session_state.results.iterrows():
                        file_name = row["File Name"]
                        initial_silence_duration = row["Initial Silence (s)"]
                        end_silence_duration = row["End Silence (s)"]

                        file_path = os.path.join(folder_path, file_name)

                        # Check if the initial silence duration exceeds the pre roll
                        if initial_silence_duration > pre_roll:
                            # Trim the beginning of the file
                            modified_file_path = trim_beginning(file_path, initial_silence_duration, pre_roll)
                        else:
                            # Skip the file
                            #st.write(f"Skipping file: {file_name} - Initial silence duration is not greater than pre roll.")
                            continue

                        # Update the session state with the modified file path
                        st.session_state.results.at[index, "Modified File Path"] = modified_file_path

                        st.write("Beginning trimmed successfully.")
        with col2:
            # Trim the end of each file
            if st.button("Trim End"):
                if st.session_state.results is not None:
                    for index, row in st.session_state.results.iterrows():
                        file_name = row["File Name"]
                        initial_silence_duration = row["Initial Silence (s)"]
                        end_silence_duration = row["End Silence (s)"]

                        file_path = os.path.join(folder_path, file_name)
                        # Check if the end silence duration exceeds the pre roll
                        if end_silence_duration > pre_roll:
                            # Trim the end of the file
                            modified_file_path = trim_end(file_path, end_silence_duration, pre_roll)
                        else:
                            # Skip the file
                            #st.write(f"Skipping file: {file_name} - End silence duration is not greater than pre roll.")
                            continue

                        # Update the session state with the modified file path
                        st.session_state.results.at[index, "Modified File Path"] = modified_file_path

                        st.write("End trimmed successfully.")
        with col3:
            # Pad the beginning of each file
            if st.button("Pad Beginning"):
                if st.session_state.results is not None:
                    for index, row in st.session_state.results.iterrows():
                        file_name = row["File Name"]
                        initial_silence_duration = row["Initial Silence (s)"]
                        end_silence_duration = row["End Silence (s)"]

                        file_path = os.path.join(folder_path, file_name)

                        # Check if the initial silence duration is less than the pre roll
                        if initial_silence_duration < pre_roll:
                            # Pad the beginning of the file
                            modified_file_path = pad_beginning(file_path, initial_silence_duration, pre_roll)
                        else:
                            # Skip the file
                            #st.write(f"Skipping file: {file_name} - Initial silence duration is not less than pre roll.")
                            continue

                        # Update the session state with the modified file path
                        st.session_state.results.at[index, "Modified File Path"] = modified_file_path

                        st.write("Beginning padded successfully.")
        with col4:
            # Pad the end of each file
            if st.button("Pad End"):
                if st.session_state.results is not None:
                    for index, row in st.session_state.results.iterrows():
                        file_name = row["File Name"]
                        initial_silence_duration = row["Initial Silence (s)"]
                        end_silence_duration = row["End Silence (s)"]

                        file_path = os.path.join(folder_path, file_name)

                        # Check if the end silence duration is less than the pre roll
                        if end_silence_duration < pre_roll:
                            # Pad the end of the file
                            modified_file_path = pad_end(file_path, end_silence_duration, pre_roll)
                        else:
                            # Skip the file
                            #st.write(f"Skipping file: {file_name} - End silence duration is not less than pre roll.")
                            continue

                        # Update the session state with the modified file path
                        st.session_state.results.at[index, "Modified File Path"] = modified_file_path

                        st.write("End padded successfully.")
       
        st.write("---")          
        st.write("")
        # Create the noise tab
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write("Add noise from the noise folder. Files are mixed randomly between the clips. Please make sure the noise files are always longer than the input files. Files are saved in the 'output/added_noise' folder")                 
 
        with col3:    
            # Process Noise Beginning
            default_noise_folder_path = "./output"

            # Folder input
            noise_folder_name = st.text_input("Enter folder name", value="pad_beginning")

            # Combine default folder path with user-inputted folder name
            noise_folder_path = os.path.join(default_noise_folder_path, noise_folder_name)

            if st.button("Process Noise Beginning"):
                    # Check if audio files were dropped
                    if uploaded_files:
                        # Save uploaded files to the specified folder
                        os.makedirs(noise_folder_path, exist_ok=True)
                        for file in uploaded_files:
                            file_path = os.path.join(noise_folder_path, file.name)
                            with open(file_path, "wb") as f:
                                f.write(file.getbuffer())

                    process_audio_files(noise_folder_path)

        with col4:    
            # Process Noise End
            default_noise_folder_path = "./output"

            # Folder input
            folder_name = st.text_input("Enter folder name", value="pad_end")

            # Combine default folder path with user-inputted folder name
            noise_folder_path = os.path.join(default_noise_folder_path, folder_name)

            if st.button("Process Noise End"):
                    # Check if audio files were dropped
                    if uploaded_files:
                        # Save uploaded files to the specified folder
                        os.makedirs(noise_folder_path, exist_ok=True)
                        for file in uploaded_files:
                            file_path = os.path.join(noise_folder_path, file.name)
                            with open(file_path, "wb") as f:
                                f.write(file.getbuffer())

                    process_audio_files(noise_folder_path)              
                    

        st.write("---")  
        st.write("")
        st.write("Saving and Overwriting the files. Files are saved in the audio folder, replacing the original. Save each time before processing for the next step to concatenate the results.")
        # Create the MOVING tab columns
        col1, col2, col3, col4 = st.columns(4)

        #Move Trim Begin        
        with col1:
            # Create a Streamlit button
            if st.button("Save TB"):
                source_folder = "./output/trim_beginning"
                destination_folder = os.path.join(default_folder_path, folder_path)
                st.write("Destination folder:", destination_folder)  # Print the destination folder path in Streamlit

                try:
                    move_files(source_folder, destination_folder)
                    st.success("Files moved successfully!")
                except ValueError as e:
                    st.error(str(e))


 
        #Move Trim End        
        with col2:
            # Create a Streamlit button
            if st.button("Save TE"):
                source_folder = "./output/trim_end"
                destination_folder = os.path.join(default_folder_path, folder_path)
                st.write("Destination folder:", destination_folder)  # Print the destination folder path in Streamlit
                try:
                    move_files(source_folder, destination_folder)
                    st.success("Files moved successfully!")
                except ValueError as e:
                    st.error(str(e))
   
        #Move Pad Begin        
        with col3:
            # Create a Streamlit button
            if st.button("Save PB"):
                source_folder = "./output/added_noise"
                destination_folder = os.path.join(default_folder_path, folder_path)
                st.write("Destination folder:", destination_folder)  # Print the destination folder path in Streamlit
                try:
                    move_files(source_folder, destination_folder)
                    st.success("Files moved successfully!")
                except ValueError as e:
                    st.error(str(e))
 
   
        #Move Pad End        
        with col4:
            # Create a Streamlit button
            if st.button("Save PE"):
                source_folder = "./output/added_noise"
                destination_folder = os.path.join(default_folder_path, folder_path)
                st.write("Destination folder:", destination_folder)  # Print the destination folder path in Streamlit
                try:
                    move_files(source_folder, destination_folder)
                    st.success("Files moved successfully!")
                except ValueError as e:
                    st.error(str(e))



        st.write("---")  
        st.write("")
        st.write("Summary block. It shows alll the FALSE and TRUE checks for Initial, End and Overall.")
        # Summary block
        num_initial_false = st.session_state.results["Initial Check"].value_counts().get(False, 0)
        num_initial_true = st.session_state.results["Initial Check"].value_counts().get(True, 0)
        num_end_false = st.session_state.results["End Check"].value_counts().get(False, 0)
        num_end_true = st.session_state.results["End Check"].value_counts().get(True, 0)
        num_check_false = st.session_state.results["Check"].value_counts().get(False, 0)
        num_check_true = st.session_state.results["Check"].value_counts().get(True, 0)


        # Creating a tab
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            tabs = ["Initial Checks", "End Checks", "Overall Checks"]
            current_tab = st.radio("Checks", tabs)

        with col2:
            st.write("Results:")              
            if current_tab == "Initial Checks":
                st.write(f"FALSE: {num_initial_false}")
                st.write(f"TRUE: {num_initial_true}")
            elif current_tab == "End Checks":
                st.write(f"FALSE: {num_end_false}")
                st.write(f"TRUE: {num_end_true}")
            elif current_tab == "Overall Checks":
                st.write(f"FALSE: {num_check_false}")
                st.write(f"TRUE: {num_check_true}")


# Run the Streamlit app
if __name__ == "__main__":
    main()
