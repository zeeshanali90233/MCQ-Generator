import PyPDF2
import json


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()
            return text
        except Exception as e:
            raise Exception("Error while reading PDF file")
    elif file.name.endswith(".txt"):
        try:
            text = file.read().decode("utf-8")
            return text
        except Exception as e:
            raise Exception("Error while reading TXT file")
    else:
        raise Exception("Unsupported file format, only PDF and TXT files are supported")
    
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
