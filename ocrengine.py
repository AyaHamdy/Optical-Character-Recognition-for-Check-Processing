from paddleocr import PaddleOCR

def create_ocr():
    #read ocr models
    def ocr_text(image):
        ocr = PaddleOCR(det_model_dir='models/det/en/en_PP-OCRv3_det_infer',
                        rec_model_dir='models/rec/en/en_PP-OCRv4_rec_infer',
                        cls_model_dir='models/cls/ch_ppocr_mobile_v2.0_cls_infer',use_angle_cls=True, lang="en",show_log=False)  # need to
        output=[]
        result = ocr.ocr(image,cls=True)
        for idx in range(len(result)):
            res = result[idx]
        for line in res:
            output.append(line[-1][0])
        return output

    #search for amount pattern 
    #Ex: #25,00#
    def get_amount(text):
        amount = [item[1:-1] for item in text if item.startswith('#') and item.endswith('#')]
        if amount:
            return amount
        return "cannot recognize amount"
    #search for checkno
    def get_checkNo(text):
        index = [idx for idx, s in enumerate(text) if 'CHEQUE' in s][0]
        checknum=text[index-1]
        if checknum:
            return checknum
        return "cannot recognize checkno"
    #read image and return ocr result
    def ocr_engine(image):
        ocrResult=ocr_text(image)
        print(ocrResult)
        amount= get_amount(ocrResult)
        checknum=get_checkNo(ocrResult)
        return  {'Amount':amount,'Check No':checknum}
    return ocr_engine
