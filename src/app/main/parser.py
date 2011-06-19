# -*- encoding: utf8 -*-
from lib.docx import opendocx, nsprefixes
import re
from lxml.etree import tounicode
import pprint
"""
Parser get docx file and return list of questions.
Question has this structure:
{
    'question': u'<Question>',
    'text_answer': u'<Answer>',
    'answers: [{
        'text': u'<Answer>',
        'correct': True/False
    },...]
}
If text_answer, asnwers choices are ignored
"""
text_answer_re = re.compile(r'\(\*(.+)\*\)')

def parser(file):
    """
    № 5
    У якій відповіді правильно вказано, що є кримінально-процесуальною формою: 
    передбачена законом система стадії кримінального процесу; 
    передбачені законом засоби контролю за законністю та обґрунтованістю всіх процесуальних дій і рішень; 
     # передбачений законом порядок провадження у кримінальній справі в цілому, порядок і послідовність виконання необхідних процесуальних дій та прийняття відповідних рішень; 
    передбачені законом процесуальні засоби і способи викриття винних у вчиненні злочину осіб; 
    зміст процесуальних дій і прийнятих рішень та їх форма.
    
    № 141, 0, 2, 1, 4, 60
    Вкажіть рік прийняття Кримінально-процесуального кодексу України: (*1960*)    
    """
    doc = opendocx(file)

    questions_data = []

    for p in doc.xpath('/w:document/w:body/w:p', namespaces=nsprefixes):
        t = p.xpath('w:r/w:t', namespaces=nsprefixes)
        if len(t):
            questions_data.append([i.text.strip() for i in t])
       
    questions = []

    for qs_data in questions_data:
        num = ''
        if qs_data[0].startswith(u'№'):
            assert len(qs_data[0]) == 1
            num = qs_data[1]
            qs_data = qs_data[2:]
  
        data = {
            'question': qs_data[0],
            'text_answer': u'',
            'answers': []
        }
        
        for answer in qs_data[1:]:
            if answer.startswith('#'):
                data['answers'].append({
                    'text': answer[1:],
                    'correct': True
                })
            else:
                data['answers'].append({
                    'text': answer,
                    'correct': False
                })
                        
        if data['answers']:
            questions.append(data)
        else:
            r = text_answer_re.search(data['question'])
            if r:
                data['text_answer'] = r.groups()[0]
                data['question'] = text_answer_re.sub('', data['question'])
                questions.append(data)
        
        assert len(data['answers']) or data['text_answer'], 'Question: %s' % num
        
    return questions

def parser3(file):
    """
    № 9, 0, 1, 1, 1, 90
    Особлива частина кримінального права України включає в себе норми таких видів:
    -одноразові;
    -похідні;
    +заохочувальні;
    -про помилування;
    -каральні.
    
    № 1249, 0, 18, 2, 4, 180
    Підставте відповідні цифри у вказану формулу і впишіть лише результат: А + Б, 
    де А - під незаконною винагородою у значному розмірі в злочині 
    “Одержання незаконної винагороди працівником державного підприємства, установи чи організації” 
    слід розуміти незаконну винагороду, яка в ________ і більше разів перевищує 
    неоподатковуваний мінімум доходів громадян; Б – кількість форм вини, з якими 
    вчинюються злочини проти авторитету органів державної влади, органів місцевого 
    самоврядування та об’єднань громадян. (*3*)
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
        num = ''
        if qs_data[0].startswith(u'№') or qs_data[0].startswith(u'#'):
            num = qs_data[0]
            qs_data = qs_data[1:]
  
        data = {
            'question': qs_data[0],
            'text_answer': u'',
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
        else:
            r = text_answer_re.search(data['question'])
            if r:
                data['text_answer'] = r.groups()[0]
                data['question'] = text_answer_re.sub('', data['question'])
                questions.append(data)
        
        #Uncommen for debuging and checking all questions
        #assert len(data['answers']) or data['text_answer'], 'Question: %s' % num
    
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