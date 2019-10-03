# -*- coding: utf-8 -*-
#! Python3

# @author
# - Renan Silva

import PIL
from PIL import Image,ImageTk

import cv2
import time

import numpy    as np
from fuzzywuzzy import fuzz, process

import tkinter     as tk
import tkinter.ttk as ttk
from tkinter       import filedialog, messagebox
from tkinter       import font as tkfont

from Dict            import Dictionary
from Exceptions      import Verify
from Treinamento import Treinamento
from CapturaFace     import ReferenceFile
from Configuration   import Path

class ReconhecimentoFacial(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Ministério do Meio Ambiente') #title of the window
        tk.Tk.wm_geometry(self, '700x700') #size of the window
        self.cabecalho_font = tkfont.Font(family='Calibri', size=10)
        self.title_font = tkfont.Font(family='Calibri', size=14, weight="bold")
        self.text_font = tkfont.Font(family='Calibri', size=16)
        self.small_font = tkfont.Font(family='Calibri', size=11)
        self.acess_name_font = tkfont.Font(family='Calibri', size=21)
        self.acess_nivel_font = tkfont.Font(family='Calibri', size=20)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Home, Entrar, Cadastrar):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.grid()

class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="Bem vindo ao Sistema de Identificação Biométrico do\nMinistério do Meio Ambiente", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        labelText = tk.Label(self)
        labelText.pack()
        texto = tk.StringVar()
        texto.set('''Esse sistema controla o acesso a uma rede com banco dados do Ministério do Meio Ambiente que contém informações estratégicas sobre
                     as propriedades rurais que utilizam agrotóxicos proibidos por causarem grandes impactos nos lenções freáticos, rios e mares.''')
        label = tk.Label(labelText, textvariable=texto, font=controller.text_font, relief="groove", wraplengt=700, height=10)
        label.pack(side="top", pady=100)

        labelButtons = tk.Label(self)
        labelButtons.pack()

        button1 = ttk.Button(labelButtons, text="Já sou cadastrado", command=lambda: controller.show_frame("Entrar"))
        button2 = ttk.Button(labelButtons, text="Cadastrar", command=lambda: controller.show_frame("Cadastrar"))
        button1.pack(side="left", padx=5)
        button2.pack(side="left", padx=10)

        labelBottom = tk.Label(self)
        labelBottom.pack(side='bottom')

        labelBottom = tk.Label(labelBottom, text="Ministério do Meio Ambiente", font=controller.cabecalho_font)
        labelBottom.pack(side="bottom", fill="x", pady=10)

class Entrar(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Ministério do Meio Ambiente", font=controller.title_font)
        label.pack(side="top", fill="x", pady=2)

        self.labelText = tk.Label(self)
        self.labelText.pack()
        self.textoEntrar = tk.StringVar()

        self.frameFotoEntrar = tk.Frame(self)
        self.frameFotoEntrar.pack(fill='x', anchor='center')

        self.tirarFotoLabelEntrar = tk.Label(self.frameFotoEntrar)
        self.tirarFotoLabelEntrar.pack()
        
        if Verify().verifyFiles() == True:

            self.textoEntrar.set('''Detalhes sobre o acesso:\n
            1 - Informação de nível 1, todos podem ter acesso.{}
            2 - Informação de nível 2, restritas aos diretores de divisões.{}
            3 - Informação de nível 3, somente Ministro do Meio Ambiente.{}'''.format(' '*40, ' '*24, ' '*18))
            label = tk.Label(self.labelText, textvariable=self.textoEntrar, font=controller.text_font, relief="groove", wraplengt=700, height=10)
            label.pack(side="top", pady=100)

            self.entrarBtn = ttk.Button(self, text="Entrar", command=self.checkFace)
            self.entrarBtn.pack()

        else:

            self.textoEntrar.set('''Parece que algo está errado, garanta que os pontos abaixo estão contemplados.\n
            1 - Fotos tiradas com sucesso, seu dataset foi gerado corretamente no diretório:{}
            ../fotos/\n
            2 - Seu nome e seu nível de acesso devem estar preenchidos no arquivo:{}
            ../config/id_with_reference.csv\n
            3 - Seu modelo reconhecedor deve estar criado no diretório:{}
            ../models/classificadorLBPH.yml\n
            Se o erro persistir, por gentileza contate o administrador do sistema.\n'''.format(' '*9, ' '*24, ' '*47))
            label = tk.Label(self.labelText, textvariable=self.textoEntrar, font=controller.small_font, relief="groove", wraplengt=700, height=15)
            label.pack(side="top", pady=100)

        button = ttk.Button(self, text="Ir para home",command=reinicia_gui)
        button.pack()

        self.labelContent = tk.Label(self, text="-")
        self.labelContent.pack()

        self.textoName = tk.StringVar()
        self.textoName.set('')
        self.labelName = tk.Label(self, textvariable=self.textoName, font=controller.acess_name_font)
        self.labelName.pack()

        self.textoNivel = tk.StringVar()
        self.textoNivel.set('')
        self.labelNivel = tk.Label(self, textvariable=self.textoNivel, font=controller.acess_nivel_font)
        self.labelNivel.pack()

        self.scrollBarTexto = tk.Scrollbar(self)
        self.scrollBarTexto.pack(side="right", fill='y')
        self.textoInScrollBar = tk.Text(self, wrap= None, yscrollcommand=self.scrollBarTexto.set)
        
        labelBottom = tk.Label(self)
        labelBottom.pack(side='bottom')
        

    def restart(self):
        self.refresh()
        self.controller.show_frame("Home")

    #USADO PARA LIMPAR E RODAR DE NOVO
    def refresh(self):
        self.textoName.set('')
        self.textoNivel.set('')

        self.textoInScrollBar.pack_forget()
        self.textoInScrollBar = tk.Text(self, wrap= None, yscrollcommand=self.scrollBarTexto.set)

    def checkFace(self):

        #USADO PARA LIMPAR O TEXTO DE DESCRICAO
        self.labelText.destroy()

        detectorFace = cv2.CascadeClassifier("{}/haarcascade-frontalface-default.xml".format(Path().reconhecedores))
        reconhecedor = cv2.face.LBPHFaceRecognizer_create()
        reconhecedor.read("{}/classificadorLBPH.yml".format(Path().models))
        largura, altura = 220, 220
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    
        self.cameraEntrar = cv2.VideoCapture(0)

        nomeDict = Dictionary().dictionary_id
        lvlDict = Dictionary().dictionary_lvl

        checkEntry = []
        
        ids = []
        confiancas = []
        
        temp = 0

        while (True):

            conectado, imagem = self.cameraEntrar.read()
            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            facesDetectadas = detectorFace.detectMultiScale(imagemCinza,
                                                            scaleFactor=1.5,
                                                            minSize=(30,30))

            for (x, y, l ,a) in facesDetectadas:

                imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))

                cv2.rectangle(imagem, (x,y), (x + l, y + a), (0,0,255), 2)
                id, confianca = reconhecedor.predict(imagemFace)
                nome = nomeDict[str(id)]
                lvl  = lvlDict[str(id)]
  
                ids.append(id)
                confiancas.append(confianca)

                cv2.putText(imagem, str(id), (x,y +(a+30)), font, 2, (0,0,255))
                cv2.putText(imagem, str(confianca), (x,y + (a+50)), font, 1, (0,0,255))
                temp += 1

            cv2.imshow("Face", imagem)
            cv2.waitKey(1)
            if temp > 100:
                break

        self.validaFace(ids, confiancas)

        self.cameraEntrar.release()
        cv2.destroyAllWindows()

    def validaFace(self, ids, confiancas):

        nomeDict = Dictionary().dictionary_id
        lvlDict = Dictionary().dictionary_lvl

        idsAmount = 0
        idsAmount = len(set(ids))

        id = ''
        id = ids[0]

        minimo = 0
        maximo = 0
        minimo = min(confiancas)
        maximo = max(confiancas)

        print('Ids amount = {}'.format(idsAmount))
        print('Min confianca = {}'.format(minimo))
        print('Max confianca = {}'.format(maximo))

        if idsAmount > 1 and (maximo >= 55 and minimo >= 55):
            messagebox.showerror("Acesso negado", "Você não tem acesso!")
        else:
            self.mostraConteudo(id)


    def mostraConteudo(self, id):

        self.entrarBtn.destroy()
        informations = Dictionary()
        nomeDict = informations.dictionary_id
        lvlDict = informations.dictionary_lvl

        nome = ''
        lvl  = ''

        nome = nomeDict[str(id)]
        lvl  = lvlDict[str(id)]

        self.textoName.set('Bem vindo {}!'.format(nome))
        self.textoNivel.set('Você tem acesso à informação de nível {}'.format(lvl))

        self.textoInScrollBar.pack(side="left")

        if '1' in lvl:
            texto = informations.getText('1')
            self.textoInScrollBar.insert("1.0", "{}".format(texto))
        elif '2' in lvl:
            texto = informations.getText('2')
            self.textoInScrollBar.insert("1.0", "{}".format(texto))
        elif '3' in lvl:
            texto = informations.getText('3')
            self.textoInScrollBar.insert("1.0", "{}".format(texto))
        else:
            messagebox.showerror("Error", "Algo errado ocorreu identificando seu nível de acesso!")

        self.scrollBarTexto.config(command=self.textoInScrollBar.yview)

class Cadastrar(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller

        #---------------------------
        frameTitle = tk.Frame(self)
        frameTitle.pack(fill='both')

        labelTitle = tk.Label(frameTitle, text="Página de Cadastro", font=controller.title_font)
        labelTitle.pack(side="top", fill="x", pady=10)

        #---------------------------
        #nome
        frameName = tk.Frame(self)
        frameName.pack(fill='x')


        nomeLabel = tk.Label(frameName, text="Digite seu nome:", bd=10, width=12, anchor="w")
        nomeLabel.pack(side='left', padx=5, pady=5)

        self.nomeEntry = tk.Entry(frameName)
        self.nomeEntry.pack(fill='x', padx=5, expand=True)

        #---------------------------
        #niveis
        frameNiveis = tk.Frame(self)
        frameNiveis.pack(fill='x')

        niveisLabel = tk.Label(frameNiveis, text="Selecione seu nível de acesso:", bd=10, width=23, anchor="w")
        niveisLabel.pack(side='left', padx=5, pady=5)

        #to do ------------------
        self.lvl = tk.IntVar()
        self.lvlUm = tk.Radiobutton(frameNiveis, text="Nivel 1", variable=self.lvl, value=1)
        self.lvlUm.pack(side="left")

        self.lvlDois = tk.Radiobutton(frameNiveis, text="Nivel 2", variable=self.lvl, value=2)
        self.lvlDois.pack(side="left")

        self.lvlTres = tk.Radiobutton(frameNiveis, text="Nivel 3", variable=self.lvl, value=3)
        self.lvlTres.pack(side="left")

        #---------------------------
        #progress bar
        self.frameProgressBar = tk.Frame(self)
        self.frameProgressBar.pack(fil='both')

        barProgressTitle = tk.Label(self.frameProgressBar, text="Barra de progresso", anchor='w')
        barProgressTitle.pack(fill='x')

        self.barProgress = ttk.Progressbar(self.frameProgressBar, length=250, orient='horizontal', mode='determinate')
        self.barProgress.pack(fill='x')

        #---------------------------
        #tirar foto
        self.frameFotoCadastrar = tk.Frame(self)
        self.frameFotoCadastrar.pack(fill='x', anchor='center')

        self.tirarFotoLabelCadastrar = tk.Label(self.frameFotoCadastrar)

        self.tirarFotoLabelCadastrar.pack()

        frameBottom = tk.Frame(self)
        frameBottom.pack(fill='x', anchor='center')

        tirarFotoBtn = ttk.Button(frameBottom, text="Tirar fotos", width=15, command=self.tirarFotos)
        tirarFotoBtn.pack(side='left', fill='x', padx=100)

        button = ttk.Button(frameBottom, text="Ir para home", width=15, command=reinicia_gui)
        button.pack(side='right', fill='x', padx=100)

        labelBottom = tk.Label(self)
        labelBottom.pack(side='bottom')

        labelBottom = tk.Label(labelBottom, text="Ministério do Meio Ambiente", font=controller.cabecalho_font)
        labelBottom.pack(side="bottom", fill="x", pady=10)


    #USADO PARA LIMPAR E RODAR DE NOVO
    def restart(self):

        reinicia_gui()
        self.refresh()
        self.controller.show_frame("Home")

    #USADO PARA LIMPAR E RODAR DE NOVO
    def refresh(self):

        self.nomeEntry.delete(0, "end")
        self.lvl.set(0)

        self.barProgress.pack_forget()
        self.barProgress = ttk.Progressbar(self.frameProgressBar, length=250, orient='horizontal', mode='determinate')
        self.barProgress.pack(fill='x')

        self.frameFotoCadastrar.pack_forget()
        self.frameFotoCadastrar = tk.Frame(self)
        self.frameFotoCadastrar.pack(fill='x', anchor='center')

        self.tirarFotoLabelCadastrar = tk.Label(self.frameFotoCadastrar)
        self.tirarFotoLabelCadastrar.pack()

    def tirarFotos(self):

        checkName = self.checkName()
        checkNiveis = self.checkNiveis()

        if checkName == None:
            #print("Por favor informe seu nome!")
            messagebox.showerror("Error", "Por favor, informe seu nome!")
        elif checkName == False:
            #print("Por favor informe seu nome, apenas letras!")
            messagebox.showerror("Error", "Por favor, apenas letras são permitidas no campo nome!")
        else:
            
            if checkNiveis == None:
                #print("Por favor informe seu nível!")
                messagebox.showerror("Error", "Por favor, informe seu nível!")
            elif checkNiveis == False:
                #print('Por favor informe seu nível de acesso corretamente!')
                messagebox.showerror("Error", "Por favor, informe seu nível de acesso corretamente!")
            else:
                print('ok')
                # initBarProgress(self.nomeEntry.get(), self.niveisEntry.get())
                # self.capturarFace(self.nomeEntry.get(), self.niveisEntry.get())
                self.capturarFace(self.nomeEntry.get(), self.lvl.get())

    def checkName(self):

        checkName = str(self.nomeEntry.get())
        checkFlag = None

        if len(checkName) == 0:
            return checkFlag
        else:
            for eachLetter in checkName:
                if eachLetter.isalpha() == True or ord(eachLetter) == 32:
                    checkFlag = True
                else:
                    checkFlag = False
                    self.nomeEntry.delete(0,'end')

            return checkFlag

    def checkNiveis(self):

        checkNivel = str(self.lvl.get())
        checkFlag = None

        if len(checkNivel) == 0:
            return checkFlag
        else:
            for eachLetter in checkNivel:
                if eachLetter.isnumeric() == True and (eachLetter == '1' or eachLetter == '2' or eachLetter == '3') and len(eachLetter) <= 3:
                    checkFlag = True
                else:
                    checkFlag = False
                    # self.niveisEntry.delete(0,'end')
                    break

            return checkFlag

    def capturarFace(self, _name, _niveis):

        classificador = cv2.CascadeClassifier("{}/haarcascade-frontalface-default.xml".format(Path().reconhecedores))
        classificadorOlho = cv2.CascadeClassifier("{}/haarcascade-eye.xml".format(Path().reconhecedores))

        amostra = 1
        numeroAmostras = 30

        name = _name
        niveis = _niveis
        largura, altura = 200, 200
        print("Capturando...")

        messagebox.showwarning("Aviso", "Pronto?")
        id = ReferenceFile().writeReference(name, niveis)

        messagebox.showwarning("Mensagem de atenção", "Por favor, olhe para a camera e espere a barra de progresso terminar.")
        self.barProgress.start()
        self.cameraCadastrar = cv2.VideoCapture(0)

        while (True):

            time.sleep(1)
            conectado, imagem = self.cameraCadastrar.read()
            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            facesDetectadas = classificador.detectMultiScale(imagemCinza,
                                                            scaleFactor=1.5,
                                                            minSize=(150, 150))
            
            for (x, y, l, a) in facesDetectadas:

                cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)
                regiao = imagem[y:y + a, x:x + l]
                regiaoCinzaOlho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
                img = PIL.Image.fromarray(regiaoCinzaOlho)
                imgtk = ImageTk.PhotoImage(image=img)
                self.tirarFotoLabelCadastrar.imgtk = imgtk
                self.tirarFotoLabelCadastrar.configure(image=imgtk)
                
                olhosDetectados = classificadorOlho.detectMultiScale(regiaoCinzaOlho)
                for (ox, oy, ol, oa) in olhosDetectados:

                    cv2.rectangle(regiao, (ox, oy), (ox + ol, oy + oa), (0, 255, 0), 2)
                    if np.average(imagemCinza) > 110:

                        self.barProgress.update()
                        self.barProgress["maximum"]=numeroAmostras
                        self.barProgress["value"]=amostra
                        imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))                        
                        cv2.imwrite("{}/pessoa-{}-{}.jpg".format(Path().dataset, str(id), str(amostra)), imagemFace)
                        print("Foto {} capturada".format(str(amostra)))
                        amostra += 1
                       
            cv2.waitKey(1)
            if (amostra >= numeroAmostras + 1):
                break

        print("Faces Capturadas!!")
        self.cameraCadastrar.release()
        cv2.destroyAllWindows()
        self.barProgress.stop()
        self.barProgress.destroy()
        messagebox.showinfo("Pronto!", "Obrigado {}, suas fotos foram tiradas!\nVolte para home e entre no sistema.".format(self.nomeEntry.get()))
        Treinamento().runTreinamento()

def inicia_gui():
    
    global root
    root = ReconhecimentoFacial()
    root.mainloop()    

if __name__ == '__main__':
    def reinicia_gui():
        root.destroy()
        inicia_gui()

    inicia_gui()


