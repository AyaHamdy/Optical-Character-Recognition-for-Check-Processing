from easyocr import Reader
import checkpreprocessing
def create_easyocr_reader():
    reader = Reader(lang_list=['en'], gpu=False)
    #preprocessing check to improve ocr results for check number part
    def check_preprocessing(image):
        images=checkpreprocessing.segmentation_detection(image)
        return images
    #use easy ocr engine for ocr
    def easy_ocr(image):
        results = reader.readtext(image, detail=0)
        return results

    #search for amount pattern 
    #Ex: #25,00#
    def search_amount(text):
        amount = [item[1:-1] for item in text if item.startswith('#') and item.endswith('#')]
        if amount:
            return amount
        return amount
    #read image and return ocr result
    def ocr_engine(image):
        fullimage,num=check_preprocessing(image)
        checknum=easy_ocr(num)
        text=easy_ocr(fullimage)
        amount= search_amount(text)
        return  {'Amount':amount[0],'Check No':checknum[0]}
    return ocr_engine
