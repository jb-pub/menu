def find_last_items_row(ws, start):
    i = start
    while  i < ws.max_row:
        val = ws[f'C{i}'].value
        if not val:
            return i
        i += 1
    return ws.max_row

def find_last_ref_col(ws, start):
    i = start
    while  i < ws.max_column:
        val = ws.cell(3, start).value
        if not val:
            return i
        i += 1
    return ws.max_column

import openpyxl
import yaml
import json

from openpyxl import load_workbook

wb = load_workbook(filename = 'DATABASE_MENU_VENDITA.xlsx', data_only=True)

result = {}

result["categories"] = []

catIndex = 0 # TODO

for sheet in wb.sheetnames:
    result["categories"].append({ "name": sheet, "subcategories": [] })

    # subcatIndex = 0
    bIndex = 4
    cIndex = 5

    if sheet == "BIRRE": # TODO
        ws = wb[sheet]

        subcatName = ws[f'B{bIndex}'].value

        subcategories = result["categories"][catIndex]["subcategories"]
        subcategory = { "name": subcatName, "items": [] }
        subcategories.append(subcategory)
        
        last_items_row = find_last_items_row(ws, 5)

        for i in range(cIndex, last_items_row):
            itemName = ws[f'C{cIndex}'].value
            itemDescr = ws[f'D{cIndex}'].value
            menuItem = { "name": itemName, "description": itemDescr, "allergens": [], "refs": []}
            subcategory["items"].append(menuItem)
            cIndex += 1

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
                    "size": ws.cell(i, k + 1).value,
                    "price": ws.cell(i, k + 2).value
                }

                if ref["ref"]:
                    menuItem["refs"].append(ref)

        cIndex = last_items_row

yamlResult = yaml.dump(result)
jsonResult = json.dumps(result)
# print (yamlResult)

f = open("result.yml", "w")
f.write(yamlResult)
f.close()

f = open("result.json", "w")
f.write(jsonResult)
f.close()