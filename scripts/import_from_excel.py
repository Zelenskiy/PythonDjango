import openpyxl
from plan.models import Plan, Purpose, Responsibl, Direction, Rubric, Plantable


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


def start_import():  # Тут точка входу
    print('УВАГА!!!'
          'У папці d:/MyDoc/Dropbox/BASE/1/ мають розміщатися експортовані '
          'з IBExpert таблиці з іменами'
          'plan.xlsx, rozd.xlsx, meta.xlsx, napr.xlsx')

    pl_table = Plantable()
    pl_table.name = "asdfg"
    pl_table.save()
    pt_id = pl_table.id
    print("Створили Plantable з id=" + str(pt_id))



    imp_4(pt_id)

    imp_2(pt_id)
    imp_3(pt_id)

    imp_1(pt_id)

    # Випраляємо посилання на id в Rubric
    rubrics = Rubric.objects.filter(plantable_id=pt_id)
    for rubric in rubrics:
        id_owner_old = rubric.ownertmp
        per = Rubric.objects.filter(plantable_id=pt_id, ident=id_owner_old)[0]
        i_id = per.id
        rubric.id_owner = Rubric.objects.get(pk=i_id)
        rubric.save()
    # Випраляємо посилання в Plan
    plans = Plan.objects.filter(plantable_id=pt_id)
    for plan in plans:
        direction_old = plan.direction
        per = Direction.objects.filter(plantable_id=pt_id, ident=direction_old)[0]
        i_id = per.id
        plan.direction_id = Direction.objects.get(pk=i_id)

        purpose_old = plan.purpose
        per = Purpose.objects.filter(plantable_id=pt_id, ident=purpose_old)[0]
        i_id = per.id
        plan.purpose_id = Purpose.objects.get(pk=i_id)

        rubric_old = plan.rubric
        per = Rubric.objects.filter(plantable_id=pt_id, ident=rubric_old)[0]
        i_id = per.id
        plan.r_id = Rubric.objects.get(pk=i_id)

        plan.save()

def imp_1(pt_id):
    print("Починаю експортувати")

    wb = openpyxl.load_workbook('d:/MyDoc/Dropbox/BASE/1/plan.xlsx')
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
        p.ident = var_to_str(sheet['A' + str(r)].value)
        p.rubric = int(var_to_str(sheet['B' + str(r)].value))
        p.content = var_to_str(sheet['C' + str(r)].value)
        p.termin = var_to_str(sheet['D' + str(r)].value)
        p.generalization = var_to_str(sheet['E' + str(r)].value)
        p.responsible = var_to_str(sheet['F' + str(r)].value)
        p.note = var_to_str(sheet['G' + str(r)].value)

        p.sort = var_to_float(sheet['H' + str(r)].value)
        p.direction = var_to_int(sheet['I' + str(r)].value)
        p.purpose = var_to_int(sheet['J' + str(r)].value)
        p.tmp = var_to_str(sheet['K' + str(r)].value)
        p.plantable_id = Plantable.objects.get(pk=pt_id)
        if var_to_str(sheet['K' + str(r)].value) == '1':
            p.show = True
        else:
            p.show = False

        p.save()
    wb.close()

    print("Експорт завершено")


def imp_2(pt_id):
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
        p.ident = var_to_str(sheet['A' + str(r)].value)
        p.name = var_to_str(sheet['B' + str(r)].value)
        p.plantable_id = Plantable.objects.get(pk=pt_id)
        p.save()
    wb.close()

    print("Експорт завершено")


def imp_3(pt_id):
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
        p.ident = var_to_int(sheet['A' + str(r)].value)
        p.name = var_to_str(sheet['B' + str(r)].value)
        p.plantable_id = Plantable.objects.get(pk=pt_id)

        p.save()
    wb.close()

    print("Експорт завершено")


def imp_4(pt_id):
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
        p.ident = var_to_int(sheet['A' + str(r)].value)
        p.n_r = var_to_int(sheet['B' + str(r)].value)
        p.name = var_to_str(sheet['C' + str(r)].value)
        # p.id_owner = var_to_int(sheet['D' + str(r)].value)
        p.ownertmp = var_to_int(sheet['D' + str(r)].value)
        p.plantable_id = Plantable.objects.get(pk=pt_id)
        p.riven = var_to_int(sheet['E' + str(r)].value)

        p.save()
    wb.close()

    print("Експорт завершено")


"""
delete from plan_direction where true ;
delete from plan_plan where true ;
delete from plan_purpose where true ;
delete from plan_responsibl where true ;
delete from plan_rubric where true ;
delete from plan_terms where true ;


"""
