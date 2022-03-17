from IPython.core.display import display, HTML, Markdown
import json
import os.path
import csv
import ipywidgets as widgets
import datetime
import traceback
from IPython.display import clear_output
import webbrowser
from IPython.display import Javascript
import functools
import iwut

class Announce:
    """error index, serves as an id on the csv file"""
    eindex = 0

    def __init__(self, etype, value, tb, tb_offset=None):
        self.eindex = Announce.eindex
        Announce.eindex += 1
        self.etype = etype
        self.value = value
        self.feedbackRating = 0
        self.feedbackMSG = ""
        self.errorname = str(etype().__class__.__name__)
        self.tb = tb
        self.tb_offset = tb_offset
        self.resourceList = {}
        with open("errorConfig.json", "r") as f:
            diction = json.load(f)
        exceptionClass = diction.get(self.errorname)
        prewrittenMessge = False
        
        if exceptionClass is None:
            self.print = False
        else:
            self.print = True
            for i in exceptionClass:
                key, items = list(i.items())[0]
                if (key in str(value)):
                    prewrittenMessge = True
            self.print = prewrittenMessge

        # this generates a semi-readable summary of the traceback, which includes some information about the python code that caused the error
        summary = traceback.format_exc().splitlines()
        
        # iterate through traceback object to extract linenumber and bytecode of the first two frames
        curr_tb = tb.tb_next # skip the first frame which is the jupyter notebook frame

        # get code from jupyter notebook
        self.codeToLinenos = []

        while curr_tb and len(self.codeToLinenos) < 2:
            code = self.parseTraceback(curr_tb)
            self.codeToLinenos.append((code, curr_tb.tb_lineno))
            curr_tb = curr_tb.tb_next
            
        mode = 'w' if not os.path.isfile("errorLog.csv") else 'a'
        if os.path.isfile("errorLog.csv") and Announce.eindex == 1:
            with open("errorLog.csv", 'r') as f:
                for row in csv.reader(f):
                    self.eindex = int(row[0])
                self.eindex += 1
                Announce.eindex = self.eindex + 1
        
        with open('errorLog.csv', mode, newline='') as f:
            fieldnames = ['index', 'errorType', 'errorMSG', 'feedbackRating', 'feedbackMSG', 'time', 'codeToLinenos', 'traceSummary']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({"index": self.eindex,
                            "errorType": self.errorname,
                            "errorMSG": str(self.value),
                            "feedbackRating": self.feedbackRating,
                            "feedbackMSG": self.feedbackMSG,
                            "time": str(datetime.datetime.now()),
                            "codeToLinenos": self.codeToLinenos, 
                            "traceSummary":summary})
    
    def parseTraceback(self, tb):
        return traceback.extract_tb(tb)[0].line

    def tips(self):
        etype = self.etype
        value = self.value
        with open("errorConfig.json", "r") as f:
            diction = json.load(f)
        exceptionClass = diction.get(self.errorname)
        if exceptionClass is not None:
            self.default()
            
            for i in exceptionClass:
                key, items = list(i.items())[0]
                if (key in str(value)):
                    c=1
                    for j in items.get("helptext"):
                        display(Markdown(str(c)+". "+j))
                        c += 1
    def data8(self):
        display(Markdown("The Data 8 Reference might be helpful to look over for examples and usage: [Data 8 Reference](http://data8.org/fa21/python-reference.html)"))
    def furtherTips(self):
        display(Markdown("If you are having more trouble please feel free to consult a staff member at [Office Hours](https://oh.data8.org)\
                        \n or see the error message below "))
    def print(self, i):
        display(Markdown)
    def title(self):
        "## **There seems to be a <font color='red'>" + self.errorname+ "<font>**" + "."
        display(Markdown("## **" + self.errorname + "**" + "<font size = '3px'>" + ",  line " + str(self.codeToLinenos[0][1]) + "<font>"))
    def default(self):
        display(Markdown("Here are some possible reasons for your error:"))
    def resources(self):
        """Generate helpful resources"""
        display(Markdown("Still stuck? Here's some useful resources:"))
        self.resourceList = {'Textbook': 'http://data8.org/zero-to-data-8/textbook.html', 'Data 8 Reference': 'http://data8.org/fa21/python-reference.html', 'Office Hours': 'https://oh.data8.org/'}
        self.makeResources()
    def makeResources(self):
        """Helper method for creating resource buttons based on the resource list for error"""
        buttons = []
        for text in self.resourceList.keys():
            currButton = widgets.Button(description=text,icon="square")
            buttons.append(currButton)
        output = widgets.Output()
        h1 = widgets.HBox(buttons)
        display(h1)

        def button_click(b1, url):
            """clicking button sends you to resource URL"""
            with output:
                webbrowser.open(url)
        
        # Configure button on click functions for each of the resources
        count = 0
        for resPair in (self.resourceList.items()):
            buttons[count].on_click(functools.partial(button_click, url=resPair[1]))
            count += 1

    def feedback(self):
        def overwriteRow():
            """rewrites the feedbackRating & feedbackMSG columns on errorLog.csv"""
            with open("errorLog.csv", 'r') as f:
                reader = csv.reader(f, delimiter=',')
                lines = []
                for line in reader:
                    if line[0] == str(self.eindex):
                        line[3] = self.feedbackRating
                        line[4] = self.feedbackMSG
                    lines.append(line)
            with open("errorLog.csv", 'w', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerows(lines)

        """create & label a dropdown menu"""
        dropdown_label = widgets.Label(value="Was the message you saw useful?")
        dropdown = widgets.Dropdown(options=[('', 0),
                                             ('Extremely useful', 5),
                                             ('Very useful', 4),
                                             ('Somewhat useful', 3),
                                             ('Slightly useful', 2),
                                             ('Not at all useful', 1)],
                                    value=0)
        def handle_slider_change(change):
            """on change: rewrites the feedbackRating in the CSV"""
            self.feedbackRating = dropdown.value
            overwriteRow()
        dropdown.observe(handle_slider_change)

        """create & label a textbox"""
        textbox_label = widgets.Label(value="Any other feedback?")
        textbox = widgets.Text(value="",
                               placeholder="Press enter to submit.",
                               layout=widgets.Layout(width='50%', margin='0px 8px 0px 0px', padding='0px'))
        def submit_text(t):
            """on textbox submit: remove other fields and replace with a thank you message"""
            self.feedbackMSG = t.value
            accordion.children = [widgets.Label(value="Thank you for your feedback!")]
            overwriteRow()
        textbox.on_submit(submit_text)

        """create a submit button for the textbox"""
        submit_button = widgets.Button(description="Submit",
                                       layout=widgets.Layout(width='10%', min_width='80px'))
        def on_btn_click(b):
            """on button click: submits textbox and replaces other fields with a thank you message"""
            submit_text(textbox)
        submit_button.on_click(on_btn_click)
        
        """bundle together widgets for a cleaner output"""
        dropdownBox = widgets.VBox([dropdown_label, dropdown])
        submitBox = widgets.HBox([textbox, submit_button])
        submitBox.layout.align_items = 'center'
        textboxBox = widgets.VBox([textbox_label, submitBox])
        output = widgets.VBox([dropdownBox, textboxBox])
        accordion = widgets.Accordion([output])
        accordion.set_title(0, '  Feedback Form')

        display(accordion)

def test_exception(self, etype, value, tb, tb_offset=None):
    try:
        announce = Announce(etype, value, tb, tb_offset)
        if announce.print:
            announce.title()
            display(iwut.get_wut_traceback(etype, value, tb, tb_offset))
            announce.tips()
            announce.resources()
            announce.feedback()
    except: 
        display(iwut.get_wut_traceback(etype, value, tb, tb_offset))
    
get_ipython().set_custom_exc((Exception,), test_exception)
