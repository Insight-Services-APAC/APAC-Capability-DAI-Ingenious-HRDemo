import json
import PyPDF2

def pdf_to_json(pdf_path):
    pdf_reader = PyPDF2.PdfReader(open(pdf_path, 'rb'))
    pdf_content = {}

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_content[f'Page_{page_num + 1}'] = page.extract_text()

    return json.dumps(pdf_content, indent=4)

if __name__ == "__main__":
    pdf_path = './ingenious_extensions/uploads/cv_senior_data_specialist_notsuitable.pdf'
    json_content = pdf_to_json(pdf_path)
    with open('cv_senior_data_specialist_notsuitable.json', 'w') as json_file:
        json_file.write(json_content)
    
    with open('cv_senior_data_specialist_notsuitable.json', 'rb') as json_file:
        criteria  = json.load(json_file)
    
    print(criteria)