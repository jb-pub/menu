def find_last_items_row(ws, start):
    i = start
    while i < ws.max_row:
        val = ws[f'C{i}'].value
        if not val:
            return i
        i += 1
    return ws.max_row

def find_last_ref_col(ws, start):
    i = start
    while i < ws.max_column:
        # val = ws.cell(3, start).value
        val = ws.cell(3, i).value
        if not val:
            return i
        i += 1
    return ws.max_column

def col_next_cell(ws, col, startRow):
    r = startRow
    while r < ws.max_row:
        val = ws.cell(r, col).value
        if val:
            return r
        r += 1
    return -1


def append_subcategories(ws, bIndex, subcategories):
    cIndex = bIndex + 1
    subcatName = ws[f'B{bIndex}'].value
    subcategory = { "name": subcatName, "items": [] }
    subcategories.append(subcategory)
    last_items_row = find_last_items_row(ws, cIndex)

    for i in range(cIndex, last_items_row):
        itemName = ws[f'C{cIndex}'].value
        itemDescr = ws[f'D{cIndex}'].value
        menuItem = { "name": itemName, "description": itemDescr, "allergens": [], "sizes": []}
        subcategory["items"].append(menuItem)
        cIndex += 1
        # TODO Allergens vs infos
        for k in range(0, 17):
            allergIndex = 5 + k
            allergValue = ws.cell(i, allergIndex).value
            if allergValue:
                allergName = ws.cell(4, allergIndex).value
                menuItem["allergens"].append(allergName)

        firstRefCol = 18 + 4
        lastRefCol = find_last_ref_col(ws, firstRefCol)
        # print(openpyxl.utils.cell.get_column_letter(lastRefCol))

        for k in range(firstRefCol, lastRefCol, 3):
            ref = {
                "ref": ws.cell(i, k).value,
                "label": ws.cell(i, k + 1).value,
                "price": ws.cell(i, k + 2).value
            }

            if ref["ref"]:
                menuItem["sizes"].append(ref)

import openpyxl
import yaml
import json

from openpyxl import load_workbook

wb = load_workbook(filename = 'DATABASE_MENU_VENDITA.xlsx', data_only=True)

result = { "categories": [] }

for sheet in wb.sheetnames:
    category = { "name": sheet, "subcategories": [] }
    result["categories"].append(category)

    bIndex = 4

    ws = wb[sheet]

    append_subcategories(ws, bIndex, category["subcategories"])

    while True:
        bIndex = col_next_cell(ws, 2, bIndex + 1)
        if bIndex > -1:
            append_subcategories(ws, bIndex, category["subcategories"])
        else:
            break

yamlResult = yaml.dump(result)
jsonResult = json.dumps(result)
# print (yamlResult)

f = open("result.yml", "w")
f.write(yamlResult)
f.close()

f = open("result.json", "w")
f.write(jsonResult)
f.close()