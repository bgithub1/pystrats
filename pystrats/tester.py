'''
Created on Feb 11, 2016

@author: sarahhartman
'''

run_pandaExamples = False
if run_pandaExamples:
    
    from utility.pyfunc import readYahoo, dsInsert, asb
    from pandas.stats.moments import rolling_mean
    import numpy as np
    from pandas.core.frame import DataFrame
     
    import pandas as pd
     
    pathmov = '/Users/sarahhartman/Dropbox/pyStuff/pydata-book-master/ch02/movielens/movies.dat'
    pathrat = '/Users/sarahhartman/Dropbox/pyStuff/pydata-book-master/ch02/movielens/ratings.dat'
    pathusers = '/Users/sarahhartman/Dropbox/pyStuff/pydata-book-master/ch02/movielens/users.dat'
     
    unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
    users = pd.read_table(pathusers, sep='::', header=None,names=unames)
    rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_table(pathrat, sep='::', header=None,names=rnames)
    mnames = ['movie_id', 'title', 'genres']
    movies = pd.read_table(pathmov, sep='::', header=None,names=mnames)
    users[:5]
    rnames[:5]

run_strat_maLong_maShort = True
if run_strat_maLong_maShort:
    from pystrats.state_strats import strat_maLong_maShort as ss
    dfretfinal = ss() #strat_maLong_maShort()
    print dfretfinal
    print dfretfinal['ret'].mean()

