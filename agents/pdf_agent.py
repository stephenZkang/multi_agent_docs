import os
from core.vectordb import vectordb

def extract_text_pypdf2(path):
    from pypdf import PdfReader
    print(f"[extract_text_pypdf2] 开始解析: {path}")
    reader = PdfReader(path)
    texts = []
    for i, page in enumerate(reader.pages):
        print(f"[extract_text_pypdf2] 解析第{i+1}页: {page}")
        text = page.extract_text()
        if text:
            print(f"[extract_text_pypdf2] 第{i+1}页提取文本长度: {len(text)}")
            texts.append(text)
        else:
            print(f"[extract_text_pypdf2] 第{i+1}页无文本")
    print(f"[extract_text_pypdf2] 完成: 共{len(texts)}页有文本")
    return texts

def extract_text_pdfplumber(path):
    print(f"[extract_text_pdfplumber] 开始解析: {path}")
    import pdfplumber
    texts = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"[extract_text_pdfplumber] 解析第{i+1}页")
            text = page.extract_text()
            if text:
                print(f"[extract_text_pdfplumber] 第{i+1}页提取文本长度: {len(text)}")
                texts.append(text)
            else:
                print(f"[extract_text_pdfplumber] 第{i+1}页无文本")
    print(f"[extract_text_pdfplumber] 完成: 共{len(texts)}页有文本")
    return texts

def extract_text_fitz(path):
    print(f"[extract_text_fitz] 开始解析: {path}")
    import fitz  # PyMuPDF
    doc = fitz.open(path)
    texts = []
    for i, page in enumerate(doc):
        print(f"[extract_text_fitz] 解析第{i+1}页")
        text = page.get_text()
        if text:
            print(f"[extract_text_fitz] 第{i+1}页提取文本长度: {len(text)}")
            texts.append(text)
        else:
            print(f"[extract_text_fitz] 第{i+1}页无文本")
    print(f"[extract_text_fitz] 完成: 共{len(texts)}页有文本")
    return texts

def segment_text(text, strategy="paragraph", length=200):
    if strategy == "paragraph":
        return [p.strip() for p in text.split("\n") if p.strip()]
    elif strategy == "page":
        return [text]
    elif strategy == "fixed_length":
        segs = []
        t = text.replace("\n", " ")
        for i in range(0, len(t), length):
            segs.append(t[i:i+length])
        return segs
    else:
        return [text]

def run(input):
    """
    input: dict, 可选参数：
        model: 'pypdf2' | 'pdfplumber' | 'fitz'，默认 'pypdf2'
        segment: 'paragraph' | 'page' | 'fixed_length'，默认 'paragraph'
        length: int, 固定长度分段时使用，默认200
    """
    model = input.get("model", "pypdf2")
    segment = input.get("segment", "paragraph")
    length = input.get("length", 200)
    print(f"[PDF_AGENT DEBUG] input: {input}")
    pdf_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "documents")
    extractors = {
        "pypdf2": extract_text_pypdf2,
        "pdfplumber": extract_text_pdfplumber,
        "fitz": extract_text_fitz
    }
    extractor = extractors.get(model, extract_text_pypdf2)
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_folder, filename)
            try:
                texts = extractor(path)
            except Exception as e:
                continue
            for page_num, text in enumerate(texts):
                segments = segment_text(text, strategy=segment, length=length)
                for seg in segments:
                    if seg.strip():
                        vectordb.add_text(seg.strip(), source=f"{filename} - 第 {page_num+1} 页")
    return {
        "status": f"所有 PDF 已处理并嵌入向量数据库，模型: {model}，分段策略: {segment}",
        "input": input.get("input", ""),
        "template": input.get("template", "default"),
        "llm_provider": input.get("llm_provider", "gemini")
    }
