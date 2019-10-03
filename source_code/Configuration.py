# -*- coding: utf-8 -*-
#! Python3

# @author
# - Renan

import os
import sys
# -*- coding: utf-8 -*-
#! Python3

# @author
# - Renan Silva

import requests
import inspect
import argparse
import time

class Path:

    def __init__(self):

        #-- ACESSO RÁPIDO A DIRETORIOS USADOS
        self.data_store     = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())).replace("source_code", "config"))
        self.dataset        = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())).replace("source_code", "fotos"))
        self.reconhecedores = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())).replace("source_code", "reconhecedores"))
        self.models         = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())).replace("source_code", "models"))
        self.source_code    = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
     
