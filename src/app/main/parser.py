# -*- encoding: utf8 -*-
from lib.docx import opendocx, nsprefixes
from lxml.etree import tounicode
import pprint
"""
Parser get docx file and return list of questions.
Question has this structure:
{
    'question': u'<Question>'
    'answers: [{
        'text': u'<Answer>',
        'correct': True/False
    },...]
}
"""

def parser(file):
    """
    № 9, 0, 1, 1, 1, 90
    Особлива частина кримінального права України включає в себе норми таких видів:
    -одноразові;
    -похідні;
    +заохочувальні;
    -про помилування;
    -каральні.
    """
    doc = opendocx(file)

    questions_data = []
    data = []

    for p in doc.xpath('/w:document/w:body/w:p', namespaces=nsprefixes):
        t = p.xpath('w:r/w:t', namespaces=nsprefixes)
        if bool(t):
            data.append(u''.join([i.text for i in t]).replace(u'№', u'#').strip())
        else:
            len(data) and questions_data.append(data)
            data = []

    if len(data):
        questions_data.append(data)
       
    questions = []

    for qs_data in questions_data:
        if qs_data[0].startswith(u'№') or qs_data[0].startswith(u'#'):
            qs_data = qs_data[1:]
  
        data = {
            'question': qs_data[0],
            'answers': []
        }
        
        for answer in qs_data[1:]:
            answer = answer.strip()
            data['answers'].append({
                'text': answer[1:],
                'correct': answer.startswith('+')
            })
        
        if data['answers']:
            questions.append(data)
  
    return questions

def parser2(file):
    """
    № 2, 1, 1, 1, 120
    Якщо одна сторона бере на себе обов’язок перед другою стороною вчинити певні дії або утриматися від них, а друга сторона наділяється лише правом вимоги, без виникнення зустрічного обов’язку щодо першої сторони, то договір вважається :
    1) двостороннім;
    2) консенсуальним;
    3) реальним;
    4) одностороннім;
    5) недвостороннім.
    #4    
    """
    doc = opendocx(file)

    questions_data = []
    data = []

    for p in doc.xpath('/w:document/w:body/w:p', namespaces=nsprefixes):
        t = p.xpath('w:r/w:t', namespaces=nsprefixes)
        if bool(t):
            data.append(u''.join([i.text for i in t]).replace(u'№', u'#').strip())
        else:
            len(data) and questions_data.append(data)
            data = []

    if len(data):
        questions_data.append(data)
       
    questions = []

    for qs_data in questions_data:
        if qs_data[0].startswith(u'№') or qs_data[0].startswith(u'#'):
            qs_data = qs_data[1:]
            
        data = {
            'question': qs_data[0],
            'answers': []
        }
        
        correct = []
        for i in qs_data[-1][1:]:
            correct.append(int(i))

        for i, answer in enumerate(qs_data[1:-1]):
            data['answers'].append({
                'text': answer,
                'correct': i+1 in correct
            })
        
        questions.append(data)
        
    return questions

def parser1(file):
    doc = opendocx(file)
    
    questions_data = []
    data = []
    for p in doc.xpath('/w:document/w:body/w:p', namespaces=nsprefixes):
        if not bool(p.xpath('w:r/w:t', namespaces=nsprefixes)):
            if len(data):
                questions_data.append(data)
                data = []
        else:
            data.append(p)
    
    if len(data):
        questions_data.append(data)
    
    questions = []
    for qs_data in questions_data:
        data = {
            'question': u'',
            'answers': []
        }
        
        for r in qs_data[0].xpath('w:r/w:t', namespaces=nsprefixes):
            data['question'] += u'%s ' % r.text.strip()
        
        for p in qs_data[1:]:
            text = u''
            for r in p.xpath('w:r/w:t', namespaces=nsprefixes):
                text += u'%s ' % r.text.strip()  
            data['answers'].append({
                'text': text,
                'correct': bool(p.xpath('w:r/w:rPr/w:b', namespaces=nsprefixes))
            })                  
                    
        if data['answers']:
            questions.append(data)    