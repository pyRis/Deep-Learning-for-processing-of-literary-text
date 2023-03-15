#!/usr/bin/env python3

def post_processing(summ:str, person_dict:dict) -> str:

    num_of_person = len(person_dict)
    for item in reversed(range(num_of_person)):
        key=f"PERSON{item}"
        summ = summ.replace(key, person_dict[key]).replace(f"Person{item}", person_dict[key])
    return summ
