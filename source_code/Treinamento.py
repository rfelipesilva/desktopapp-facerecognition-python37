# -*- coding: utf-8 -*-
#! Python3

# @author
# - Renan Silva

import cv2
import os
import numpy as np
from Configuration import Path
from Exceptions import Verify

class Treinamento:

    def __init__(self):

        self.dataset     = Path().dataset
        self.model       = Path().models
        self.verifyFiles = Verify()
        self.lbph        = cv2.face.LBPHFaceRecognizer_create()

    def getImagemComId(self):

        caminhos = [os.path.join('{}'.format(self.dataset), f) for f in os.listdir('{}'.format(self.dataset))]
        faces = []
        ids = []

        for caminhoImagem in caminhos:
            imagemFace = cv2.cvtColor(cv2.imread(caminhoImagem), cv2.COLOR_BGR2GRAY)
            id = int(os.path.split(caminhoImagem)[-1].split('-')[1])
            ids.append(id)
            faces.append(imagemFace)
        return np.array(ids), faces

    def treinarMaquina(self):

        ids, faces = self.getImagemComId()

        checkFile = True

        for each in os.listdir(self.model):
            if "classificadorLBPH.yml" in each:
                os.remove('{}\classificadorLBPH.yml'.format(self.model))
            else:
                pass

        try:
            print("Criando treinamento")
            self.lbph.train(faces, ids)
            self.lbph.write("{}\\classificadorLBPH.yml".format(self.model))

            print("Treinamente concluido")
        except:
            print("Erro no treinamento do modelo")

    def runTreinamento(self):

        if self.verifyFiles.verifyDataset() == True:

            self.treinarMaquina()
            return True

        else:
            print('Voce nao tem um dataset de treino! Por favor, cadastre primeiro')
            return False