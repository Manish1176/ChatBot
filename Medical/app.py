import os
import streamlit as st
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

system_prompt="""

As a highly skilled medical practitioner specializing in image analysis, analyze the given medical image with attention to detail. 
Your responsibilities include:

Detailed Analysis: Identify any abnormalities, patterns, or notable features in the image. Clearly describe the findings, and mention the anatomical structures involved, highlighting areas that require attention.

Finding Reports: Provide a comprehensive report summarizing the observations. Include potential diagnoses or conditions suggested by the findings, and state the confidence level for each interpretation.

Recommendations and Next Steps: Suggest appropriate follow-up steps, including further diagnostic tests or procedures. If the findings indicate a particular condition, recommend treatment options or consultations with specialists.

Important Notes:

Scope of Response: Focus on the clinical significance of the findings. Ensure all observations are grounded in medical best practices.
Clarity of Images: If the image quality affects the analysis, mention any limitations due to image clarity or resolution and suggest ways to improve the diagnostic accuracy.
Respond as though communicating with fellow medical professionals.

Please provide me an output response with 4 headings Detailed Analysis,Finding Reports,Recommendations and Next Steps,Treatment Suggestions

"""

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

st.set_page_config(page_title="DieseaseImage Aalytics",page_icon=":robot")

st.title("Diesease Image Analytics")

st.subheader("This application helps to identify medical images ")

uploaded_file=st.file_uploader("Upload Image for Analysis",type=["png","jpg","jpeg"])

if uploaded_file:
    st.image(uploaded_file,width=300,caption="Uploaded Medical Image")


submit_button=st.button("Generate Analysis")

if submit_button:
    image_data=uploaded_file.getvalue()

    image_parts = [
         {
             "mime_type":"image/jpeg",
             "data":image_data
             
        },
    ]  

    prompt_parts = [

        image_parts[0],
        system_prompt,
    ]

    response=model.generate_content(prompt_parts)
    
    if response:
        st.title="Here is the analysis based on your image: "

        st.write(response.text)