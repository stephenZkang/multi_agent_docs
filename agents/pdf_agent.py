import os
from core.vectordb import vectordb
import json
import hashlib

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

# 保证data目录存在
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
CACHE_PATH = os.path.join(DATA_DIR, "pdf_status.cache")

def get_pdf_status(pdf_folder):
    status = {}
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_folder, filename)
            stat = os.stat(path)
            status[filename] = stat.st_mtime
    return status

def status_hash(status):
    # 生成唯一hash用于比较
    return hashlib.md5(json.dumps(status, sort_keys=True).encode()).hexdigest()

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

    # 检查PDF状态缓存
    current_status = get_pdf_status(pdf_folder)
    current_hash = status_hash(current_status)
    cache_hash = None
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            cache_hash = f.read().strip()
    if cache_hash == current_hash:
        print("[PDF_AGENT] PDF未变化，跳过解析。")
        return {
            "status": "PDF未变化，未重新解析。",
            "input": input.get("input", ""),
            "template": input.get("template", "default"),
            "llm_provider": input.get("llm_provider", "gemini")
        }
    # 有变化，清空向量库并重新解析
    print("[PDF_AGENT] 检测到PDF有变化，重新解析并重建向量库。")
    vectordb.clear()
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
    # 更新缓存
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        f.write(current_hash)
    return {
        "status": f"所有 PDF 已处理并嵌入向量数据库，模型: {model}，分段策略: {segment}",
        "input": input.get("input", ""),
        "template": input.get("template", "default"),
        "llm_provider": input.get("llm_provider", "gemini")
    }
