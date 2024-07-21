import os
import PyPDF2
import json
import traceback
 


def read_file(file):
    if(file.name.endswith(".pdf")):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error while reading pdf file")
    elif(file.name.endswith(".txt")):
      return file.read().decode("utf-8")
    else:
        raise Exception("UnSupported file format, only pdf and txt file is supported")  


def get_table_data(quiz_str):

    quiz_dict=eval(str(quiz_str))
    try:
        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value['mcq']
            options = " | ".join(
                [f"{option}: {option_value}" for option, option_value in value['options'].items()]
            )
            correct = value['correct']
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    except json.JSONDecodeError as e:
        raise Exception(f"Error decoding JSON from quiz string: {e}")
    except KeyError as e:
        raise Exception(f"Missing expected key in quiz data: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while processing quiz data: {e}")
