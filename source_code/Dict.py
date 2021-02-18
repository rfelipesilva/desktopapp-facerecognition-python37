# -*- coding: utf-8 -*-
#! Python3

#? @author: Renan Silva
#? @github: https://github.com/rfelipesilva

from Configuration import Path

class Dictionary:

    def __init__(self):

        self.path = Path().data_store+"\\id_with_reference.csv"
        self.textFilePath = Path().data_store
        self.dictionary_id = self.getId()
        self.dictionary_lvl = self.getLvl()

    def getId(self):

        """This function returna dictionary of ids

        Returns:
            {str} -- A dictionary of ids
        """

        file = open("{}".format(self.path), mode="r", encoding="utf-8")
        registros = file.readlines()

        dict_id_with_reference = {}
        
        for each in registros:
            if "nome" in each: pass
            else:
                registroSplited = each.split(";")
                dict_id_with_reference[registroSplited[1].replace('\n','')] = registroSplited[0]

        return dict_id_with_reference

    def getLvl(self):

        """This function returna dictionary of levels

        Returns:
            {str} -- A dictionary of levels
        """

        file = open("{}".format(self.path), mode="r", encoding="utf-8")
        registros = file.readlines()

        dict_lvl_with_reference = {}

        for each in registros:
            if "nome" in each: pass
            else:
                registroSplited = each.split(";")
                dict_lvl_with_reference[registroSplited[1].replace('\n','')] = registroSplited[2]

        return dict_lvl_with_reference

    def getText(self, lvl):

        """This function will provide the text for specific lvl informed

        Arguments:
            lvl {str} -- A string

        Returns:
            {str} -- A string that corresponds a specific text file
        """
        
        listaOfLines = open("{}/texto{}.txt".format(self.textFilePath, lvl), mode="r", encoding="utf-8")

        return listaOfLines.read()
