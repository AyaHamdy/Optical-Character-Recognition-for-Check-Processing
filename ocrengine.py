from easyocr import Reader

def create_easyocr_reader():
    reader = Reader(lang_list=['en'], gpu=False)

    def easy_ocr(image):

        results = reader.readtext(image, detail=0)
        amount= [item for item in results if item.startswith('#') and item.endswith('#')]
        checkNum=results[results.index('CHEQUE NO')+1]
        return  {'Amount':amount[0],'Check No':checkNum}
    return easy_ocr
