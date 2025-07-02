import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#  Load environment variables
load_dotenv()

#  Streamlit app title
st.title("LeetCode Easy Problem Solver (Optimized) 🚀")

#  User inputs
problem_description = st.text_area("Enter the LeetCode Problem Description")
constraints = st.text_area("Enter the Constraints (Optional but better)")
language = st.selectbox("Choose Language", ["Python", "Java", "C++", "JavaScript"], index=0)

input_trigger = st.button("Generate Solution")

#  Prompt template
leetcode_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are an expert competitive programmer and software engineer. 
Your job is to write highly efficient, clean, and optimized solutions for coding problems.
The problem provided will be from LeetCode Easy difficulty.

Requirements:
- Write clean and readable code.
- Prioritize optimal time and space complexity.
- Add brief inline comments only where necessary.
- Avoid unnecessary code; keep it minimal and efficient.
- Return only the function code — no extra explanations, no main method.

If constraints allow, use the most efficient data structures 
(like sets, hashmaps, two pointers, or simple loops).
"""),
    ("user", 
     """Problem:
{problem_description}

Constraints:
{constraints}

Language: {language}

Return only the optimized function code.""")
])

# LLM instance (ensure Ollama server is running and model is correct)
llm = Ollama(model="llama3.2:latest")

# Output parser
output_parser = StrOutputParser()

# Create the chain
chain = leetcode_prompt | llm | output_parser

# Generate solution
if input_trigger and problem_description:
    with st.spinner("Generating solution..."):
        response = chain.invoke({
            "problem_description": problem_description,
            "constraints": constraints,
            "language": language
        })
    st.subheader("🧠 Optimized Solution:")
    st.code(response, language=language.lower())
