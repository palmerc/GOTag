import csv
import math
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Frame
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

return_address = """\
GO! Orchestra
Org nr. 922 581 762\
"""


class Instrument:
    def __init__(self, row):
        self.row = row

    def category(self):
        return self.row['Category']

    def model(self):
        return self.row['Model']

    def serial_no(self):
        return self.row['Serial NO']

    def size(self):
        return self.row['Size']

    def student(self):
        return self.row['Student']

    def print_please(self):
        return self.row['PRINT'] == 'TRUE'


def instruments_from_csv(csv_path):
    instruments = []
    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            instruments.append(Instrument(row))
    return instruments


def text_from_instrument(instrument):
    category = instrument.category()
    model = instrument.model()
    serial_no = instrument.serial_no()
    if len(serial_no) == 0:
        serial_no = 'N/A'
    size = instrument.size()
    student = instrument.student()

    return f"""\
    {category}
    
    {model}
    Serial Nr: {serial_no}
    Size: {size}

    {student}\
    """


def replace_new_lines(string):
    return string.replace('\n', '<br/>')


def address_style():
    style = ParagraphStyle(name='Address')
    style.fontName = 'Courier'
    style.fontSize = 12
    style.spaceAfter = 10
    return style


def body_style():
    style = ParagraphStyle(name='Body')
    style.fontName = 'Courier'
    style.fontSize = 12
    return style


def main():
    instruments = instruments_from_csv('./violin_inventory.csv')

    tag_width = 69 * mm
    tag_height = 98 * mm
    rows = 3
    cols = 3
    tag_index = 0
    page = 0

    canvas = Canvas('tuto1.pdf', pagesize=A4)
    canvas.setFont('Courier', 16)
    for instrument in instruments:
        if not instrument.print_please():
            continue
        if tag_index % (rows * cols) == 0:
            if page == 0:
                page = 1
            else:
                canvas.showPage()
                page += 1
                tag_index = 0

        inst_text = text_from_instrument(instrument)
        col = tag_index % cols
        row = math.floor(tag_index / cols)
        x = col * tag_width
        y = row * tag_height
        parts = []
        tag = Frame(x, y, tag_width, tag_height, showBoundary=1)
        parts.append(Paragraph(replace_new_lines(return_address), address_style()))
        parts.append(Paragraph(replace_new_lines(inst_text), body_style()))
        tag.addFromList(parts, canvas)
        tag_index += 1

    canvas.save()


if __name__ == '__main__':
    main()
