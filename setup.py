from setuptools import find_packages,setup


setup(
    name="mcqgenerator",
    version="0.0.1",
    author="Zeeshan Ali",
    author_email="zeeshanali90233@gmail.com",
    install_requires=['openai','langchain','streamlit','python-dotenv','PyPDF'],
    packages=find_packages()
)