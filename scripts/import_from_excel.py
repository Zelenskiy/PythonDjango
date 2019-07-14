import openpyxl
from plan.models import Plan, Purpose, Responsibl, Direction, Rubric


def var_to_str(v):
    if v is None:
        return ''
    else:
        return str(v)

def var_to_int(v):
    if v is None:
        return 0
    else:
        return int(v)

def var_to_float(v):
    if v is None:
        return 0
    else:
        return float(v)



def imp_1(self):
    print("Починаю експортувати")

    wb = openpyxl.load_workbook('d:/MyDoc/Dropbox/BASE/1/1.xlsx')
    sheet = wb['Sheet1']
    # Рахуємо кількість заповнених рядків у таблиці Excel. У n номер останнього рядка з даними
    n = 1
    k = 1
    s = str(sheet['A' + str(n)].value)
    while k is not None:
        n += 1
        s = str(sheet['A' + str(n)].value)
        try:
            k = int(s)
        except:
            break
        # print(str(n)+'. '+s)
    # IDENT	ID_R	ZMIST	STROKI	FORMA	VIDPOV	PRIMITKA	SORT_	ID_NAPR	ID_META	TMP	SHOW
    for r in range(2, n):
        print(var_to_str(sheet['A' + str(r)].value))
        p = Plan()
        p.tmp2 = var_to_str(sheet['A' + str(r)].value)
        p.r_id = int(var_to_str(sheet['B' + str(r)].value))
        p.content = var_to_str(sheet['C' + str(r)].value)
        p.termin = var_to_str(sheet['D' + str(r)].value)
        p.generalization = var_to_str(sheet['E' + str(r)].value)
        p.responsible = var_to_str(sheet['F' + str(r)].value)
        p.note = var_to_str(sheet['F' + str(r)].value)

        p.sort = var_to_float(sheet['H' + str(r)].value)
        p.direction_id = var_to_int(sheet['I' + str(r)].value)
        p.purpose_id = var_to_int(sheet['J' + str(r)].value)
        p.tmp = var_to_str(sheet['K' + str(r)].value)
        if var_to_str(sheet['K' + str(r)].value) == '1':
            p.show = True
        else:
            p.show = False
        p.save()
    wb.close()

    print("Експорт завершено")

def imp_2(self):
    print("Починаю експортувати")

    wb = openpyxl.load_workbook('d:/MyDoc/Dropbox/BASE/1/meta.xlsx')
    sheet = wb['Sheet1']
    # Рахуємо кількість заповнених рядків у таблиці Excel. У n номер останнього рядка з даними
    n = 1
    k = 1
    s = str(sheet['A' + str(n)].value)
    while k is not None:
        n += 1
        s = str(sheet['A' + str(n)].value)
        try:
            k = int(s)
        except:
            break
        # print(str(n)+'. '+s)
    # IDENT	ID_R	ZMIST	STROKI	FORMA	VIDPOV	PRIMITKA	SORT_	ID_NAPR	ID_META	TMP	SHOW
    for r in range(2, n):
        print(var_to_str(sheet['A' + str(r)].value))
        p = Purpose()
        p.tmp = var_to_str(sheet['A' + str(r)].value)
        p.name = var_to_str(sheet['B' + str(r)].value)

        p.save()
    wb.close()

    print("Експорт завершено")

def imp_3(self):
    print("Починаю експортувати")

    wb = openpyxl.load_workbook('d:/MyDoc/Dropbox/BASE/1/napr.xlsx')
    sheet = wb['Sheet1']
    # Рахуємо кількість заповнених рядків у таблиці Excel. У n номер останнього рядка з даними
    n = 1
    k = 1
    s = str(sheet['A' + str(n)].value)
    while k is not None:
        n += 1
        s = str(sheet['A' + str(n)].value)
        try:
            k = int(s)
        except:
            break
        # print(str(n)+'. '+s)
    for r in range(2, n):
        print(var_to_str(sheet['A' + str(r)].value))
        p = Direction()
        p.tmp = var_to_int(sheet['A' + str(r)].value)
        p.name = var_to_str(sheet['B' + str(r)].value)

        p.save()
    wb.close()

    print("Експорт завершено")

def imp_4(self):
    print("Починаю експортувати")

    wb = openpyxl.load_workbook('d:/MyDoc/Dropbox/BASE/1/rozd.xlsx')
    sheet = wb['Sheet1']
    # Рахуємо кількість заповнених рядків у таблиці Excel. У n номер останнього рядка з даними
    n = 1
    k = 1
    s = str(sheet['A' + str(n)].value)
    while k is not None:
        n += 1
        s = str(sheet['A' + str(n)].value)
        try:
            k = int(s)
        except:
            break
        # print(str(n)+'. '+s)
    for r in range(2, n):
        print(var_to_str(sheet['A' + str(r)].value))
        p = Rubric()
        p.id_1 = var_to_int(sheet['A' + str(r)].value)
        p.n_r = var_to_int(sheet['B' + str(r)].value)
        p.name = var_to_str(sheet['C' + str(r)].value)
        p.id_owner = var_to_int(sheet['D' + str(r)].value)
        p.riven = var_to_int(sheet['E' + str(r)].value)

        p.save()
    wb.close()

    print("Експорт завершено")

if __name__ == '__main__':
    pass

