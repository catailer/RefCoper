import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import re

def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            laparams = LAParams()
            converter = TextConverter(resource_manager, fake_file_handle,laparams=laparams)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()

def extract_text(pdf_path):
    result=""
    for page in extract_text_by_page(pdf_path):
        result=result+page
        print(1)
    return result

def get_references(article):
    references=[]
    start=False
    tmp=""
    for line in article.splitlines( ):
        if start:
            if re.match("(\\[).*?(\\])", line, flags=0):
                references.append(tmp)
                tmp=line
            else:
                tmp=tmp+line
        if (line.strip().lower()=="references"):
            start=True
    return references



if __name__ == '__main__':
    article=extract_text('test/CCIS.pdf')
    references=get_references(article)
    print(references)
