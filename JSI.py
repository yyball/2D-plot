# -*- coding: UTF-8 -*-
#csvファイルのプロット・解析プログラム

import wx
import os
import csv 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib.ticker as ptick
from statistics import mean, median, variance,stdev
from scipy import interpolate

# import numpy.random.common #exe化時のエラー回避用
# import numpy.random.bounded_integers
# import numpy.random.entropy


f2 = open(r'C:\Users\yamagishi\Desktop\データ\和周波\f150\JSI\HR4000 noise\5.csv') 
reader2 = csv.reader(f2)
l2 =[row for row in reader2]
l_2 = [x[0] for x in l2]
li2 = [float(s) for s in l_2]

class FileDropTarget(wx.FileDropTarget):
    """ Drag & Drop Class """
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, files):
        global file
        file = files
        text_entry.SetLabel('{0:}'.format(len(file))+'個のファイル  最初のファイル名'+os.path.basename(file[0])) #ファイル絶対パスの取得
        
        return 0
        
class App(wx.Frame):
    """ GUI """
    def __init__(self, parent, id, title):
        def click_button_1(event):    #ボタン１がクリックされた時のイベント
            global c #複数ファイルプロット用カウンタ
            c = 0
            
            fig, ax=plt.subplots()
            text_entry.SetLabel('グラフを作成中です')
            if 'file' in globals():
                pass
            else:
                wx.MessageBox('ファイルを指定してください','error') #ファイルが指定されていないとき
                plt.close(fig)
                return 0
                
            li_z = []
                
            for fname in file:
                
                dirname = os.path.dirname(fname)   #ファイルの位置とファイル名に分解   
                basename = os.path.basename(fname)
                if dirname =='' or file[0] == 'None':
                    wx.MessageBox('ファイルを指定してください','error') #ファイルが指定されていないとき
                    plt.close(fig)
                    return 0
      
                os.chdir(dirname) #ファイルのある位置に移動
                ext = basename[-3:] #ファイル名の下から3文字の取得
                if not (ext == 'csv' or ext == 'DAT' or ext == 'txt'): #拡張子がcsvであるかの判定
                    wx.MessageBox('対応していない拡張子のファイルが含まれています','error') 
                    plt.close(fig)
                    return 0
                    
                else:
                    
                    f = open(basename) 
                    if ext == 'csv':
                        reader = csv.reader(f)
                        
                    elif ext == 'DAT': #datファイルはタブ区切り
                        reader = csv.reader(f,delimiter='\t')
                        
                    elif ext == 'txt': #txtファイルはタブ区切り?
                        reader = csv.reader(f,delimiter='\t')
                        
                    l =[row for row in reader]
                    
                    #ファイル形式がわかるまで保留
                    if len(l)==1 and l[0] ==[]: #ファイルの配列がない場合
                        plt.close(fig)
                        wx.MessageBox('空のファイルが含まれています','error') 
                        return 0
                    elif len(l[0])== 5 or len(l[0])== 2 or len(l[0]) == 3 or len(l[0])==1:    
                        title = text_1.GetValue()
                        x_label = text_2.GetValue()
                        y_label = text_3.GetValue()
                        z_label = text_4.GetValue()
                        if len(l[0])== 5:
                            l_x = [x[3] for x in l] #リスト列に変換
                            l_y = [y[4] for y in l] 
                            
                        elif len(l[0])== 2:
                            l_y = []
                            for y in l:  #DATファイルの２行目がないところを補てんしてからリスト列に変換
                                if len(y) == 1:
                                    y = y+['None']
                                l_y = l_y+[y[1]]
                                
                            l_x = [x[0] for x in l] #リスト列に変換
                            
                            
                            l_ch = [i for i, x in enumerate(l_x) if x == '!'] #スペアナ用リスト変換
                            if len(l_ch) == 3:
                                pt2 = l_ch[1]
                                pt3 = l_ch[2]
                                del l_x[pt3]
                                del l_y[pt3]
                                del l_x[:pt2+2]
                                del l_y[:pt2+2]
                                
                        
                        elif len(l[0]) == 3:
                            l_x = [x[0] for x in l] #リスト列に変換
                            l_y = [y[1] for y in l]
                            try:
                                if combobox_1.GetSelection() == 5 or combobox_1.GetSelection() == 6:
                                    l_yerr = [y[2] for y in l]
                            
                            except:
                                wx.MessageBox('３列目に標準偏差のデータが必要です','error')
                                plt.close(fig)
                                return 0 
                                
                        elif len(l[0])== 1:
                            l_y = []
                            l_x = []
                            for y in l:  #DATファイルの２行目がないところを補てんしてからリスト列に変換
                                if len(y) == 1:
                                    y = y+['None']
                                elif len(y) == 0:
                                    y = ['None','None']
                                l_y = l_y+[y[1]]
                            for x in l:  #DATファイルの２行目がないところを補てんしてからリスト列に変換
                                if len(x) == 0:
                                    x = ['None']
                                l_x = l_x+[x[0]]    
                            
                            
                            l_ch = [i for i, x in enumerate(l_x) if x == '>>>>>Begin Spectral Data<<<<<'] #スペアナ用リスト変換
                            if len(l_ch) == 1: 
                                pt1 = l_ch[0]
                                del l_x[:pt1+1]
                                del l_y[:pt1+1]    
                        try:
                            li_x = [float(s) for s in l_x] #文字列を数字列に変換
                            li_y = [float(s) for s in l_y]
                            if checkbox_2.GetValue():
                                for i in range(len(li_y)):
                                    li_y[i] = li_y[i] -li2[i] #ノイズ除去
                        
    
                            
                        except ValueError:
                            wx.MessageBox('csv,datデータに除去できない文字が含まれています','error')
                            plt.close(fig)
                            return 0
                       
                        
                            
                       
                        
                        

                        
                       
                        
                    
                    
                    else: #csvファイルが5列でない場合
                        wx.MessageBox('対応できないcsv,datファイルがあります（列数）','error')
                        plt.close(fig)
                        return 0
                li_z.append(li_y)
                
                c += 1
            
            if title !='':
                fig.canvas.set_window_title(title)
            
            plt.title(title) #plt.title(title,fontproperties = fp) で日本語対応
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            
            plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定
            plt.rcParams["mathtext.fontset"] = "stix" 
            plt.rcParams["font.size"] = 25
            plt.rcParams['axes.linewidth'] = 1.0# 軸の線幅edge linewidth。囲みの太さ
            #plt.rcParams['axes.grid'] = True
            plt.rcParams['xtick.direction'] = 'in'#x軸の目盛線
            plt.rcParams['ytick.direction'] = 'in'#y軸の目盛線
            plt.locator_params(axis='y',nbins=6)
            
            
            
            
            Z=np.array(li_z)
            if checkbox_3.GetValue():
                Z = Z[:,3411:3435]
            #x軸作成
            fir = spin1.GetValue()
            inc = spin2.GetValue()
            li_y = [fir+i*inc for i in range(len(Z[:,0])+1)]
            x = np.array(li_y) #x軸
            y = np.array(li_x) #y軸
            if checkbox_3.GetValue():
                y = y[3411:3435]
            X,Y=np.meshgrid(x,y)
            if checkbox_1.GetValue():
                Z =Z.transpose()
                X,Y=np.meshgrid(y,x)
            im = plt.pcolormesh(X,Y,Z.transpose(), cmap='jet')
            U, s, V = np.linalg.svd(Z, full_matrices =True)
            s2 = s**2
            norm = np.sum(s2)
            schmidt = np.sum((s2/norm)**2)
            text_entry.SetLabel('Schmidt number:'+str(1/schmidt))
            pp=plt.colorbar(im) # カラーバーの表示 
            pp.set_label(z_label) #カラーバーのラベル
            try:
                lim1 = float(text_5.GetValue())
                lim2 = float(text_6.GetValue())
                lim3 = float(text_7.GetValue())
                lim4 = float(text_8.GetValue())
            except:
                text_entry.SetLabel('範囲の値が適切ではありません')
                plt.close(fig)
                return 0
            if lim1 == 0 and lim2 == 0:
                pass
            else :
                try:
                    plt.xlim([lim1,lim2]) #表示範囲指定
                except:
                    text_entry.SetLabel('x軸の範囲が適切ではありません')
                    plt.close(fig)
                    return 0
                    
            if lim3 == 0 and lim4 == 0:
                pass
            else :
                try:
                    plt.ylim([lim3,lim4]) #表示範囲指定
                except:
                    text_entry.SetLabel('y軸の範囲が適切ではありません')
                    plt.close(fig)
                    return 0
            plt.subplots_adjust(bottom=0.2)
            plt.subplots_adjust(left=0.2)
            plt.tight_layout
            plt.show()        
                    
            
        def click_button_2(event):    #ボタン１がクリックされた時のイベント
            global c #複数ファイルプロット用カウンタ
            c = 0
            
            fig, ax=plt.subplots()
            
            if 'file' in globals():
                pass
            else:
                wx.MessageBox('ファイルを指定してください','error') #ファイルが指定されていないとき
                plt.close(fig)
                return 0
                
            li_z = []
                
            for fname in file:
                
                dirname = os.path.dirname(fname)   #ファイルの位置とファイル名に分解   
                basename = os.path.basename(fname)
                if dirname =='' or file[0] == 'None':
                    wx.MessageBox('ファイルを指定してください','error') #ファイルが指定されていないとき
                    plt.close(fig)
                    return 0
      
                os.chdir(dirname) #ファイルのある位置に移動
                ext = basename[-3:] #ファイル名の下から3文字の取得
                if not (ext == 'csv' or ext == 'DAT' or ext == 'txt'): #拡張子がcsvであるかの判定
                    wx.MessageBox('対応していない拡張子のファイルが含まれています','error') 
                    plt.close(fig)
                    return 0
                    
                else:
                    
                    f = open(basename) 
                    if ext == 'csv':
                        reader = csv.reader(f)
                        
                    elif ext == 'DAT': #datファイルはタブ区切り
                        reader = csv.reader(f,delimiter='\t')
                        
                    elif ext == 'txt': #txtファイルはタブ区切り?
                        reader = csv.reader(f,delimiter='\t')
                        
                    l =[row for row in reader]
                    
                    #ファイル形式がわかるまで保留
                    if len(l)==1 and l[0] ==[]: #ファイルの配列がない場合
                        plt.close(fig)
                        wx.MessageBox('空のファイルが含まれています','error') 
                        return 0
                    elif len(l[0])== 5 or len(l[0])== 2 or len(l[0]) == 3 or len(l[0])==1:    
                        title = text_1.GetValue()
                        x_label = text_2.GetValue()
                        y_label = text_3.GetValue()
                        z_label = text_4.GetValue()
                        if len(l[0])== 5:
                            l_x = [x[3] for x in l] #リスト列に変換
                            l_y = [y[4] for y in l] 
                            
                        elif len(l[0])== 2:
                            l_y = []
                            for y in l:  #DATファイルの２行目がないところを補てんしてからリスト列に変換
                                if len(y) == 1:
                                    y = y+['None']
                                l_y = l_y+[y[1]]
                                
                            l_x = [x[0] for x in l] #リスト列に変換
                            
                            
                            l_ch = [i for i, x in enumerate(l_x) if x == '!'] #スペアナ用リスト変換
                            if len(l_ch) == 3:
                                pt2 = l_ch[1]
                                pt3 = l_ch[2]
                                del l_x[pt3]
                                del l_y[pt3]
                                del l_x[:pt2+2]
                                del l_y[:pt2+2]
                                
                        
                        elif len(l[0]) == 3:
                            l_x = [x[0] for x in l] #リスト列に変換
                            l_y = [y[1] for y in l]
                            try:
                                if combobox_1.GetSelection() == 5 or combobox_1.GetSelection() == 6:
                                    l_yerr = [y[2] for y in l]
                            
                            except:
                                wx.MessageBox('３列目に標準偏差のデータが必要です','error')
                                plt.close(fig)
                                return 0 
                                
                        elif len(l[0])== 1:
                            l_y = []
                            l_x = []
                            for y in l:  #DATファイルの２行目がないところを補てんしてからリスト列に変換
                                if len(y) == 1:
                                    y = y+['None']
                                elif len(y) == 0:
                                    y = ['None','None']
                                l_y = l_y+[y[1]]
                            for x in l:  #DATファイルの２行目がないところを補てんしてからリスト列に変換
                                if len(x) == 0:
                                    x = ['None']
                                l_x = l_x+[x[0]]    
                            
                            
                            l_ch = [i for i, x in enumerate(l_x) if x == '>>>>>Begin Spectral Data<<<<<'] #スペアナ用リスト変換
                            if len(l_ch) == 1: 
                                pt1 = l_ch[0]
                                del l_x[:pt1+1]
                                del l_y[:pt1+1]    
                        try:
                            li_x = [float(s) for s in l_x] #文字列を数字列に変換
                            li_y = [float(s) for s in l_y]
    
                            
                        except ValueError:
                            wx.MessageBox('csv,datデータに除去できない文字が含まれています','error')
                            plt.close(fig)
                            return 0
                            
                        if checkbox_2.GetValue():
                            for i in range(len(li_y)):
                             if li_y[i] <= 0:
                                li_y[i] = 0
       
                    
                    
                    else: #csvファイルが5列でない場合
                        wx.MessageBox('対応できないcsv,datファイルがあります（列数）','error')
                       
                        return 0
                li_z.append(li_y)
                
                c += 1
            
            if title =='':
                title = '2dplot'

            Z=np.array(li_z)
            if checkbox_1.GetValue():
                Z =Z.transpose()

         
            np.savetxt(title+'.csv',Z,delimiter=',')
                    
                   
                    
                
            
        
        
        
        wx.Frame.__init__(self, parent, id, title, size=(600, 600), style=wx.DEFAULT_FRAME_STYLE)

        # パネル
        p = wx.Panel(self, wx.ID_ANY)

        label = wx.StaticText(p, wx.ID_ANY, 'ノイズを除去したデータを出力HR4000', style=wx.SIMPLE_BORDER | wx.TE_CENTER)
        label.SetBackgroundColour("#e0ffff")
        s_text_t = wx.StaticText(p,wx.ID_ANY,'タイトル') #固定文
        s_text_x = wx.StaticText(p,wx.ID_ANY,'x軸ラベル')
        s_text_y = wx.StaticText(p,wx.ID_ANY,'y軸ラベル')
        s_text_z = wx.StaticText(p,wx.ID_ANY,'z軸ラベル')
        s_text_f = wx.StaticText(p,wx.ID_ANY,'ファイル数軸の初値')
        s_text_inc = wx.StaticText(p,wx.ID_ANY,'ファイル数軸の間隔')
        text_x = wx.StaticText(p,wx.ID_ANY,'x軸範囲')
        text_y = wx.StaticText(p,wx.ID_ANY,'y軸範囲')
        text_to = wx.StaticText(p,wx.ID_ANY,'~')
        text_to2 = wx.StaticText(p,wx.ID_ANY,'~')
        # text_m = wx.StaticText(p,wx.ID_ANY,'マーカーサイズ')
        
        
        # ドロップ対象の設定
        self.SetDropTarget(FileDropTarget(self))
     

        # テキスト入力ウィジット
        global text_entry
        text_entry = wx.TextCtrl(p, wx.ID_ANY)
        text_1 = wx.TextCtrl(p, wx.ID_ANY) 
        text_2 = wx.TextCtrl(p, wx.ID_ANY)
        text_3 = wx.TextCtrl(p, wx.ID_ANY)
        text_4 = wx.TextCtrl(p, wx.ID_ANY)
        text_5 = wx.TextCtrl(p, wx.ID_ANY,'0')
        text_6 = wx.TextCtrl(p, wx.ID_ANY,'0')
        text_7 = wx.TextCtrl(p, wx.ID_ANY,'0')
        text_8 = wx.TextCtrl(p, wx.ID_ANY,'0')
        text_entry.Disable()
        
        #スピンロール
        spin1 = wx.SpinCtrlDouble(p, wx.ID_ANY, value="1550", inc = 0.1, min=1500, max=1630)
        spin2 = wx.SpinCtrlDouble(p, wx.ID_ANY, value="1", inc = 0.1, min=0.001, max=10)
        
        #チェックボックス
        checkbox_1 = wx.CheckBox(p, wx.ID_ANY, 'x軸とy軸を入れ替える')
        checkbox_2 = wx.CheckBox(p, wx.ID_ANY,'ノイズ除去')
        checkbox_3 = wx.CheckBox(p, wx.ID_ANY,'切り取り')
        # checkbox_4 = wx.CheckBox(p, wx.ID_ANY,'x軸を指数表記')
        # checkbox_5 = wx.CheckBox(p, wx.ID_ANY,'y軸を指数表記')
        # checkbox_6 = wx.CheckBox(p, wx.ID_ANY,'FWHM')
        
        checkbox_1.SetValue(True)
        # checkbox_5.SetValue(True)
        
        
        #コンボボックス
        # element_array = ('線と点','線','点（プロットのみ対応）','近似直線（プロットのみ対応）','スプライン補間（プロットのみ対応）','近似直線（エラーバー付き）','点（エラーバー付き）')
        # combobox_1 = wx.ComboBox(p, wx.ID_ANY , 'プロット表記の選択', choices = element_array, style = wx.CB_READONLY)
        
        # element_array2 = ('T','G','M','k','1','c','m','u','n','p','f')
        # combobox_2 = wx.ComboBox(p, wx.ID_ANY , 'プロット表記の選択', choices = element_array2, style = wx.CB_READONLY)
       
        # combobox_3 = wx.ComboBox(p, wx.ID_ANY , 'プロット表記の選択', choices = element_array2, style = wx.CB_READONLY)
        
        # combobox_1.SetSelection(0)
        # combobox_2.SetSelection(4)
        # combobox_3.SetSelection(4)

       
        
        #ボタン
        button_1 = wx.Button(p,wx.ID_ANY,'2Dプロット')
        button_2 = wx.Button(p,wx.ID_ANY,'csv保存')
        # button_3 = wx.Button(p,wx.ID_ANY,'ｙ軸成分のデータ')
        # button_4 = wx.Button(p,wx.ID_ANY,'ｙ軸成分のデータ(dBm用)')
        
        button_1.Bind(wx.EVT_BUTTON,click_button_1)
        button_2.Bind(wx.EVT_BUTTON,click_button_2)
        # button_3.Bind(wx.EVT_BUTTON,click_button_3)
        # button_4.Bind(wx.EVT_BUTTON,click_button_4)
        
        #スライダー
        
        # slider = wx.Slider(p, style=wx.SL_AUTOTICKS|wx.SL_LABELS)
        # slider.SetTickFreq(1)
        # slider.SetMin(0)
        # slider.SetMax(10)
        # slider.SetValue(5)

        # レイアウト
        layout = wx.BoxSizer(wx.VERTICAL)
        sizer1= wx.BoxSizer(wx.HORIZONTAL)
        # sizer2= wx.BoxSizer(wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        # sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_txy = wx.FlexGridSizer(4,2,(0,0))
        sizer_limxy = wx.FlexGridSizer(2,4,(0,0))
        layout.Add(label, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)
        layout.Add(sizer1, flag =wx.GROW, border=10)
        # layout.Add(sizer2, flag =wx.GROW, border=10)
        layout.Add(sizer_txy,flag=wx.EXPAND | wx.ALL, border=10)
        layout.Add(sizer3, flag =wx.GROW, border=10)
        layout.Add(sizer_limxy, flag =wx.GROW, border=10)
        layout.Add(text_entry, flag=wx.EXPAND | wx.ALL, border=10)
        # layout.Add(sizer4)
        layout.Add(sizer)
        
        # sizer1.Add(combobox_1, flag =wx.GROW| wx.LEFT, border=10)
        sizer1.Add(checkbox_1, flag =wx.GROW| wx.LEFT, border=10)
        sizer1.Add(checkbox_2, flag =wx.GROW| wx.LEFT, border=10)
        sizer1.Add(checkbox_3, flag = wx.EXPAND| wx.LEFT, border = 10)
        
        # sizer2.Add(checkbox_3, flag =wx.GROW| wx.LEFT|wx.TOP, border=10)
        # sizer2.Add(checkbox_4, flag =wx.GROW| wx.LEFT|wx.TOP, border=10)
        # sizer2.Add(checkbox_5, flag =wx.GROW| wx.LEFT|wx.TOP, border=10)
        
        sizer_txy.Add(s_text_t, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_txy.Add(text_1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_txy.Add(s_text_x, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_txy.Add(text_2, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_txy.Add(s_text_y, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_txy.Add(text_3, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_txy.Add(s_text_z, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_txy.Add(text_4, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_txy.AddGrowableCol(1) #グリッドサイズ変更
        
        sizer3.Add(s_text_f, flag =wx.GROW| wx.LEFT, border=10)
        sizer3.Add(spin1, flag =wx.GROW| wx.LEFT, border=10)
        sizer3.Add(s_text_inc, flag =wx.GROW| wx.LEFT, border=10)
        sizer3.Add(spin2, flag =wx.GROW| wx.LEFT, border=10)
        
        # sizer4.Add(text_m,1, flag = wx.ALL, border=10)
        # sizer4.Add(slider ,4)
        
        sizer_limxy.Add(text_x, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_limxy.Add(text_5, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_limxy.Add(text_to, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_limxy.Add(text_6, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_limxy.Add(text_y, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_limxy.Add(text_7, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_limxy.Add(text_to2, flag=wx.EXPAND | wx.ALL, border=10)
        sizer_limxy.Add(text_8, flag=wx.EXPAND | wx.ALL, border=10)
        
        sizer.Add(button_1, flag =wx.GROW| wx.LEFT|wx.BOTTOM, border=10)
        sizer.Add(button_2, flag =wx.GROW| wx.LEFT|wx.BOTTOM, border=10)
        # sizer.Add(button_3, flag =wx.GROW| wx.LEFT|wx.BOTTOM, border=10)
        # sizer.Add(button_4, flag =wx.GROW| wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        p.SetSizer(layout)
        
        self.Centre()

        self.Show()
        
    def frame_close(self, event):
        """ 閉じたときに発生するイベント """
        
        plt.close('all')
        #event.Skip()
        self.Destroy()
    
        

app = wx.App()
App(None, -1, '2Dプロット')
app.MainLoop()


