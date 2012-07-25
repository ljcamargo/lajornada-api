# -*- coding: utf-8 -*-
'''
Created on 20/06/2012

@author: lcammx
'''

from esp import ESP

if __name__ == '__main__':
    problem = u"El mismo día en que Enrique Peña Nieto dijo no al movimiento #YoSoy132, aceptó reunirse con las huestes de Elba Esther Gordillo. El candidato presidencial del PRI rechazó, como se sabe, asistir al debate organizado por los jóvenes, aduciendo que no le garantizaban condiciones de neutralidad y de imparcialidad. Sin embargo, aceptó asistir, este viernes, a una reunión con la cúpula del Sindicato Nacional de Trabajadores de la Educación, que desde su neutralidad respalda a otro candidato presidencial, Gabriel Quadri de la Torre, el único que hasta ahora había accedido a participar en un cónclave magisterial."
    espa = ESP()
    
    for word in problem.split():
        espa.languageEntropy(word)
    