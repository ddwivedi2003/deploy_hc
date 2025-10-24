import streamlit as st
from streamlit_lottie import st_lottie
import json
import numpy as np
from PIL import Image
from report import analyze_report
from assistant import get_health_assistance


path = "a1.json"
with open(path, "r") as file:
    url = json.load(file)



st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Select a section",
    ("Home", "Health Assistant AI", "Report Analysis"),
    index=0  
)




if section == "Home":
    st.title("Welcome to Healthcare AI")
    st_lottie(url, height=150, width=150, speed=0.5, loop=True)

    st.markdown("""
        ### Choose an option to get started:
        
        **🤖 Health Assistant AI**  
        Ask any health-related questions, including information about symptoms, treatments, fitness advice, and medicines.
        
        
        **🩺 Report Analysis**  
        Upload a medical report image to get AI-assisted analysis of the report's findings.
    """, unsafe_allow_html=True)


if section == "Health Assistant AI":
    st.markdown("<h2>💬 Health Assistance via AI</h2>", unsafe_allow_html=True)

    user_query = st.text_input("Ask any health-related question (e.g., symptoms, treatments, fitness advice, About Medicine):")
    category = st.radio(
        "What kind of advice are you looking for?",
        ("Symptoms & Diagnosis", "Nutrition & Diet", "Mental Health", "Fitness & Exercise", "About Medicine")
    )

    if st.button("Get AI Assistance"):
        if user_query and category:
            with st.spinner("Thinking..."):
                ai_response = get_health_assistance(user_query, category)
                st.markdown(f"**AI Response:**\n\n{ai_response}")
        else:
            st.error("Please enter a question and select a category.")


elif section == "Report Analysis":
    st.markdown("<h2>Medical Report Analysis</h2>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload a medical report", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Report", use_column_width=True)
        with st.spinner("Analyzing the report..."):
            diagnosis, error = analyze_report(uploaded_file)
        if error:
            st.error(error)
        elif diagnosis:
            st.write("Diagnosis:")
            st.write(diagnosis)

st.markdown("---")
st.markdown("Powered by Healthcare AI  2024. For support, contact [Dewashish Dwivedi](mailto:ddwivedi2003@gmail.com).")

