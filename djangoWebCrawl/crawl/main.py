from stage_1 import kikuu, kilimall, fix, jjshouse, lovelywholesale, valueco, wholesale7, \
    dealhub, snatcher, jumia, bidorbuy, ackermans, cjdropshipping, mrp, zando, yellowsubtrading
from alibaba import stage2, stage3
import time
import multiprocessing


tableList = ['kikuu', 'kilimall', 'fix', 'jjshouse', 'lovelywholesale', 'valueco', 'wholesale7', 'dealhub',
             'snatcher', 'jumia', 'bidorbuy', 'ackermans', 'cjdropshipping', 'mrp', 'zando', 'yellowsubtrading']


# 得到日期
def get_date():
    date = time.strftime('%Y-%m-%d')
    return date


def firstStage(pack, db, table, **kwargs):
    print(f'{table}的一阶段开始,当前日期为{get_date()}')
    pack.main(db, table, **kwargs)


def secondStage(offer, db, table,img_path):
    print(f'{table}的二阶段开始,当前日期为{get_date()}')
    stage2.main(offer, db, table, img_path)


def main():
    db = 'mysql02'

    while True:
        try:
            stage = int(input('Please Enter the stage you want to process:'))
            if stage not in [1, 2 ,3]:
                raise ValueError
            break
        except:
            print("Please enter the integer.")

    while True:
        try:
            table = input('Please enter the website you want to process:')
            if table not in tableList:
                raise ValueError
            break
        except ValueError:
            print("Website in not valid!")

    if stage == 1:
        if table == 'kilimall':
            while True:
                category = input("Please select from [kitchen_supply, men_shoe, women_bag]:")
                if category not in ['kitchen_supply', 'men_shoe', 'women_bag']:
                    print("Invalid input, please retry")
                    continue
                firstStage(kilimall, db, table, category=category)
                break
        elif table == 'kikuu':
            firstStage(kikuu, db, table)
        elif table == 'valueco':
            firstStage(valueco, db, table)
        elif table == 'snatcher':
            firstStage(snatcher, db, table)
        elif table == 'jumia':
            firstStage(jumia, db, table)
        elif table == 'jjshouse':
            firstStage(jjshouse, db, table)
        elif table == 'bidorbuy':
            firstStage(bidorbuy, db, table)
        elif table == 'ackermans':
            firstStage(ackermans, db, table)
        elif table == 'fix':
            firstStage(fix, db, table)
        elif table == 'dealhub':
            firstStage(dealhub, db, table)
        elif table == 'lovelywholesale':
            firstStage(lovelywholesale, db, table)
        elif table == 'wholesale7':
            firstStage(wholesale7, db, table)
        elif table == 'cjdropshipping':
            firstStage(cjdropshipping, db, table)
        elif table == 'mrp':
            idx = int(input('please enter the idx:'))
            firstStage(mrp, db, table, index=idx)
        elif table == 'zando':
            firstStage(zando, db, table)
        elif table == 'yellowsubtrading':
            firstStage(yellowsubtrading, db, table)

    elif stage == 2:
        accessToken = input('Please enter the updated access token:')
        stage2.main(stage2.offer(accessToken), db, table, f'../media/{table}_img')

    elif stage == 3:
        numRows = stage3.get_num_rows(db, table)
        print(numRows)
        lowerBound = int(input('Please enter the lower bound: '))
        upperBound = int(input('Please enter the upper bound: '))
        stage3.main(db, table, lowBound=lowerBound, upperBound=upperBound)