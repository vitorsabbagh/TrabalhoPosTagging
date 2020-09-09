# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 21:41:27 2020
@author: Geraldo
Implementação de Viterbi encontrada em
https://github.com/phvu/misc/tree/master/viterbi
Aplicação do algoritmo no problema exemplo de Jurafsky
https://web.stanford.edu/~jurafsky/slp3/8.pdf
"""
import numpy as np

p = print
'''
N: number of hidden states
'''

# A é a matriz de transição de estados
# nesse exemplo $N = 5$
# A indica $P(t_i|t{i-1})$
# onde $t_{i-1}$ são as linhas
# $t_i$ as colunas

# nosso A é levemente diferente de Jurafsky, porque <s>
# não está na primeira linha, mas em $\pi$

A = [
    [0.3777, 0.0110, 0.0009, 0.0084, 0.0584, 0.0090, 0.0025],
    [0.0008, 0.0002, 0.7968, 0.0005, 0.0008, 0.1698, 0.0041],
    [0.0322, 0.0005, 0.0050, 0.0837, 0.0615, 0.0514, 0.2231],
    [0.0366, 0.0004, 0.0001, 0.0733, 0.4509, 0.0036, 0.0036],
    [0.0096, 0.0176, 0.0014, 0.0086, 0.1216, 0.0177, 0.0068],
    [0.0068, 0.0102, 0.1011, 0.1012, 0.0120, 0.0728, 0.0479],
    [0.1147, 0.0021, 0.0002, 0.2157, 0.4744, 0.0102, 0.0017]
]

# pi, ou $\pi$ são as probabilidades a priori $P(t_i)$ usadas para o
# primeiro estado (pois não existe $P_{-1}$)

pi = [[.2767, .006, .0031, .0453, .0449, .0510, .2026]]


# B são as probabilidades de emissão das palavras exatas da sentença
# exemplo
# $P(w_i|t_i)$
# onde $t_i$ estão nas linhas e $w_i$ nas colunas
# Uma tabela real seria bem maior, pois incluiria todas as palavras
# do corpus
B = [
    [0.000032, 0, 0, 0.000048, 0],
    [0, 0.308431, 0, 0, 0],
    [0, 0.000028, 0.000672, 0, 0.000028],
    [0, 0, 0.000340, 0, 0],
    [0, 0.000200, 0.000223, 0, 0.002337],
    [0, 0, 0.010446, 0, 0],
    [0, 0, 0, 0.506099, 0]
]


# Todos os dados acima são convertidos para np.array

Anp = np.array(A)
pinp = np.array(pi).T
Bnp = np.array(B)

# A frase exemplo é a sequência $0,1,2,3,4$, indicando as colunas
# de B (Jane will back the bill)

data = [0, 1, 2, 3, 4]

# A cl


class Decoder(object):
    '''
    The Decoder class implements the Viterbi algorithm
    Parameters
    ----------
      initialProb: np.array Tx1
      The initial probability $P(t_i)$
      transProb: np.array NxN
      The transition matrix $P(t_i|t_{i-1})$
      obsProb: np.array NxT
      The emission matrix $P(w_i|t_i)$
    Attributes
    ----------
        N : int
        The number of states (tags in POS-Tagging)
        initialProb:
        A priori probability of stats ($P(t_i)$ in POST)
        transProb:
        Transition matrix ($P(t_i|t{i-1})$ in POST)
        obsProb:
        Emission matrix ($P(w_i|t_i)$ in POST)
    '''

    def __init__(self, initialProb, transProb, obsProb, obsSufixProb):
        self.N = initialProb.shape[0]
        self.initialProb = initialProb
        self.transProb = transProb
        self.obsProb = obsProb
        self.obsSufixProb = obsSufixProb
        assert self.initialProb.shape == (self.N, 1)
        assert self.transProb.shape == (self.N, self.N)
        assert self.obsProb.shape[0] == self.N  # no control over 2nd dimension

    def Obs(self, obs):
        return self.obsProb[:, obs, None]

    def ObsSufix(self, obs):
        return self.obsSufixProb[:, obs, None]

    def Decode(self, obs, obs_words, obs_sufix):
        '''
        This is the Viterbi algorithm
        Parameters
        ----------
        obs : list
            DESCRIPTION.
        Returns
        -------
        list
            List of states
        '''
        trellis = np.zeros((self.N, len(obs)))
        backpt = np.ones((self.N, len(obs)), 'int32') * -1

        # initialization
        trellis[:, 0] = np.squeeze(self.initialProb * self.Obs(obs[0]))

        t = 0
        # steps
        for t in range(1, len(obs)):
            # p('\n***trellis*** ' + str(t))
            # p(trellis)

            # p('\n***trellis[:, t - 1, None]*** ')
            # p(trellis[:, t - 1, None])
            # p('\n***self.ObsSufix(obs_sufix[t]).T)*** ')
            # p(self.ObsSufix(obs_sufix[t]).T)
            # p('\n***self.transProb*** ')
            # p(self.transProb)

            # p('\n***(trellis[:, t - 1, None].dot(self.ObsSufix(obs_sufix[t]).T) *self.transProb)*** ')
            # p((trellis[:, t - 1, None].dot(self.ObsSufix(obs_sufix[t]).T) * self.transProb))

            # p('\n***backpt*** ' + str(t))
            # p(backpt)

            # p('\n(np.tile(trellis[:, t - 1, None], [1, self.N]) * self.transProb)')
            # p((np.tile(trellis[:, t - 1, None], [1, self.N]) *
            #    self.transProb))

            # p('\nPALAVRA: ' + obs_words[t])
            if obs[t] == self.obsProb.shape[1] - 1:
                # p('asçdlakjsdsaçldjkASDASDASDAS')
                if obs_sufix[t] > 0:
                    trellis[:, t] = (
                        trellis[:, t - 1, None].dot(self.ObsSufix(obs_sufix[t]).T) * self.transProb).max(0)
                    if (np.amax(trellis[:, t])) == 0:
                        # trellis[:, t] = (
                        #     trellis[:, t - 1, None].dot(self.ObsSufix(obs_sufix[t]).T) * np.ones((self.N, self.N), 'int32')).max(0)

                        trellis[:, t] = np.ones((self.N, 1), 'int32').T 
                else:
                    # considera Prob de Obs igual para todas as tags
                    trellis[:, t] = (
                        trellis[:, t - 1, None].dot(np.ones((self.N, 1), 'int32').T) * self.transProb).max(0)

                # p('ObsSufix(obs_sufix[t])')
                # p(self.ObsSufix(obs_sufix[t]))
                # p('obs_sufix[t]')
                # p(obs_sufix[t])

            else:
                trellis[:, t] = (trellis[:, t - 1, None].dot(self.Obs(obs[t]).T) *
                                 self.transProb).max(0)
            #     p('Obs(obs[t])')
            #     p(self.Obs(obs[t]))
            #     p('obs[t]')
            #     p(obs[t])

            # p('\n***trellis*** ' + str(t))
            # p(trellis)
            # p(trellis[:, t])

            backpt[:, t] = (np.tile(trellis[:, t - 1, None], [1, self.N]) *
                            self.transProb).argmax(0)
            # p('_____________________________________________')
            # p('_____________________________________________')

        # termination
        tokens = [trellis[:, -1].argmax()]

        # p('***trellis*** -1')
        # p(trellis[:, -1])
        # p()

        # p('***tokens*** ')
        # p(tokens)
        # p()

        for i in range(len(obs) - 1, 0, -1):
            tokens.append(backpt[tokens[-1], i])

        return tokens[::-1]


# initialize
# d = Decoder(pinp, Anp, Bnp)

# # solve for sentence and print
# x = d.Decode(data)
# print(x)
