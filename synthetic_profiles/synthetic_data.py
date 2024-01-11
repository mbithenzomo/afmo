from datetime import date
from faker import Faker

import numpy as np
import pandas as pd
import random

fake = Faker()

rng = np.random.default_rng()

###################################
###### generate person data #######
###################################

def get_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def generate_person_data(num):

    # person ID
    id = "person_" + num

    # demographic data
    birthdate = fake.date_of_birth(minimum_age=30,maximum_age=80)
    age = get_age(birthdate)
    sex = random.choice(["Male", "Female"])
    gender = random.choices([sex, "Nonbinary"], weights=(50, 3), k=1)[0]

    # basic information
    if gender == "Male":
        first_name = fake.first_name_male()
        title = "Mr"
    elif gender == "Female":
        first_name = fake.first_name_female()
        title = "Ms"
    else:
        first_name = fake.first_name()
        title = "Mx"
    last_name = fake.last_name()

    # lifestyle data
    smoking_status = np.random.choice(["CurrentSmoker", "FormerSmoker", "NeverSmoker"], 1, p=[0.3, 0.2, 0.5])[0]
    weekly_drinks = np.random.randint(0, 18)
    average_daily_steps = np.random.randint(2000, 15000)

    # body data
    if sex == "Male":
        height = round(rng.normal(175,10),1) # cm
        weight = round(rng.normal(82,10),1) # kg
    else:
        height = round(rng.normal(162,10),1) # cm
        weight = round(rng.normal(70,10),1) # kg
    height_m = height/100 # metres
    bmi = round(weight/(height_m*height_m),1)


    # other medical info
    af_detected = random.choice([True, False])
    antiplatelet = random.choice([True, False])
    nsaids = random.choice([True, False])
    ttr = random.randint(0, 100)

    return [id, title, first_name, last_name, str(birthdate), age, sex, gender,
    smoking_status, weekly_drinks, average_daily_steps, height, weight, bmi,
    af_detected, antiplatelet, nsaids, ttr]

person_df = pd.DataFrame(columns = ["ID", "title", "first_name", "last_name",
    "birthdate", "age", "sex", "gender", "smoking_status", "weekly_drinks",
    "average_daily_steps", "height", "weight", "bmi", "af_detected",
    "antiplatelet", "nsaids", "ttr"])

print("[START] Creating person dataframe ...")

for i in range(25):
    num = "{:03d}".format(i+1)
    person_data = generate_person_data(num)
    person_df.loc[len(person_df)] = person_data

print("[SUCCESS] Person dataframe generated")

###################################
##### generate physician data #####
###################################

def generate_physician_data(num):

    id = "physician_" + num # physician ID
    title = "Dr"
    first_name = fake.first_name()
    last_name = fake.last_name()

    return [id, title, first_name, last_name]

physician_df = pd.DataFrame(columns = ["ID", "title", "first_name", "last_name"])

print("[START] Creating physician dataframe ...")

for i in range(8):
    num = "{:03d}".format(i+1)
    physician_data = generate_physician_data(num)
    physician_df.loc[len(physician_df)] = physician_data

print("[SUCCESS] Physician dataframe generated")

###################################
##### generate condition data #####
###################################

conditions = ["AbnormalLiverPhysiology", "AbnormalLVFunction", "AbnormalRenalPhysiology",
    "Anemia", "AorticAtherosclerosis", "CongestiveHeartFailure", "DiabetesMellitus",
    "Hypertension", "MajorBleeding", "MyocardialInfarction", "PeripheralArteryDisease",
    "SleepApnoea", "IschemicStroke", "TransientIschemicAttack", "Thromboembolism", "Obesity",
    "AtrialFibrillation"]

condition_df = pd.DataFrame(columns = ["ID", "condition"])
num = 1
for condition in conditions:
    id = "condition_" + "{:03d}".format(num) # condition ID
    condition_df.loc[len(condition_df)] = [id, condition]
    num += 1

###################################
##### generate diagnosis data #####
###################################
print("[START] Creating diagnosis dataframe ...")

condition_dict = dict(zip(condition_df.ID, condition_df.condition))

# AF diagnoses
def generate_diagnosis_data_af(num):
    id = "diagnosis_" + num # diagnosis ID
    person_id = random.choice(person_df["ID"].tolist())
    condition_id = condition_df["ID"].tolist()[-1:][0]
    condition = condition_df["condition"].tolist()[-1:][0]
    physician_id = random.choice(physician_df["ID"].tolist())
    return [id, person_id, condition_id, condition, physician_id]

# Obesity diagnoses
def generate_diagnosis_data_obesity(num, person_id):
    id = "diagnosis_" + num # diagnosis ID
    cond_id_list = condition_df["ID"].tolist()
    condition_id = cond_id_list[len(cond_id_list)-2]
    cond_list = condition_df["condition"].tolist()
    condition = cond_list[len(cond_list)-2]
    physician_id = random.choice(physician_df["ID"].tolist())
    return [id, person_id, condition_id, condition, physician_id]

# Other diagnoses
def generate_diagnosis_data_others(num):
    id = "diagnosis_" + num # diagnosis ID
    person_id = random.choice(person_df["ID"].tolist())
    condition_id = random.choice(condition_df["ID"].tolist()[:-2])
    condition = condition_dict[condition_id]
    physician_id = random.choice(physician_df["ID"].tolist())
    return [id, person_id, condition_id, condition, physician_id]

diagnosis_df = pd.DataFrame(columns = ["ID", "person", "condition_id", "condition", "physician"])

unique_diagnosis = []
num = 1
# ensure 12 AF diagnoses
while len(diagnosis_df) < 12:
    diagnosis_data_af = generate_diagnosis_data_af("{:03d}".format(num))
    # ensure all person-condition combinations are unique
    if (diagnosis_data_af[1] + diagnosis_data_af[2]) not in unique_diagnosis:
        diagnosis_df.loc[len(diagnosis_df)] = diagnosis_data_af
        unique_diagnosis.append(diagnosis_data_af[1] + diagnosis_data_af[2])
    num += 1
print("[1/3] AF diagnoses generated")

# obesity diagnoses
obese_person_df = person_df.loc[person_df["bmi"] >= 30]
for person_id in obese_person_df["ID"].tolist():
    diagnosis_data_obesity = generate_diagnosis_data_obesity("{:03d}".format(num), person_id)
    diagnosis_df.loc[len(diagnosis_df)] = diagnosis_data_obesity
    num += 1
print("[2/3] Obesity diagnoses generated")

# ensure 100 total diagnoses
while len(diagnosis_df) < 100:
    diagnosis_data_others = generate_diagnosis_data_others("{:03d}".format(num))
    if (diagnosis_data_others[1] + diagnosis_data_others[2]) not in unique_diagnosis:
        diagnosis_df.loc[len(diagnosis_df)] = diagnosis_data_others
        unique_diagnosis.append(diagnosis_data_others[1] + diagnosis_data_others[2])
    num += 1
print("[3/3] Other diagnoses generated")

print("[SUCCESS] Diagnoses dataframe generated")

###################################
## generate medical history data ##
###################################
def generate_history_data(num):

    id = "history_" + num # history ID
    person = random.choice(person_df["ID"].tolist())
    condition_id = random.choice(condition_df["ID"].tolist()[:-1])
    condition = condition_dict[condition_id]

    return [id, person, condition_id, condition]

history_df = pd.DataFrame(columns = ["ID", "person", "condition_id", "condition"])

unique_history = []

print("[START] Creating medical history dataframe ...")

num = 1
# ensure 100 medical histories
while len(history_df) < 100:
    history_data = generate_history_data("{:03d}".format(num))
    # ensure all person-condition combinations are unique
    if (history_data[1] + history_data[2]) not in unique_history:
        history_df.loc[len(history_df)] = history_data
        unique_history.append(history_data[1] + history_data[2])
    num += 1

print("[SUCCESS] Medical history dataframe generated")

###################################
### add diagnosis/history data ####
##################################

print("[START] Adding other diagnoses/history data ...")

persons = person_df["ID"].tolist()
relevant_diagnoses = ["AbnormalLiverPhysiology", "AbnormalRenalPhysiology", "Anemia",
"CongestiveHeartFailure", "DiabetesMellitus", "Hypertension", "SleepApnoea",
"AtrialFibrillation"]
relevant_histories = ["IschemicStroke", "MajorBleeding", "MyocardialInfarction"]
all_person_info = []

for person_id in persons:
    person_info = []
    diagnosis_conditions = diagnosis_df.loc[diagnosis_df["person"] == person_id, "condition"].values
    history_conditions = history_df.loc[history_df["person"] == person_id, "condition"].values

    # key is the condition ID
    for key in condition_dict:
        if condition_dict[key] in relevant_diagnoses:
            # add diagnosis state for all conditions
            if condition_dict[key] not in diagnosis_conditions:
                person_info.append(False)
            else:
                person_info.append(None)

    for key in condition_dict:
        if condition_dict[key] in relevant_histories:

            # add history state for all conditions
            if condition_dict[key] not in history_conditions:
                person_info.append(False)
            else:
                person_info.append(None)

    # vascular disease
    if ("MyocardialInfarction" in history_conditions) or  ("PeripheralArteryDisease" in diagnosis_conditions) or ("AorticAtherosclerosis" in diagnosis_conditions):
        person_info.append(None)
    else:
        person_info.append(False)

    # CHF or LV dysfunction
    if ("CongestiveHeartFailure" in diagnosis_conditions) or ("AbnormalLVFunction" in diagnosis_conditions):
        person_info.append(None)
    else:
        person_info.append(False)

    # bleeding history or disposition
    if ("MajorBleeding" in history_conditions) or ("Anemia" in diagnosis_conditions):
        person_info.append(None)
    else:
        person_info.append(False)

    # history of stroke or similar
    if ("IschemicStroke" in history_conditions) or ("TransientIschemicAttack" in history_conditions) or ("Thromboembolism" in history_conditions):
        person_info.append(None)
    else:
        person_info.append(False)

    all_person_info.append(person_info)

column_names_diagn = [c + " (diagnosis)" for c in relevant_diagnoses]
column_names_hist = [c + " (history)" for c in relevant_histories]
column_names_extras = ["vascular disease", "CHF or LV dysfunction", "bleeding history or disposition", "history of stroke or similar"]
columns = column_names_diagn + column_names_hist + column_names_extras
person_info_df = pd.DataFrame(columns=columns,data=all_person_info)
person_df = pd.concat([person_df, person_info_df], axis=1, join="inner")

print("[SUCCESS] Other diagnoses/history data added to person dataframe")


# ###################################
# ##### generate symptoms data ######
# ###################################

print("[START] Creating symptom and experienced symptom dataframes ...")

symptoms = ["ChestPain", "ChestTightness", "Dizziness", "Dyspnea", "Fatigue", "Palpitation", "Syncope"]
symptom_df = pd.DataFrame(columns = ["ID", "symptom"])
num = 1

for symptom in symptoms:
    id = "symptom_" + "{:03d}".format(num) # symptom ID
    symptom_df.loc[len(symptom_df)] = [id, symptom]
    num += 1

def generate_experienced_symptom_data(num, person_id, symptom_id):
    id = "experienced_symptom_" + num # experienced symptom ID
    person_id = person_id
    symptom_id = symptom_id
    severity = random.choice(["Disabling", "Mild", "Moderate", "None", "Severe"])

    return [id, person_id, symptom_id, symptom, severity]

experienced_symptom_df = pd.DataFrame(columns = ["ID", "person_id", "symptom_id", "symptom", "severity"])

num = 1
for person_id in persons:
    for symptom_id in symptom_df["ID"].tolist():
        experienced_symptom_data = generate_experienced_symptom_data("{:03d}".format(num), person_id, symptom_id)
        experienced_symptom_df.loc[len(experienced_symptom_df)] = experienced_symptom_data
        num += 1

print("[SUCCESS] Symptom and experienced symptom dataframes generated")

# ###################################
# ######## create Excel file ########
# ###################################

print("[START] Creating Excel file ...")

with pd.ExcelWriter("data.xlsx") as writer:
    person_df.to_excel(writer, sheet_name="Persons", index=False)
    physician_df.to_excel(writer, sheet_name="Physicians", index=False)
    condition_df.to_excel(writer, sheet_name="Conditions", index=False)
    diagnosis_df.to_excel(writer, sheet_name="Diagnoses", index=False)
    history_df.to_excel(writer, sheet_name="History", index=False)
    symptom_df.to_excel(writer, sheet_name="Symptoms", index=False)
    experienced_symptom_df.to_excel(writer, sheet_name="Experienced symptoms", index=False)

print("[SUCCESS] Created Excel file")
