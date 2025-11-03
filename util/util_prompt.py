import pandas as pd
import ast
import math

subject_in_id = {
        'Tourism': 'Pariwisata',
        'Teacher Competency Test': 'Ujian Kompetensi Guru',
        'Advocate': 'Advokat',
        'Medical Doctor': 'Kedokteran',
        'Sharia Life Insurance': 'Asuransi Jiwa Syariah',
        'Nurse': 'Ilmu Keperawatan',
        'Clinical Psychology': 'Psikologi Klinis',
        'Life Insurance': 'Asuransi Jiwa',
        'Certified Financial Planner': 'CFP',
        'Midwife': 'Kebidanan',
        'Certified Public Accountant': 'CPA',
        'Certified Professional Management Accountant': 'CPMA',
        'Pharmacist': 'Apoteker',
        'Certified Indonesian Tax Accountant': 'Brevet AB',
        'Office Administration': 'Administrasi Perkantoran',
        'Hospitality': 'Perhotelan',
        'Broadcasting': 'Broadcasting',
        'Graphic Design': 'Desain Grafis',
        'Police': 'Kepolisian',
        'Cullinary Art': 'Tata Boga',
        'Fashion Design': 'Tata Busana',
        'Risk Management': 'Manajemen Resiko'
}

exam_type_in_id = {
        'Tourism': ' untuk level SMK',
        'Teacher Competency Test': '',
        'Advocate': ' untuk ujian sertifikasi',
        'Medical Doctor': ' untuk ujian kompetensi profesi',
        'Sharia Life Insurance': ' untuk ujian sertifikasi',
        'Nurse': ' untuk ujian kompetensi profesi',
        'Clinical Psychology': ' untuk ujian kompetensi profesi',
        'Life Insurance': ' untuk ujian sertifikasi',
        'Certified Financial Planner': ' untuk ujian sertifikasi',
        'Midwife': ' untuk ujian kompetensi profesi',
        'Certified Public Accountant': ' untuk ujian sertifikasi',
        'Certified Professional Management Accountant': ' untuk ujian sertifikasi',
        'Pharmacist': ' untuk ujian kompetensi',
        'Certified Indonesian Tax Accountant': ' untuk ujian sertifikasi',
        'Office Administration': ' untuk level SMK',
        'Hospitality': ' untuk level SMK',
        'Broadcasting': ' untuk level SMK',
        'Graphic Design': ' untuk level SMK',
        'Police': '',
        'Cullinary Art': ' untuk level SMK',
        'Fashion Design': ' untuk level SMK',
        'Risk Management': ' untuk ujian sertifikasi'
}

def get_option(row):
    option_str = ''
    number = 0
    for pilihan in ['A', 'B', 'C', 'D', 'E']:
        tmp = row[f'Option {pilihan}']
        if pd.isna(tmp) or tmp == '':
            break
        option_str += f'{pilihan}. {tmp.strip()}\n'
        number += 1
    return option_str, number


def prepare_data_id(dataset):
    if dataset == 'indocloze':
        inputs = []; answers = []; number_options = []
        PROMPT = 'Pilihlah kelanjutan dari kalimat berikut yang benar!\n\n[QUESTION]\n[OPTIONS]\nJawaban:'
        df = pd.read_csv('dataset/indocloze.csv')
        for idx, row in df.iterrows():
            premise_str = row['sentence-1'] + ' ' + row['sentence-2'] + ' ' + row['sentence-3'] + ' ' + row['sentence-4']
            option_str = f"A. {row['correct_ending']}\nB. {row['incorrect_ending']}"
            option_num = 2
            prompt_str = PROMPT.replace('[QUESTION]', premise_str).replace('[OPTIONS]', option_str)
            inputs.append(prompt_str)
            answers.append(0)
            number_options.append(option_num)
        return inputs, answers, number_options

    if dataset == 'maps':
        inputs = []; answers = []; number_options = []
        PROMPT = 'Perhatikan percakapan berikut!\n\n[QUESTION]\n[OPTIONS]\nJawaban:'
        df = pd.read_csv('dataset/maps.csv')
        for idx, row in df.iterrows():
            premise_str = row['conversation'] + '\n\nApakah arti dari ' + row['proverb'] + '?\n' 
            option_str = f"A. {row['answer1']}\nB. {row['answer2']}\n"
            option_num = 2
            prompt_str = PROMPT.replace('[QUESTION]', premise_str).replace('[OPTIONS]', option_str)
            inputs.append(prompt_str)
            answers.append({'a':0, 'b':1}[row['answer_key']])
            number_options.append(option_num)
        return inputs, answers, number_options
   
    if dataset == 'copal':
        inputs = []; answers = []; number_options = []
        df = pd.read_csv('dataset/copal.csv')
        for idx, row in df.iterrows():
            premise_str = row['premise'] + '\n\n'
            if row['question'] == 'effect':
                premise_str += 'Apa akibat yang paling mungkin timbul dari kejadian di atas?\n\n'
            elif row['question'] == 'cause':
                premise_str += 'Apa penyebab yang mengakibatkan kejadian di atas?\n\n'
            else:
                print('Error')
            option_str = f"A. {row['choice1']}\nB. {row['choice2']}\n"
            option_num = 2
            inputs.append(premise_str+option_str+'\nJawaban: ')
            answers.append(row['label'])
            number_options.append(option_num)
        return inputs, answers, number_options
    
    if dataset == 'indocareer':
        PROMPT = 'Ini adalah soal [SUBJECT][TYPE]. Pilihlah salah satu jawaban yang dianggap benar!\n\n[QUESTION]\n[OPTIONS]\nJawaban:'
        ids = []; inputs = []; answers = []; number_options = []
        data = pd.read_csv('dataset/indocareer.csv')

        for idx, row in data.iterrows():
            option_str, option_num = get_option(row)
            prompt_str = PROMPT.replace('[SUBJECT]', subject_in_id[row['Subject']]).\
                                replace('[TYPE]', exam_type_in_id[row['Subject']]).\
                                replace('[QUESTION]', row['Question']).\
                                replace('[OPTIONS]', option_str)

            ids.append(row['ID'])
            inputs.append(prompt_str)
            answers.append({'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}[row['Answer Key']])
            number_options.append(option_num)
        return inputs, answers, number_options

    if dataset == 'indoculture':
        PROMPT = 'Untuk konteks [LOKASI], sambungan yang tepat dari kalimat "[INPUT]" adalah\n[PILIHAN]\nJawaban: '

        ids = []; inputs = []; answers = []; number_options = []
        data = pd.read_csv('dataset/indoculture.csv')

        for idx, row in data.iterrows():
            location = 'propinsi ' + row['province']
            options = ast.literal_eval(row['options'])
            options_str = '\n'.join(options)
            options = [x[3:] for x in options]

            prompt_str = PROMPT.replace('[LOKASI]', location).\
                                replace('[INPUT]', row['context']).\
                                replace('[PILIHAN]', options_str)

            ids.append(row['id'])
            inputs.append(prompt_str)
            answers.append({'A': 0, 'B': 1, 'C': 2}[row['answer']])
            number_options.append(3)
        return inputs, answers, number_options

    if dataset == 'indommlu':
        PROMPT = 'Ini adalah soal [SUBJECT] untuk [LEVEL]. Pilihlah salah satu jawaban yang dianggap benar!\n\n[INPUT]\n[OPTION]\n\nJawaban: '
        inputs = []; answers = []; number_options = []
        data = pd.read_csv('dataset/indommlu.csv')
        key2id = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
        
        for idx, row in data.iterrows():
            if row['level'] == 'Seleksi PTN':
                level = 'seleksi masuk universitas'
            else:
                try:
                    level = f"{math.trunc(float(row['kelas']))} {row['level']}"
                except:
                    level = f"{row['kelas']} {row['level']}"

            inputs.append(
                PROMPT.replace('[SUBJECT]', row['subject']).\
                       replace('[LEVEL]', level).\
                       replace('[INPUT]', row['soal']).\
                       replace('[OPTION]',row['jawaban'])
            )
            answers.append(key2id[row['kunci']])
            number_options.append(len(row['jawaban'].split('\n')))
        return inputs, answers, number_options



def prepare_data_id_few_shot(dataset):
    if dataset == 'indocloze':
        inputs = []; answers = []; number_options = []
        PROMPT = 'Pilihlah kelanjutan dari kalimat berikut yang benar!\n\n[QUESTION]\n[OPTIONS]\nJawaban: '
        
        few_shot_prompt = ''
        df_training = pd.read_csv('dataset_3shot/train/indocloze.csv')
        for idx, row in df_training.iterrows():
            premise_str = row['sentence-1'] + ' ' + row['sentence-2'] + ' ' + row['sentence-3'] + ' ' + row['sentence-4']
            option_str = f"A. {row['incorrect_ending']}\nB. {row['correct_ending']}"
            prompt_str = PROMPT.replace('[QUESTION]', premise_str).replace('[OPTIONS]', option_str)
            prompt_str += 'B'
            few_shot_prompt += prompt_str + '\n\n'

        df = pd.read_csv('dataset_3shot/indocloze.csv')
        for idx, row in df.iterrows():
            premise_str = row['sentence-1'] + ' ' + row['sentence-2'] + ' ' + row['sentence-3'] + ' ' + row['sentence-4']
            option_str = f"A. {row['correct_ending']}\nB. {row['incorrect_ending']}"
            option_num = 2
            prompt_str = PROMPT.replace('[QUESTION]', premise_str).replace('[OPTIONS]', option_str)
            inputs.append(few_shot_prompt + prompt_str)
            answers.append(0)
            number_options.append(option_num)
        return inputs, answers, number_options


    if dataset == 'maps':
        inputs = []; answers = []; number_options = []
        PROMPT = 'Perhatikan percakapan berikut!\n\n[QUESTION]\n[OPTIONS]\nJawaban: '
        
        few_shot_prompt = ''
        df_training = pd.read_csv('dataset_3shot/train/maps.csv')
        for idx, row in df_training.iterrows():
            premise_str = row['conversation'] + '\n\nApakah arti dari ' + row['proverb'] + '?\n' 
            option_str = f"A. {row['answer1']}\nB. {row['answer2']}\n"
            prompt_str = PROMPT.replace('[QUESTION]', premise_str).replace('[OPTIONS]', option_str)
            prompt_str += row['answer_key'].upper()
            few_shot_prompt += prompt_str + '\n\n'

        df = pd.read_csv('dataset_3shot/maps.csv')
        for idx, row in df.iterrows():
            premise_str = row['conversation'] + '\n\nApakah arti dari ' + row['proverb'] + '?\n' 
            option_str = f"A. {row['answer1']}\nB. {row['answer2']}\n"
            option_num = 2
            prompt_str = PROMPT.replace('[QUESTION]', premise_str).replace('[OPTIONS]', option_str)
            inputs.append(few_shot_prompt + prompt_str)
            answers.append({'a':0, 'b':1}[row['answer_key']])
            number_options.append(option_num)
        return inputs, answers, number_options
   

    if dataset == 'copal':
        inputs = []; answers = []; number_options = []
        
        few_shot_prompt = ''
        df_training = pd.read_csv('dataset_3shot/train/copal.csv')
        for idx, row in df_training.iterrows():
            premise_str = row['premise'] + '\n\n'
            if row['question'] == 'effect':
                premise_str += 'Apa akibat yang paling mungkin timbul dari kejadian di atas?\n\n'
            elif row['question'] == 'cause':
                premise_str += 'Apa penyebab yang mengakibatkan kejadian di atas?\n\n'
            else:
                print('Error')
            option_str = f"A. {row['choice1']}\nB. {row['choice2']}\n"
            few_shot_prompt += premise_str + option_str + '\nJawaban: ' + {0: 'A', 1: 'B'}[row['label']] + '\n\n'


        df = pd.read_csv('dataset_3shot/copal.csv')
        for idx, row in df.iterrows():
            premise_str = row['premise'] + '\n\n'
            if row['question'] == 'effect':
                premise_str += 'Apa akibat yang paling mungkin timbul dari kejadian di atas?\n\n'
            elif row['question'] == 'cause':
                premise_str += 'Apa penyebab yang mengakibatkan kejadian di atas?\n\n'
            else:
                print('Error')
            option_str = f"A. {row['choice1']}\nB. {row['choice2']}\n"
            option_num = 2
            inputs.append(few_shot_prompt + premise_str+option_str+'\nJawaban: ')
            answers.append(row['label'])
            number_options.append(option_num)
        return inputs, answers, number_options


    if dataset == 'indocareer':
        PROMPT = 'Ini adalah soal [SUBJECT][TYPE]. Pilihlah salah satu jawaban yang dianggap benar!\n\n[QUESTION]\n[OPTIONS]\nJawaban:'
        ids = []; inputs = []; answers = []; number_options = []
        
        few_shot_prompt = ''
        df_training = pd.read_csv('dataset_3shot/train/indocareer.csv')
        for idx, row in df_training.iterrows():
            option_str, option_num = get_option(row)
            prompt_str = PROMPT.replace('[SUBJECT]', subject_in_id[row['Subject']]).\
                                replace('[TYPE]', exam_type_in_id[row['Subject']]).\
                                replace('[QUESTION]', row['Question']).\
                                replace('[OPTIONS]', option_str) 
            prompt_str += row['Answer Key']
            few_shot_prompt += prompt_str + '\n\n'

        data = pd.read_csv('dataset_3shot/indocareer.csv')
        for idx, row in data.iterrows():
            option_str, option_num = get_option(row)
            prompt_str = PROMPT.replace('[SUBJECT]', subject_in_id[row['Subject']]).\
                                replace('[TYPE]', exam_type_in_id[row['Subject']]).\
                                replace('[QUESTION]', row['Question']).\
                                replace('[OPTIONS]', option_str)

            ids.append(row['ID'])
            inputs.append(few_shot_prompt + prompt_str)
            answers.append({'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}[row['Answer Key']])
            number_options.append(option_num)
        return inputs, answers, number_options
    

    if dataset == 'indoculture':
        PROMPT = 'Untuk konteks [LOKASI], sambungan yang tepat dari kalimat "[INPUT]" adalah\n[PILIHAN]\nJawaban: '
        ids = []; inputs = []; answers = []; number_options = []
 
        few_shot_prompt = ''
        df_training = pd.read_csv('dataset_3shot/train/indoculture.csv')

        for idx, row in df_training.iterrows():
            location = 'propinsi ' + row['province']
            options = ast.literal_eval(row['options'])
            options_str = '\n'.join(options)
            options = [x[3:] for x in options]

            prompt_str = PROMPT.replace('[LOKASI]', location).\
                                replace('[INPUT]', row['context']).\
                                replace('[PILIHAN]', options_str)
            prompt_str += row['answer']
            few_shot_prompt += prompt_str + '\n\n'

        data = pd.read_csv('dataset_3shot/indoculture.csv')
        for idx, row in data.iterrows():
            location = 'propinsi ' + row['province']
            options = ast.literal_eval(row['options'])
            options_str = '\n'.join(options)
            options = [x[3:] for x in options]

            prompt_str = PROMPT.replace('[LOKASI]', location).\
                                replace('[INPUT]', row['context']).\
                                replace('[PILIHAN]', options_str)

            ids.append(row['id'])
            inputs.append(few_shot_prompt + prompt_str)
            answers.append({'A': 0, 'B': 1, 'C': 2}[row['answer']])
            number_options.append(3)
        return inputs, answers, number_options
    

    if dataset == 'indommlu':
        PROMPT = 'Ini adalah soal [SUBJECT] untuk [LEVEL]. Pilihlah salah satu jawaban yang dianggap benar!\n\n[INPUT]\n[OPTION]\n\nJawaban: '
        inputs = []; answers = []; number_options = []
        key2id = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
        
        few_shot_prompt = ''
        df_training = pd.read_csv('dataset_3shot/train/indommlu.csv')
        for idx, row in df_training.iterrows():
            if row['level'] == 'Seleksi PTN':
                level = 'seleksi masuk universitas'
            else:
                try:
                    level = f"{math.trunc(float(row['kelas']))} {row['level']}"
                except:
                    level = f"{row['kelas']} {row['level']}"
            prompt_str = PROMPT.replace('[SUBJECT]', row['subject']).\
                           replace('[LEVEL]', level).\
                           replace('[INPUT]', row['soal']).\
                           replace('[OPTION]',row['jawaban'])
            few_shot_prompt += prompt_str + row['kunci'] + '\n\n'

        data = pd.read_csv('dataset_3shot/indommlu.csv')
        for idx, row in data.iterrows():
            if row['level'] == 'Seleksi PTN':
                level = 'seleksi masuk universitas'
            else:
                try:
                    level = f"{math.trunc(float(row['kelas']))} {row['level']}"
                except:
                    level = f"{row['kelas']} {row['level']}"

            inputs.append(
                few_shot_prompt + PROMPT.replace('[SUBJECT]', row['subject']).\
                       replace('[LEVEL]', level).\
                       replace('[INPUT]', row['soal']).\
                       replace('[OPTION]',row['jawaban'])
            )
            answers.append(key2id[row['kunci']])
            number_options.append(len(row['jawaban'].split('\n')))
        return inputs, answers, number_options


