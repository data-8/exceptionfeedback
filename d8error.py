from IPython.core.display import display, HTML, Markdown
import json
import os.path
import csv
import ipywidgets as widgets

class Announce:
    def __init__(self, etype, value):
        self.etype = etype
        self.value = value
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
            
        if not os.path.isfile("errorLog.csv"):
            with open('errorLog.csv', 'w', newline='') as f:
                
                fieldnames = ['errorType', 'errorMSG']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow({"errorType": self.errorname,"errorMSG": str(value)})
        else:
            with open('errorLog.csv', 'a', newline='') as f:
                
                fieldnames = ['errorType', 'errorMSG']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow({"errorType": self.errorname,"errorMSG": str(value)})
        
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
        display(Markdown("Please fill this quick survey to help us improve the the error feedback [Data 8 Error Feedback Survey](https://forms.gle/6UZQjwZmAxVDMsBR6)"))

        storage = [0, ""]

        dropdown_label = widgets.Label(value="Was this feedback helpful?")
        dropdown = widgets.Dropdown(options=[('', -1),
                                             ('Extremely helpful', 5),
                                             ('Very helpful', 4),
                                             ('Somewhat helpful', 3),
                                             ('Slightly helpful', 2),
                                             ("Wait, that was English?", 1)],
                                    value=-1)
        def handle_slider_change(change):
            storage[0] = dropdown.value
            accordion.selected_index = 1           
        dropdown.observe(handle_slider_change)
        first_page = widgets.VBox([dropdown_label, dropdown])

        textbox_label = widgets.Label(value="How was this feedback useful?")
        textbox = widgets.Text(value="",
                               placeholder="Press enter to submit.",
                               layout=widgets.Layout(width='50%', margin='0px', padding='0px'))
        submitted_label = widgets.Label(value="Thank you for your feedback!")
        submitted_label.layout.visibility = 'hidden'
        def submit_text(t):
            submitted_label.layout.visibility = 'visible'
            storage[1] = t.value
            accordion.selected_index = None
        textbox.on_submit(submit_text)
        second_page = widgets.VBox([textbox_label, textbox, submitted_label])

        accordion = widgets.Accordion([first_page, second_page])
        display(accordion)
        return storage

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

if not os.path.isfile("errorLog.csv"):
    with open('errorLog.csv', 'w', newline='') as f:
        fieldnames = ['errorType', 'errorMSG']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
#s
