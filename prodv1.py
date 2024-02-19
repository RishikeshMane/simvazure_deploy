import streamlit as st

def intro():
    import streamlit as st
    from PIL import Image
    import pandas as pd

    sheet1 = pd.read_excel('data_nopics.xlsx' )


    # Set a title for your app
    st.title('SimuVerse by Unruffled Feathers')

    # Initialize session state variables if they don't exist
    if 'show_input' not in st.session_state:
        st.session_state.show_input = True  # Controls whether to show input form or results

    # Toggle function to switch views
    def toggle_view():
        st.session_state.show_input = not st.session_state.show_input

    # Create a placeholder to store shirt data
    if 'shirt_data' not in st.session_state:
        st.session_state.shirt_data = []

    # Define the function to add a shirt to the list
    def add_shirt(brand, shoulder, length, chest, image):
        st.session_state.shirt_data.append({"Brand": brand, "Shoulder": shoulder, "Length": length, "Chest": chest, "Image": image})

    # Function to display matching shirts based on user's dimensions
    def recommend_shirts(shoulder, length, chest):
        matches = [shirt for shirt in st.session_state.shirt_data if shirt["Shoulder"] <= shoulder + 1 and shirt["Shoulder"] >= shoulder - 1 and shirt["Length"] <= length + 1 and shirt["Length"] >= length - 1 and shirt["Chest"] <= chest + 1 and shirt["Chest"] >= chest - 1]
        if matches:
            for match in matches:
                st.write(f"Brand: {match['Brand']}, Shoulder: {match['Shoulder']}, Length: {match['Length']}, Chest: {match['Chest']}")
                st.image(match["Image"], width=200)
        else:
            st.write("No matching shirts found.")
            ####

        # Sidebar logic for showing input or results
    if st.session_state.show_input:
        expander_forexcel = st.expander("See Excel Data")
        expander_forexcel.write(sheet1)
        # expander = st.expander("Give Inputs")
        # expander.write("Inputs Here")

        col1, col2, col3 ,col4 = st.columns(4)

        with col1:
            excel_data = sheet1['Brand']
            Brand_data = st.selectbox('Brand',excel_data,key="one")

        with col2:
            excel_data = sheet1['Shoulder']
            Shoulder_data = st.selectbox('Shoulder',excel_data,key="two")

        with col3:
            excel_data = sheet1['Length']
            Length_data = st.selectbox('Length',excel_data,key="three")
        
        with col4:
            excel_data = sheet1['Chest']
            Chest_data = st.selectbox('Chest',excel_data,key="four")

        brand = Brand_data
        shoulder = Shoulder_data
        length = Length_data
        chest = Chest_data
        st.write("Values are :", Brand_data , str(Shoulder_data) , str(Length_data) , str(Chest_data))
        with st.sidebar:
            st.write("## Input Shirt Data")
            image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
            if st.button("Add Shirt"):
                if image:
                    image = Image.open(image)
                    add_shirt(brand, shoulder, length, chest, image)
                    st.success("Shirt added successfully!")
            st.button("Show Recommendations", on_click=toggle_view)
    else:
        st.sidebar.write("## Enter Your Dimensions")
        user_shoulder = st.sidebar.slider("Your Shoulder Width (in inches)", min_value=0.0, max_value=50.0, value=18.0, step=0.5)
        user_length = st.sidebar.slider("Your Shirt Length (in inches)", min_value=0.0, max_value=50.0, value=24.0, step=0.5)
        user_chest = st.sidebar.slider("Your Chest Size (in inches)", min_value=0.0, max_value=50.0, value=36.0, step=0.5)
        if st.sidebar.button("Find Matching Shirts"):
            recommend_shirts(user_shoulder, user_length, user_chest)
        st.sidebar.button("Back to Add Shirt", on_click=toggle_view)

    # st.text(sheet1['Shoulder'])
        
def mapping_demo():
    import streamlit as st
    import pandas as pd
    import numpy as np

    # Initialize session state variables for storing CSV data if they don't exist
    if 'tshirt_specs_df' not in st.session_state:
        st.session_state['tshirt_specs_df'] = pd.DataFrame()
    if 'employee_measurements_df' not in st.session_state:
        st.session_state['employee_measurements_df'] = pd.DataFrame()

    def load_csv(file):
        """Utility function to load and return CSV files."""
        if file is not None:
            return pd.read_csv(file)
        return None

    def find_best_matches():
        """Matching logic to find the best T-shirt for each employee."""
        matches = []
        for _, emp in st.session_state.employee_measurements_df.iterrows():
            # Calculate the difference in measurements for all T-shirts
            st.session_state.tshirt_specs_df['diff'] = np.sqrt(
                (st.session_state.tshirt_specs_df['shoulder'] - emp['shoulder'])**2 +
                (st.session_state.tshirt_specs_df['length'] - emp['length'])**2 +
                (st.session_state.tshirt_specs_df['chest'] - emp['chest'])**2
            )
            
            # Find the T-shirt with the minimum difference
            best_match = st.session_state.tshirt_specs_df.loc[st.session_state.tshirt_specs_df['diff'].idxmin()]
            matches.append({
                'EmployeeID': emp['EmployeeID'],
                'shoulder': emp['shoulder'],
                'length': emp['length'],
                'chest': emp['chest'],
                'type': best_match['type'],
                'brand': best_match['brand']
            })
            
        return pd.DataFrame(matches)

    # Setup the Streamlit interface
    st.title("T-shirt Matcher")

    # Navigation in sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Upload T-shirt Specs", "Upload Employee Measurements", "Match Dashboard"])

    if page == "Upload T-shirt Specs":
        st.header("Upload T-shirt Specifications")
        uploaded_file = st.file_uploader("Choose a CSV file", key="tshirt_specs")
        if uploaded_file is not None:
            st.session_state.tshirt_specs_df = load_csv(uploaded_file)
            st.write(st.session_state.tshirt_specs_df)

    elif page == "Upload Employee Measurements":
        st.header("Upload Employee Measurements")
        uploaded_file = st.file_uploader("Choose a CSV file", key="employee_measurements")
        if uploaded_file is not None:
            st.session_state.employee_measurements_df = load_csv(uploaded_file)
            st.write(st.session_state.employee_measurements_df)

    elif page == "Match Dashboard":
        st.header("Matching Dashboard")
        if st.session_state.tshirt_specs_df.empty or st.session_state.employee_measurements_df.empty:
            st.write("Please upload both T-shirt specifications and employee measurements to see matches.")
        else:
            match_results = find_best_matches()
            st.dataframe(match_results)
            
page_names_to_funcs = {
    "Single Demo": intro,
    "Bulk Demo": mapping_demo
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
