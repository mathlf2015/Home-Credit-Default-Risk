#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 12:27:10 2018

@author: kazuki.onodera
"""

import os
import pandas as pd
import gc
from glob import glob
import utils
utils.start(__file__)
#==============================================================================
KEY = 'SK_ID_CURR'
No = '203'
PREF = f'pos_{No}'

NTHREAD = 2

col_num = ['MONTHS_BALANCE', 'CNT_INSTALMENT', 'CNT_INSTALMENT_FUTURE',
           'SK_DPD', 'SK_DPD_DEF']

col_cat = ['NAME_CONTRACT_STATUS']

col_group = ['SK_ID_PREV', 'NAME_CONTRACT_STATUS']

# =============================================================================
# feature
# =============================================================================
pos = utils.read_pickles('../data/POS_CASH_balance')

pos = pos[pos['MONTHS_BALANCE']==-1]

pos = utils.get_dummies(pos)
pos.drop('SK_ID_PREV', axis=1, inplace=True)

base = pos[[KEY]].drop_duplicates().set_index(KEY)

def nunique(x):
    return len(set(x))

# =============================================================================
# gr1
# =============================================================================
gr = pos.groupby(KEY)

# stats
keyname = 'gby-'+KEY
base[f'{PREF}_{keyname}_size'] = gr.size()

base = pd.concat([
                base,
                gr.min().add_prefix(f'{PREF}_').add_suffix('_min'),
                gr.max().add_prefix(f'{PREF}_').add_suffix('_max'),
                gr.mean().add_prefix(f'{PREF}_').add_suffix('_mean'),
                gr.std().add_prefix(f'{PREF}_').add_suffix('_std'),
                gr.sum().add_prefix(f'{PREF}_').add_suffix('_sum'),
#                gr.median().add_prefix(f'{PREF}_').add_suffix('_median'),
                ], axis=1)



# =============================================================================
# merge
# =============================================================================
base.reset_index(inplace=True)

train = utils.load_train([KEY])
train = pd.merge(train, base, on=KEY, how='left').drop(KEY, axis=1)
utils.to_pickles(train, f'../data/{No}_train', utils.SPLIT_SIZE)
del train; gc.collect()

test = utils.load_test([KEY])
test = pd.merge(test, base, on=KEY, how='left').drop(KEY, axis=1)
utils.to_pickles(test,  f'../data/{No}_test',  utils.SPLIT_SIZE)



#==============================================================================
utils.end(__file__)


