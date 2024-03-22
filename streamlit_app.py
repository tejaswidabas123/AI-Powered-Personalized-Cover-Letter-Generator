import streamlit as st
import io
from PyPDF2 import PdfReader
from main import create_cover_letter

st.image("https://cdn.mos.cms.futurecdn.net/u5bN26Y7eYqrGYHDrBKqDk.jpg", width=600)
st.header("Stop Drafting, Start Applying: AI-Powered Cover Letter Crafting")

company = st.text_input("Name of Company", placeholder="Enter your preferred company name")
role = st.text_input("Role", placeholder="Enter your preferred role")
name = st.text_input("Name of Candidate", placeholder="Enter your name")
hr_name = st.text_input("Name of Hiring Manager (Optional)", placeholder="Enter HR name if known")
email = st.text_input("Email", placeholder="Enter your email")

upload_file = st.file_uploader("Upload your resume here", type="pdf")

if upload_file is not None:
    bytes_data = io.BytesIO(upload_file.getvalue())
    pdf_reader = PdfReader(bytes_data)

    text = ""
    # loop to iterate over the pdf document that we upload
    for page in pdf_reader.pages:
        text += page.extract_text()

    if company and role and text:
        # print("Company entered:", company)
        # print("Role entered:", role)
        if st.button("Generate Cover Letter"):  # Check if the button is clicked
            with st.spinner("Generating your cover letter"):
                generated_response = create_cover_letter(company=company, role=role, resume=text, name=name,
                                                         hr_name=hr_name, email=email)
                st.success('Your cover letter has been generated')
                st.text_area("Your cover letter", generated_response, height=400)
                # to download the generated cover letter
                st.download_button("Download the cover letter", data=generated_response,
                                   file_name=f"cover_letter_{company}_{role}.txt",
                                   mime="text/plain")

    else:
        st.info("Please upload your resume pdf file")
