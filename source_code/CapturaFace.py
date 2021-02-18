# -*- coding: utf-8 -*-
#! Python3

#? @author: Renan Silva
#? @github: https://github.com/rfelipesilva

import os
import cv2
import time
import numpy  as np

import tkinter     as tk
import tkinter.ttk as ttk
from tkinter       import messagebox

from Dict          import Dictionary
from Configuration import Path

class ReferenceFile:

    def __init__(self):

        self.location = Path().data_store
        self.fileCreaated = None

    def writeReference(self, name, niveis):

        self.name = name
        self.niveis = niveis

        print("{} - {}".format(self.name,str(self.niveis)))
        currentId = self.getId()
        print(currentId)

        file = open("{}\\id_with_reference.csv".format(self.location), mode="a", encoding="utf-8")
        file.write("{};{};{}\n".format(self.name, currentId, self.niveis))
        file.close()
        return currentId


    def getId(self):

        self.getFile()
        nextId = 0
        file = open("{}\\id_with_reference.csv".format(self.location), mode="r", encoding="utf-8")
        registros = file.readlines()

        if len(registros) == 1:
            print("só cabeçalho")
            nextId = 1
            return nextId
            print(nextId)
        else:
            lastId = int(registros[-1].split(";")[1])+1
            nextId = lastId
            return nextId
            print(nextId)

    def getFile(self):

        for eachFile in os.listdir(self.location):
            if "id_with_reference.csv" in eachFile:
                self.fileCreaated = True
            else: pass

        if self.fileCreaated == True:
            print("Ja existe")
            pass

        elif self.fileCreaated == None:
            with open("{}\\id_with_reference.csv".format(self.location), mode="w", encoding="utf-8") as file:
                file.write("nome;id;niveis\n")
            print("Arquivo criado")
        else:
            print("arquivo com problema")
