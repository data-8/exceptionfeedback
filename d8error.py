from IPython.core.display import display, HTML, Markdown
import json
import os.path
import csv
import ipywidgets as widgets

class Announce:
    eindex = 0
    def __init__(self, etype, value):
        self.eindex = Announce.eindex
        Announce.eindex += 1
        self.etype = etype
        self.value = value
        self.feedbackRating = 0
        self.feedbackMSG = ""
        self.errorname = str(etype().__class__.__name__)
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

        def writeRow(file):
            fieldnames = ['index', 'errorType', 'errorMSG', 'feedbackRating', 'feedbackMSG']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({"index": self.eindex,
                            "errorType": self.errorname,
                            "errorMSG": str(self.value),
                            "feedbackRating": self.feedbackRating,
                            "feedbackMSG": self.feedbackMSG})
            
        if not os.path.isfile("errorLog.csv"):
            with open('errorLog.csv', 'w', newline='') as f:
                writeRow(f)
        else:
            if Announce.eindex == 1:
                with open("errorLog.csv", 'r') as f:
                    for row in reversed(list(csv.reader(f))):
                        self.eindex = int(row[0]) + 1
                        break
                    Announce.eindex = self.eindex + 1
            with open('errorLog.csv', 'a', newline='') as f:
                writeRow(f)
    
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
        display(Markdown("## **Uh-o it seems we have an error!**"))
    def default(self):
        display(Markdown("It seems we have a "+self.errorname+ ". " +self.errorname+ "s are usually because of:"))
    def feedback(self):
        def overwriteRow():
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

        dropdown_label = widgets.Label(value="Was this feedback helpful?")
        dropdown = widgets.Dropdown(options=[('', 0),
                                             ('Extremely helpful', 5),
                                             ('Very helpful', 4),
                                             ('Somewhat helpful', 3),
                                             ('Slightly helpful', 2),
                                             ("Wait, that was English?", 1)],
                                    value=-1)
        def handle_slider_change(change):
            self.feedbackRating = dropdown.value
            accordion.selected_index = 1
            overwriteRow()

        dropdown.observe(handle_slider_change)
        first_page = widgets.VBox([dropdown_label, dropdown])

        textbox_label = widgets.Label(value="How was this feedback useful?")
        textbox = widgets.Text(value="",
                               placeholder="Press enter to submit.",
                               layout=widgets.Layout(width='50%', margin='0px', padding='0px'))
        def submit_text(t):
            self.feedbackMSG = t.value
            textbox.layout.visibility = 'hidden'
            dropdown.layout.visibility = 'hidden'
            textbox_label.value = dropdown_label.value = "Thank you for your feedback!"
            accordion.selected_index = None
            overwriteRow()
        textbox.on_submit(submit_text)
        second_page = widgets.VBox([textbox_label, textbox])

        accordion = widgets.Accordion([first_page, second_page])
        display(accordion)

def test_exception(self, etype, value, tb, tb_offset=None):
    try:
        announce = Announce(etype, value)
        if announce.print:
            announce.title()
            announce.tips()
            announce.data8()
            announce.furtherTips()
            announce.feedback()
        self.showtraceback((etype, value, tb), tb_offset=tb_offset)
    except:
        self.showtraceback((etype, value, tb), tb_offset=tb_offset)
    
get_ipython().set_custom_exc((Exception,), test_exception)
