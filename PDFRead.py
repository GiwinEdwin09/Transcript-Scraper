import PyPDF2
import json

# Array of all course codes
course_codes = [
    'ACEN', 'AM', 'ANTH', 'APLX', 'ARBC', 'ART', 'ARTG', 'ASTR', 'BIOC', 'BIOE', 
    'BIOL', 'BME', 'CHEM', 'CHIN', 'CLNI', 'CLST', 'CMMU', 'CMPM', 'COWL', 'CRES', 
    'CRSN', 'CT', 'CRWN', 'CSE', 'CSP', 'DANM', 'EART', 'ECE', 'ECON', 'EDUC', 
    'ENVS', 'ESCI', 'FIL', 'FILM', 'FMST', 'FREN', 'GAME', 'GCH', 'GERM', 'GIST', 
    'GRAD', 'GREE', 'HAVC', 'HEBR', 'HISC', 'HIS', 'HCI', 'HUMN', 'ITAL', 'JAPN', 
    'JRLC', 'JWST', 'KRSG', 'LAAD', 'LALS', 'LATN', 'LGST', 'LING', 'LIT', 'MATH', 
    'MERR', 'METX', 'MSE', 'MUSC', 'NLP', 'OAKS', 'OCEA', 'PBS', 'PERS', 'PHIL', 
    'PHYE', 'PHYS', 'POLI', 'PORT', 'PRTR', 'PSYC', 'PUNJ', 'RUSS', 'SCIC', 'SOCD', 
    'SOCY', 'SPAN', 'SPHS', 'STAT', 'STEV', 'THEA', 'TIM', 'UCDC', 'VAST', 'WRIT', 
    'YIDD'
]

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def contains_any(main_string, string_array):
    return any(substring in main_string for substring in string_array)

def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if line.strip() and not line.startswith('***') and not line.startswith('Page:') and not line.startswith('Print Date:'):
            cleaned_lines.append(line.strip())
    return cleaned_lines

def parse_courses(cleaned_lines):
    courses_by_quarter = {}
    current_quarter = None
    all_grades = ["A", "B", "C", "D", "F", "P", "NP", "W", "I", "IP"]

    for line in cleaned_lines:
        # Check if the line indicates a new quarter
        if 'Quarter' in line:
            current_quarter = line
            courses_by_quarter[current_quarter] = []
        # Check if the line contains course information by searching for any course code
        elif current_quarter is not None and any(subject in line for subject in course_codes):
            # Split the line into parts
            parts = line.split()

            if len(parts) >= 4:
                # Extract course code (first part)
                course_code = ' '.join(parts[0:2])
                # Extract course name (everything between the course code and the credits)

                # Extract credits earned and grade
                if not contains_any(parts[-2], all_grades):
                    course_name = ' '.join(parts[2:-3])
                    credits_earned = parts[-2]
                    grade = "IP"
                else:
                    course_name = ' '.join(parts[2:-4])
                    credits_earned = parts[-3]
                    grade = parts[-2]

                # Add the course to the current quarter
                courses_by_quarter[current_quarter].append({
                    'course_code': course_code,
                    'course_name': course_name,
                    'credits_earned': credits_earned,
                    'grade': grade
                })
    return courses_by_quarter

def main(pdf_path, json_output_path):
    text = extract_text_from_pdf(pdf_path)
    cleaned_lines = clean_text(text)
    courses_by_quarter = parse_courses(cleaned_lines)

    # Save the courses to a JSON file
    with open(json_output_path, 'w') as json_file:
        json.dump(courses_by_quarter, json_file, indent=4)

    print(f"Course data has been saved to {json_output_path}")

if __name__ == "__main__":
    pdf_path = "./giwTranscript.pdf"
    json_output_path = "./courses_by_quarter.json"
    main(pdf_path, json_output_path)