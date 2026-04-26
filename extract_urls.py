import zipfile, xml.etree.ElementTree as ET, re
with zipfile.ZipFile('Lab_4_5_6.docx') as docx:
    xml_content = docx.read('word/document.xml')
    tree = ET.fromstring(xml_content)
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    texts = [node.text for node in tree.iterfind('.//w:t', namespaces) if node.text]
    full_text = ''.join(texts)
    urls = re.findall(r'https?://[^\s<>\"\'()]+', full_text)
    for url in set(urls):
        print(url)
