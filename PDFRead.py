import PyPDF2
import re
def extract_courses(pdf_path):
    courses_by_quarter = {}
    quarter_pattern = re.compile(r'\d{4} (Summer|Fall|Winter|Spring) Quarter')
    course_pattern = re.compile(r'([A-Z]+ \d+[A-Z]?) (.+?) \d+\.\d+ \d+\.\d+ [A-Z\+\-]? \d+\.\d+')

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        current_quarter = None

        for page in reader.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    quarter_match = quarter_pattern.search(line)
                    if quarter_match:
                        current_quarter = quarter_match.group()
                        courses_by_quarter[current_quarter] = []
                    
                    course_match = course_pattern.search(line)
                    if course_match and current_quarter:
                        course_code, course_name = course_match.groups()
                        courses_by_quarter[current_quarter].append(f"{course_code} - {course_name}")

    return courses_by_quarter

pdf_path = "./SSR_TSRPT.pdf"
courses = extract_courses(pdf_path)

for quarter, course_list in courses.items():
    print(f"\n{quarter}:")
    for course in course_list:
        print(f"  {course}")
