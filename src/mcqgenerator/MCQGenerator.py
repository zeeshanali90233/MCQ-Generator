import os 
from langchain_openai  import ChatOpenAI
from dotenv import load_dotenv
# Langchain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain,SequentialChain

# Load Env Variables
load_dotenv() 

KEY=os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(openai_api_key=KEY,model_name="gpt-3.5-turbo",temperature=0.7)

QUIZ_TEMPLATE=  """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below as use it as a guide 
Ensure to make {number} mcqs
###Response_JSON
{response_json}
"""

# Input and Output Prompt Designing
quiz_generation_prompt=PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=QUIZ_TEMPLATE
)

quiz_chain=LLMChain(llm=llm,prompt=quiz_generation_prompt,output_key="quiz",verbose=True)
# Few Short Prompt
REVIEW_TEMPLATE=  """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity 
if the quiz is not at per with the cognitive and analytical abilities of the students, 
update the quiz questions which needs to be changed and change the tone such that is perfectly fits the student Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

# Input and Output Prompt Designing
review_prompt=PromptTemplate(
    input_variables=['subject','quiz'],
    template=REVIEW_TEMPLATE
)


review_chain=LLMChain(llm=llm,prompt=review_prompt,output_key="review",verbose=True)

generate_evaluate_chain=SequentialChain(chains=[quiz_chain,review_chain],input_variables=['text','number','subject','tone','response_json'],output_variables=['quiz','review'],verbose=True)

