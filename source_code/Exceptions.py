# -*- coding: utf-8 -*-
#! Python3

# @author
# - Renan Silva

import os

from Configuration import Path

#classe criada para verificar arquivos mandatórios
class Verify:

    def __init__(self):

        self.picturessFolder = Path().dataset
        self.filesFolder     = Path().reconhecedores
        self.model           = Path().models

    #verifica se existe fotos capturadas para treinar o modelo
    def verifyDataset(self):

        datasetAmount = os.listdir(self.picturessFolder)
        if len(datasetAmount) > 10: return True
        else: return False

    #verifica se arquivo do modelo foi criado
    def verifyClassifier(self):

        files           = os.listdir(self.model)
        checkClassifier = False
        for eachFile in files:
            if 'classificadorLBPH.yml' in eachFile:
                checkClassifier = True
            else: pass

        return checkClassifier

    #verifica se arquivos de deteccao foram criados
    def verifyDetectors(self):

        files = os.listdir(self.filesFolder)
        if 'deteccaoface.xml' and 'haarcascade-frontalface-default.xml' and 'haarcascade-frontalface-default.xml' in files:
            return True
        else: return False

    def verifyFiles(self):
        check = False
        while check == False:
            if self.verifyDataset() == False or self.verifyClassifier() == False or self.verifyDetectors == False:
                check = False
                return False
            else:
                check = True
                return True