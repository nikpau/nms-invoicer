# Invoicer Slack Bot

Welcome to the Invoicer. This is a spending tracker bot that lets you enter spendings for a project or event using a modal dialog. After the submission of the spending data a formatted LaTeX report is automatically generated or updated, depending whether the report for the given event already existed or not. 

## Blueprint

[logo]: https://github.com/nikpau/nms-invoicer/blob/main/doc/img/modal.png

Upon pressing the corresponding button you will be greeted with this modal: 

![modal][logo]

Before the modal is constructed the `get_eventlist()` function in the `helper.py` file pulls a list of current events or projects from an arbitrary source and transforms it into a list which is then parsed to construct the modal (currently this function is just a dummy). Then the user can select any of the pulled events to submit a spending notice. 

### Basic input checks

Currently there exists some basic input checking only for the `Wie viel Geld hast du ausgegeben?` field, which checks for any non-integer inputs as well as the number of decimal places of the entered amount. 

> TODO: At the moment it is possible to enter submission dates that lie in the future. This needs to be fixed. 

### After submission

After the user presses the `Einreichen` button, the modal diappears and the user interaction is completed. 

> TODO: It may be useful to construct a confirmation modal that pops up upon successful submission.

Internally, the bots checks whether there already exists a data file for the event/project the invoice was submitted for. If no file exists a new one is created and stored under `db/myevent.data`, if it did exist the newly entered data is appended to the file. 

The data file then gets passed to a LaTeXBuilder Class that reads the data file and builds a pdf file containing an overview over all spendings related to the event/project and stores it to the `out` folder named after the event as `myevent.pdf`.

> Note: The LaTeXBuilder spawns a subprocess calling pdflatex directly. Make sure to have pdflatex with any modern TeX distribution installed; otherwise the script just crashes. It's not too bad though as the submitted data is not lost as the data will be saved independendly of the Builder, and therefore will be integrated into the document during the next functioning run.
