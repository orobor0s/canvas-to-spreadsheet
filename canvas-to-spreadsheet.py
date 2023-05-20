'''
After you run this program, all you need to do is type get_responses(assignment_id,file_name,request_type) into the shell
in order to generate a csv file that can then be imported into excel or google sheets

assignment_id refers to the unique identifier at the end of the assignment's url, for example:
https://canvas.vt.edu/courses/136516/assignments/1074777 <- this number right here

file_name refers to whatever you'd like the generated file to be called,
and no need to worry about adding '.csv' to the end, that's taken care of

request_type refers to what type of information you want to be included,
as is explained further down / when you run the program

make sure to wrap both of the variables in '' when you enter them, for example:
get_responses('1074777','Journal 1','responses')

then all you need to do is access the generated file and you're good to go!
'''

# Details needed to access your school's Canvas, your Account, and your Course
API_URL = ''    # TODO: Your Canvas URL (Ex: "https://school.instructure.com")
API_KEY = ''    # TODO: Your Canvas API key for the URL (Ex: "hjOyO8TQpVb5D4R1ygrMnTl0eO7QNp7y6QnfQkIMBeaMVv2KYRnEYrlN1rtW18Jv")
COURSE_ID =     # TODO: Your course ID from Canvas URL (Ex: the 12345 from https://school.instructure.com/courses/12345/)


# need canvasapi installed, use pip install canvasapi
from canvasapi import Canvas
# Canvas API Docs/info:
# See: https://canvasapi.readthedocs.io/en/latest/getting-started.html
# And: https://github.com/ucfopen/canvasapi/


# This is to strip the html tags off the responses
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# need pandas installed, use pip install pandas
import pandas as pd


# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
# Get a course object for this course
course = canvas.get_course(COURSE_ID)

print("Please enter the assignment id you would like to aggregate \n\
responses for, the file name you'd like to save them to, \n\
and select any additional information you'd like included \n\n\
'responses' for just the responses \n\
'ids' for responses + student ids \n\
'dates' for responses + student ids + submission date \n\n\
for instance: get_responses('1074777','Journal 1','responses')"
)
    

def get_responses(assignment_id,file_name,request_type):

    #selecting the correct assignment / submissions to pull from
    assignment = course.get_assignment(assignment_id)
    submissions = assignment.get_submissions()

    responses = []
    clean_responses = []
    ids = []
    date = []

    # compiling the responses into a list
    for a in assignment.get_submissions(include=['user_id','submitted_at_date','body']):
        if a.body != None:
            ids.append(str(a.user_id))
            date.append(str(a.submitted_at_date))
            responses.append(a.body)

    # getting rid of Null values
    responses = list(filter(None,responses))

    # stripping the html tags
    for i in responses:
        x = strip_tags(i)

        clean_responses.append(x)


    # dictionary of lists
    if request_type == "responses":
        dict = {'responses': clean_responses}
    elif request_type == "ids":
        dict = {'id': ids, 'responses': clean_responses}
    elif request_type == "dates":
        dict = {'ids': ids, 'dates': date, 'responses': clean_responses}
    else:
        print('Please enter a valid request type')

    df = pd.DataFrame(dict)
        
    # saving the dataframe 
    df.to_csv(file_name + '.csv',index=False) 

    print('Complete')