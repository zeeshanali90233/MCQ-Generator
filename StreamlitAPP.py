import json
import pandas as pd
import traceback
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

with open("./Response.json","r") as file:
    RESPONSE_JSON=json.load(file)
    
st.title("MCQs Creater Application with Langchain")

with st.form("user_inputs"):
    # File Upload
    uploaded_file=st.file_uploader("Upload a pdf or txt file")
    
    # Input Fields
    mcq_count=st.number_input("No.of MCQS" , min_value=3,max_value=50)
    subject=st.text_input("Insert Submit" ,max_chars=50)
    tone=st.text_input("Complexity level of questions" ,max_chars=20,placeholder="Simple")
    
    button=st.form_submit_button("Create MCQs")
    
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading"):
            try:
                print(uploaded_file)
                text=read_file(uploaded_file)
                # Count Tokens
                
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {"text":text,"number":mcq_count,"subject":subject,"tone":tone,"response_json":RESPONSE_JSON})
                
                
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")    
    
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")
                logging.info(f"Quiz Generated with Cost: {cb.total_cost}")
                if isinstance(response,dict):
                    quiz=response.get("quiz")
                    if quiz is not None:
                        tabled_quiz=get_table_data(quiz)
                        if tabled_quiz is not None:
                            df=pd.DataFrame(tabled_quiz)
                            df.index=df.index+1
                            st.table(df)
                            df.to_csv("MCQ_Response.csv")
                          
                            st.text_area(label="Review",value=response.get("review"))
                        else:
                            st.error("Error in the table data")
                
                else:
                    st.write(response)

with open('MCQ_Response.csv') as f:
    st.download_button('Download CSV', f,"MCQs.csv")