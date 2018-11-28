### The below code is pasted directly into SAS ESP at the project level to create a Python MAS Module and function
### this code is not intended to run standalone

def normalize_party(party_id, name, cr_date, member_id_1, member_inst_id_1,
                    member_id_2, member_inst_id_2,
                    member_id_3, member_inst_id_3,
                    member_id_4, member_inst_id_4,
                    member_id_5, member_inst_id_5,
                    member_id_6, member_inst_id_6):
    "Output: p_party_id, party_name, party_cr_date, party_member_inst_id"
    p_party_id = []
    party_name = []
    party_cr_date = []
    party_member_inst_id = []

    for i in range(6):

        if i == 0:
            if member_inst_id_1 > 0:
                p_party_id.append(party_id)
                party_name.append(name)
                party_cr_date.append(cr_date)
                party_member_inst_id.append(member_inst_id_1)
        elif i == 1:
            if member_inst_id_2 > 0:
                p_party_id.append(party_id)
                party_name.append(name)
                party_cr_date.append(cr_date)
                party_member_inst_id.append(member_inst_id_2)
        elif i == 2:
            if member_inst_id_3 > 0:
                p_party_id.append(party_id)
                party_name.append(name)
                party_cr_date.append(cr_date)
                party_member_inst_id.append(member_inst_id_3)
        elif i == 3:
            if member_inst_id_4 > 0:
                p_party_id.append(party_id)
                party_name.append(name)
                party_cr_date.append(cr_date)
                party_member_inst_id.append(member_inst_id_4)
        elif i == 4:
            if member_inst_id_5 > 0:
                p_party_id.append(party_id)
                party_name.append(name)
                party_cr_date.append(cr_date)
                party_member_inst_id.append(member_inst_id_5)
        elif i == 5:
            if member_inst_id_6 > 0:
                p_party_id.append(party_id)
                party_name.append(name)
                party_cr_date.append(cr_date)
                party_member_inst_id.append(member_inst_id_6)
        else:
            party_member_inst_id.append(-99)

    return p_party_id, party_name, party_cr_date, party_member_inst_id


### TEST ###
result = normalize_party(10, 'Test', 'Test Date', 1, 1001, 2, 1002, 3, 1003, 4, 1004, 5, 1005, 6, 0)

print(result)
# result = ([10, 10, 10, 10, 10],
#           ['Test', 'Test', 'Test', 'Test', 'Test'],
#           ['Test Date', 'Test Date', 'Test Date', 'Test Date', 'Test Date'],
#           [1001, 1002, 1003, 1004, 1005])

result = normalize_party(10, 'Test', 'Test Date', 1, 1001, 2, 1002, 3, 0, 4, 0, 5, 0, 6, 0)

print(result)
# result = ([10, 10], ['Test', 'Test'], ['Test Date', 'Test Date'], [1001, 1002])
