import threading
import tkinter as tk
import tkinter.ttk as ttk
import csv
import time
import os
from gtts import gTTS
from playsound import playsound

# global value
g_rows = []
g_profile = {'USER': 'Sophine', 'RETRY_COUNTER': '2', 'VOICE_CK': 1, 'EXAMPLE_CK': 1, 'EXAM_TIMES': 0, 'EXAM_WORDS': 0, 'KNOW_WORDS': 0, 'LAST_IDX': 0, 'EXAM_BEGIN':0}
g_examIdx = 0

# Read/Write User Profile
def SystemProfile(flag):
    csv_file = "profile.csv"
    if flag == 'Read':
        if os.path.isfile(csv_file) == True:
            with open(csv_file, 'r', encoding='utf-8-sig', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    g_profile['USER'] = row['USER']
                    g_profile['RETRY_COUNTER'] = row['RETRY_COUNTER']
                    g_profile['VOICE_CK']  = int(row['VOICE_CK']), 
                    g_profile['EXAMPLE_CK'] = int(row['EXAMPLE_CK'])
                    g_profile['EXAM_TIMES'] = 0
                    g_profile['EXAM_WORDS'] = 0
                    g_profile['KNOW_WORDS'] = 0
                    g_profile['LAST_IDX']  = 0
                    g_profile['EXAM_BEGIN'] = 0     # 從頭開始
    else:        
        cvs_colums = ['USER', 'RETRY_COUNTER', 'VOICE_CK', 'EXAMPLE_CK', 'EXAM_TIMES', 
        'EXAM_WORDS', 'KNOW_WORDS', 'LAST_IDX', 'EXAM_BEGIN']
        try:
        
            with open(csv_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cvs_colums)
                writer.writeheader()
                writer.writerow(g_profile)
        except IOError:
            print("I/O error")

# User Profile 讀取只會更新測驗的資訊
def UserProfile(user_name, flag):
    csv_file = user_name+"_profile.csv"
    if flag == 'Read':
        if os.path.isfile(csv_file) == True:
            with open(csv_file, 'r', encoding='utf-8-sig', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    g_profile['EXAM_TIMES'] = int(row['EXAM_TIMES']) + 1 # 測驗次數
                    g_profile['EXAM_WORDS'] = int(row['EXAM_WORDS']) # 測驗文字
                    g_profile['KNOW_WORDS'] = int(row['KNOW_WORDS']) # 完成正確文字
                    g_profile['LAST_IDX']  = int(row['LAST_IDX']) # 最後測驗的 idx 
                    g_profile['EXAM_BEGIN'] = int(row['EXAM_BEGIN']) # 0 為從頭開始
    elif flag == 'Write':
        cvs_colums = ['USER', 'RETRY_COUNTER', 'VOICE_CK', 'EXAMPLE_CK', 
                      'EXAM_TIMES', 'EXAM_WORDS', 'KNOW_WORDS', 'LAST_IDX', 'EXAM_BEGIN']
        try:
        
            with open(csv_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cvs_colums)
                writer.writeheader()
                writer.writerow(g_profile)
        except IOError:
            print("I/O error")

# 讀取 Vocabulary, 並且複制一份給使用者
def LoadVocabulary(user_name):
    user_cvs_file = user_name+'_7000_Vocabulary.csv'
    if os.path.isfile(user_cvs_file) == True:
        # 假設檔案已存在則讀取檔案, 並確認是否有更新
        org_rows = []
        with open('7000_Vocabulary.csv', 'r', encoding='utf-8-sig', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dict1 = {'VOCABULARY':row['VOCABULARY'], 'TYPE':row['TYPE'], 'CHINESE':row['CHINESE'], 
                'ENGLISH_EXAMPLE':row['ENGLISH_EXAMPLE'], 'CHINESE_EXAMPLE':row['CHINESE_EXAMPLE'],
                'EXAM_TIMES': 0, 'CURRECT_TIMES':0, 'WRONG_TIMES': 0}
                org_rows.append(dict1)
        # 取使用者
        idx = 0
        with open(user_cvs_file, 'r', encoding='utf-8-sig', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dict1 = {'VOCABULARY':row['VOCABULARY'], 'TYPE':row['TYPE'], 'CHINESE':row['CHINESE'], 
                'ENGLISH_EXAMPLE':row['ENGLISH_EXAMPLE'], 'CHINESE_EXAMPLE':row['CHINESE_EXAMPLE'],
                'EXAM_TIMES': int(row['EXAM_TIMES']), 'CURRECT_TIMES': int(row['CURRECT_TIMES']), 'WRONG_TIMES': int(row['WRONG_TIMES'])}
                
                # 假設不同, 就全部取代
                if idx < len(org_rows):
                    row = org_rows[idx]
                    if dict1['VOCABULARY'] != row['VOCABULARY']:
                        dict1 = row
                    g_rows.append(dict1)
                    idx += 1

        # 原始檔比較大, 則新增到後面
        if idx < len(org_rows):
            for idx in len(org_rows):
                row = org_rows[idx]
                g_rows.append(row)
    else:
        # 沒有則讀取並備份一份
        with open('7000_Vocabulary.csv', 'r', encoding='utf-8-sig', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dict1 = {'VOCABULARY':row['VOCABULARY'], 'TYPE':row['TYPE'], 'CHINESE':row['CHINESE'], 
                'ENGLISH_EXAMPLE':row['ENGLISH_EXAMPLE'], 'CHINESE_EXAMPLE':row['CHINESE_EXAMPLE'],
                'EXAM_TIMES': 0, 'CURRECT_TIMES':0, 'WRONG_TIMES': 0}
                g_rows.append(dict1)

# 更新 Vocabulary 
def UpdateVocabulary(user_name):
    user_cvs_file = user_name+'_7000_Vocabulary.csv'
    cvs_colums = ['VOCABULARY', 'TYPE', 'CHINESE', 'ENGLISH_EXAMPLE', 'CHINESE_EXAMPLE',
                'EXAM_TIMES', 'CURRECT_TIMES', 'WRONG_TIMES'] 
    with open(user_cvs_file, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cvs_colums)
        writer.writeheader()        
        writer.writerows(g_rows)



class Speech(threading.Thread):
  def __init__(self, voc):
    threading.Thread.__init__(self)
    self.voc = voc

  def run(self):
    filename = 'voic/' + self.voc + '.mp3'
    language = 'en'
    
    if os.path.isfile(filename) == False:
        myobj = gTTS(text=self.voc, lang=language, slow=False)
        # Saving the converted audio in a mp3 file named
        myobj.save(filename)
  
    # Playing the converted file
    playsound(filename)

def OnQuit(event):
    exit()

def OnEndOfExam(user_name):
    UserProfile(user_name, 'Write')
    UpdateVocabulary(user_name)
    window_pop_up = tk.Toplevel(root)
    window_pop_up.geometry('200x150') 
    window_pop_up.title('結束測驗')
    window_pop_up.attributes('-topmost', True)
    tk.Label(window_pop_up, text=g_profile['USER'], font=('Arial', 14)).place(x=20, y=20) 
    tk.Label(window_pop_up, text='正確率 : ' + str(g_profile['KNOW_WORDS']) + ' / ' + str(g_profile['EXAM_WORDS']), font=('Arial', 14)).place(x=20, y=50) 
    btn_quit = tk.Button(window_pop_up, text='結束',  font=('Arial', 14))
    btn_quit.bind('<Button-1>', OnQuit)
    btn_quit.place(x=60, y=80)
    
# main 
class winMain(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.num_answer = 0
        self.num_correct = 0
        self.examIdx = 0
        self.rows = g_rows
        
        self.nErrorCnt = 0
        self.root = root
        if g_profile['EXAM_BEGIN'] == 1:
            self.examIdx = g_profile['LAST_IDX']
        self.row = self.rows[self.examIdx]
        
        # 使用者資料
        tk.Label(root, text=var_usr_name.get() + '  (第 '+ str(g_profile['EXAM_TIMES']) +' 次考試)', font=('Arial', 14)).place(x=20, y=5)
        tk.Label(root, text='第 ' + str(self.examIdx+1) + '單字', font=('Arial', 14)).place(x=20, y=35)
        # 考題
        self.row['EXAM_TIMES'] += 1 # 測試次數 
        self.exam = tk.StringVar()
        if self.row['WRONG_TIMES'] == 0:
            self.exam.set('中文: '+ self.row['CHINESE'] + ' (詞性: ' + self.row['TYPE'] + ' )')
        else:
            self.exam.set('中文: '+ self.row['CHINESE'] + ' (詞性: ' + self.row['TYPE'] + ' )  - 錯誤率 ' + str(self.row['WRONG_TIMES'] ) + ' / '+ str(self.row['EXAM_TIMES'] ))

        tk.Label(root, textvariable=self.exam, font=('Arial', 14)).place(x=20, y=60)
        
        # 回答
        self.var_anser = tk.StringVar()
        entry_vocabulary = tk.Entry(root, textvariable=self.var_anser, font=('Arial', 14)) 
        entry_vocabulary.place(x=20,y=95)
        entry_vocabulary.bind('<Return>', self.OnCheck)
        entry_vocabulary.focus_set()
        btn_comfirm = tk.Button(root, text='確認',  font=('Arial', 14))
        btn_comfirm.bind('<Button-1>', self.OnCheck)
        btn_comfirm.place(x=260, y=85)
        self.myThread = Speech(self.row['VOCABULARY'])
        self.myThread.start()
        self.myThread.join()

        btn_exit = tk.Button(root, text='Exit',  font=('Arial', 14))
        btn_exit.bind('<Button-1>', self.OnExit)
        btn_exit.place(x=340, y=250)

    # 離開存 unknow file
    def OnExit(self, root):
        # 依考試的次數再次存檔
        #UserProfile(g_profile['USER'], 'Write')
        #UpdateVocabulary(g_profile['USER'])
        g_profile['EXAM_WORDS'] = self.num_answer
        g_profile['KNOW_WORDS'] = self.num_correct
        g_profile['LAST_IDX'] = self.examIdx
        OnEndOfExam(g_profile['USER'])

    # Check
    def OnCheck(self, root):
        self.num_answer += 1
        print(self.var_anser.get(), "??", self.row['VOCABULARY'])
        if self.var_anser.get() == self.row['VOCABULARY']:
            # 假設之前有錯誤, 則存入 array 裡
            if self.nErrorCnt > 0:
                self.row['WRONG_TIMES'] = self.nErrorCnt
            else:
                self.row['CURRECT_TIMES'] += 1
    
            # 若相等, 下一題
            self.nErrorCnt = 0
            self.num_correct += 1
            g_profile['LAST_IDX'] = self.examIdx
            tk.Label(self.root, text='答對: '+ self.row['CHINESE'] + ' ('+ self.row['VOCABULARY']  + ')      ', 
            foreground="blue", font=('Arial', 14)).place(x=20, y=125)
            
            # 顯示範例
            tk.Label(self.root, text='範例 :' + self.row['CHINESE_EXAMPLE'], font=('Arial', 14), wraplength=350).place(x=20, y=165)
            tk.Label(self.root, text=self.row['ENGLISH_EXAMPLE'], font=('Arial', 14), wraplength=350).place(x=20, y=200)

             # 範例speech
            if g_profile['EXAMPLE_CK'] == 1 and len(self.row['CHINESE_EXAMPLE']) > 0:
                self.myThread = Speech(self.row['ENGLISH_EXAMPLE'])
                self.myThread.start()
                self.myThread.join()

            self.examIdx += 1
            if (self.examIdx >= len(g_rows)):
                g_profile['EXAM_WORDS'] = self.num_answer
                g_profile['KNOW_WORDS'] = self.num_correct
                g_profile['LAST_IDX'] = self.examIdx;
                OnEndOfExam(g_profile['USER'])
                
            self.var_anser.set('')      # 清除答案
            self.row = g_rows[self.examIdx]            
            self.row['EXAM_TIMES'] += 1
            self.exam.set('中文: '+ self.row['CHINESE'] + ' (詞性: ' + self.row['TYPE'] + ' )   ')
            if g_profile['VOICE_CK'] == True:
                self.myThread = Speech(self.row['VOCABULARY'])
                self.myThread.start()
                self.myThread.join()
            print('OK')
        else: 
            if self.nErrorCnt < int(g_profile['RETRY_COUNTER']):
                self.row['EXAM_TIMES'] += 1
                
                listStr = []
                vocabulary = self.row['VOCABULARY'];
                nVocSize = len(self.row['VOCABULARY'])
                idx = 0  
                for c in self.var_anser.get():
                    if idx < nVocSize and c != vocabulary[idx]:
                        listStr.append('_')
                    else:
                        listStr.append(c)
                    idx += 1
                answer = ''.join(listStr)
                print(answer)
                
                # 第一次錯
                self.nErrorCnt += 1
                tk.Label(self.root, text='錯了： '+ answer + '           ', foreground="red", 
                font=('Arial', 14)).place(x=20, y=125)
                self.var_anser.set('')      # 清除答案
            else:
                tk.Label(self.root, text='正確答案為: ' + self.row['VOCABULARY'] + '           ', foreground="blue", 
                 font=('Arial', 14)).place(x=20, y=125)

if __name__ == "__main__":
    root = tk.Tk()
    root.title('英文單字測試')
    root.geometry('400x300')
    # #main thread
    def OnSign(event):
        window_sign_up.destroy()
        # 找出記錄
        g_profile['USER'] = var_usr_name.get()
        g_profile['RETRY_COUNTER'] = selected_count.get()
        g_profile['VOICE_CK'] = int(ck_voice.get())
        g_profile['EXAMPLE_CK'] = int(ck_eaxmple.get())
        
        
        print('select count = ', selected_count.get())
        SystemProfile('Write')
        
        # 取得目前使用者的資訊
        UserProfile(var_usr_name.get(), 'Read')
        print('start count = ', selected_start.get())
        if selected_start.get() == '從頭':
            g_profile['EXAM_BEGIN'] = 0
        else:
            g_profile['EXAM_BEGIN'] = 1 # 

        UserProfile(var_usr_name.get(), 'Write')
        LoadVocabulary(var_usr_name.get())
        UpdateVocabulary(var_usr_name.get())
        winMain(root).pack(side="top", fill="both", expand=True)
        return
    
    SystemProfile('Read')
    window_sign_up = tk.Toplevel(root)
    window_sign_up.geometry('300x250') 
    window_sign_up.title('輸入姓名')

    name_label = tk.Label(window_sign_up, text='姓名:  ', font=('Arial', 12)).place(x=20, y=20)
    var_usr_name = tk.StringVar()
    var_usr_name.set('Sophine')
    entry_usr_name = tk.Entry(window_sign_up, textvariable=var_usr_name, font=('Arial', 12)) 
    entry_usr_name.place(x=100,y=20)
    entry_usr_name.bind('<Return>', OnSign)
    entry_usr_name.focus_set()

    # 選擇測驗次數
    count_list = {'1', '2', '3'}
    selected_count = tk.StringVar()
    tk.Label(window_sign_up, text='測驗次數: ', font=('Arial', 12)).place(x=20, y=50)
    count_cb = ttk.Combobox(window_sign_up, textvariable = selected_count)
    count_cb['values'] = ['1', '2', '3']
    count_cb['state'] = 'readonly'
    count_cb.current(1)
    count_cb.place(x=100, y=50) 

    # 選擇考試的起點/上次
    start_list = {'從頭', '接上次'}
    selected_start = tk.StringVar()
    tk.Label(window_sign_up, text='測試起點: ', font=('Arial', 12)).place(x=20, y=80)
    start_cb = ttk.Combobox(window_sign_up, textvariable = selected_start)
    start_cb['values'] = ['從頭', '接上次']
    start_cb['state'] = 'readonly'
    start_cb.current(0)
    start_cb.place(x=100, y=80) 
    
    ck_voice = tk.BooleanVar()  
    ck_voice.set(True)
    if g_profile['VOICE_CK'] == 0:
        ck_voice.set(False)
    speech_ckb = tk.Checkbutton(window_sign_up, text = "單字發音", 
                      variable = ck_voice,
                      onvalue = 1,
                      offvalue = 0,
                      height = 2,
                      width = 10, font=('Arial', 12))
    speech_ckb.place(x=10, y=105)

    ck_eaxmple = tk.BooleanVar()
    ck_eaxmple.set(True)
    if g_profile['EXAMPLE_CK'] == 0:
        ck_eaxmple.set(False)
    example_ckb = tk.Checkbutton(window_sign_up, text = "例句說明", 
                      variable = ck_eaxmple,
                      onvalue = 1,
                      offvalue = 0,
                      height = 2,
                      width = 10, font=('Arial', 12))
    example_ckb.place(x=10, y=135)
    btn_comfirm_sign_up = tk.Button(window_sign_up, text='確認',  font=('Arial', 12))
    btn_comfirm_sign_up.bind('<Button-1>',OnSign)
    btn_comfirm_sign_up.place(x=120, y=180)

    window_sign_up.attributes('-topmost', True)
    
    
    root.mainloop()


#print(g_rows)