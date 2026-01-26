import os
import shutil
from PyPDF2 import PdfReader

# ==========================================
SOURCE_DIR = r'/content/drive/MyDrive/PDFS' 
TARGET_DIR = r'/content/drive/MyDrive/PDFS/Organized_Library' 

# 분류 키워드 (필요에 따라 수정)
KEYWORDS_MAP = {
    'Spatial_Analysis': ['GIS', 'spatial', 'mapping', 'hotspot', 'distance', 'spatio-temporal'],
    'Criminology_Theory': ['theory', 'rational choice', 'social disorganization', 'strain', 'neighborhood', 'crime and place', 'spatial crime', 'crime'],
    'Quantitative_Criminology': ['intelligence', 'prediction', 'crime analysis', 'surveillance'],
    'Immigration_Crime': ['immigration', 'immigrant', 'assimilation', 'foreign', 'ethnic'],
    'Statistical_Methods': ['regression', 'causal', 'longitudinal', 'modeling', 'fourier', 'econometrics']
}

def extract_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for i in range(min(3, len(reader.pages))):
            text += reader.pages[i].extract_text()
        return text.lower()
    except:
        return ""

# organizing function
def organize_in_drive():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.pdf')]
    print(f"총 {len(files)} Articles Analyzing...")

    for filename in files:
        pdf_path = os.path.join(SOURCE_DIR, filename)
        content = extract_text(pdf_path)
        
        best_category = 'Unclassified'
        max_count = 0
        
        for category, keywords in KEYWORDS_MAP.items():
            count = sum(content.count(k.lower()) for k in keywords)
            if count > max_count:
                max_count = count
                best_category = category
        
        dest_folder = os.path.join(TARGET_DIR, best_category)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            
        # 안전을 위해 move 대신 copy를 사용합니다. 나중에 원본을 지우시면 됩니다.
        shutil.copy2(pdf_path, os.path.join(dest_folder, filename))
        print(f"✅ {filename} -> [{best_category}]")

organize_in_drive()