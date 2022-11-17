import fitz
import re
from nltk import tokenize
import glob

DIGITIZED_FILE = "The-Tempest-Shakescleare-Translation-LitChart.pdf"
organized_file="organized.txt"
final_text="result.txt"
RE_INT = re.compile(r'^Page [-+]?([1-9]\d*|0)$')
RE_int_only = re.compile(r'^[-+]?([1-9]\d*|0).+?$')
RE_int_no_text = re.compile(r'^[-+]?([1-9]\d*|0)$')
ACT_reg = re.compile(r'^Act [-+]?([1-9]\d*|0), Scene [-+]?([1-9]\d*|0)$')
Name_reg = re.compile(r'^Shakespeare$')
trans_reg = re.compile(r'^Shakescleare Translation$')
guard_match_2 = re.compile(r'^guard$')
guard_match = re.compile(r'^Guard$')
Senator_match = re.compile(r'^Senator$')
Senator_match_2 = re.compile(r'^SeNator$')
Sentinel_match = re.compile(r'^FIRST Sentinel$')
Sentinel_match_2 = re.compile(r'^FIRSt SENTINEL$')
all_match = re.compile(r'^all$')
enter_match = re.compile(r'^Enter .+?$')
clown_match = re.compile(r'^CLOWN (.+?)$')
first_not_skip=0


def skip_header(input_str):
    if input_str==".":
        return True
    if "LitCharts LLC" in input_str or "litcharts" in input_str or "all exit." in input_str or "All exit." in input_str or "Shakescleare" in input_str:
        return False
    if RE_INT.match(input_str) or ACT_reg.match(input_str) or Name_reg.match(input_str):
        return False
    if trans_reg.match(input_str):
        return False

    return True

def skip_line(input_str, line_part):
    if guard_match_2.match(input_str) or guard_match.match(input_str) or Senator_match.match(input_str):
        return True
    if Senator_match_2.match(input_str) or Sentinel_match.match(input_str) or Sentinel_match_2.match(input_str):
        return True
    if all_match.match(input_str) and "your revenge and turn" not in line_part:
        return True
    if clown_match.match(input_str):
        return True
    if "COSTARd" in input_str or "CLOwn" in input_str or "CLOWn" in input_str:
        return True
    if "jaques" in input_str or "WINCHESTEr" in input_str:
        return True
    if input_str==".\n" or input_str==",\n":
        return False
    if "GLENDOWER" in input_str and "Enter HOTSPUR,WORCESTER, Lord MORTIMER, and Owen" in line_part:
        return False
    if "HENRY IV, PART" in input_str:
        return True
    if "clown (shepherd's son)" in input_str:
        return True
    if "HENRY VI, PART" in input_str or "FIRST lord" in input_str or "MARINER (SAILoR)" in input_str:
        return True
    if "SECOND SENATor" in input_str:
        return True
    if "TIMOn" in input_str:
        return True
    if input_str=="O\n" or input_str == "I\n":
        return False
    for char in input_str:
        if char.islower():
            return False
        if char=="." or char=="," or char=="]" or char=="[" or char=="!" or char=="?":
            return False

    if len(input_str)==0:
        return False
    if RE_int_only.match(input_str):
        return False
    if RE_int_no_text.match(input_str):
        return False
    if enter_match.match(line_part):
        return False

    return True

def skip_line_step_two(input_str):
    if input_str[0]=="=":
        return False
    return True

def check_seperation_line(input_str):
    for char in input_str:
        if char== "-":
            return True
        else:
            return False
    return True

def clean_text(input_file_name, result_file_name):
    input_file_open = open(input_file_name, 'r', encoding='UTF-8')
    result_file_open = open(result_file_name, 'w', encoding='UTF-8')

    Lines = input_file_open.readlines()
    count=-2
    line_part=""
    skip_rest=False

    for line in Lines:
        if RE_int_no_text.match(line):
            skip_rest=False
        if "contemporary language" in line:
            line_part=" A good egg , ma'am."
        if skip_line(line, line_part):
            if "NORTHUMBERLAND" in line and "NORTHUMBERLAND, LADY NORTHUMBERLAND, and LADY PERCY enter." in line_part:
                line_part=""
            if "NORFOLK enters at one door, BUCKINGHAM" in line_part and "BUCKINGHAM" in line:
                line_part=""
            if "KING HENRY VIII sits and whispers to LOVELL" in line_part and "CARDINAL WOLSEY" in line:
                line_part=""
            if "ATTENDANTS" in line and "A flourish of trumpets sounds." in line_part:
                line_part=""
            if "I wish it were true and that they were my father's sons!" in line_part:
                line_part=""
            if "What time is it, Francis?" in line_part:
                line_part=""
            if "The FRENCH KING, QUEEN ISABEL, BURGUNDY, and other LORDS enter" in line_part and "BURGUNDY" in line:
                line_part=""
            if "By my troth, most pleasant" in line_part and "COSTARD" in line:
                line_part=""
            if "You were half blasted ere I knew you." in line_part or "Give me your hand. I'll praise your deeds " in line_part or "The sevenfold shield of Ajax cannot keep" in line_part:
                line_part=""
            if "But I'll tell you what I have to say at a more appropriate" in line_part:
                line_part=""
            if "Now, Charmian! Dress me, my women," in line_part:
                line_part=""
            if "Alarum as in battle. Enter, from opposite sides" in line_part:
                line_part=""
            if "The gods begin to mock me" in line_part or "The senate, Coriolanus, are well pleased" in line_part:
                line_part=""
            if "Take't; 'tis yours. What is't?" in line_part or "And live you yet?" in line_part:
                line_part=""
            if "That any one should therefore be suspicious" in line_part:
                line_part=""
            if "Enter SUFFOLK, in a discussion with KING HENRY VI" in line_part and "KING HENRY VI" in line:
                line_part=""
            if "Yes, Margaret. My heart is drowned with grief." in line_part or "An alarm sounds. There is fighting across the stage. QUEEN MARGARET, PRINCE EDWARD, and EXETER" in line_part:
                line_part=""
            if "Open your gates.  Uncle Exeter, go enter Harfleur. Stay there and fortify it well" in line_part:
                line_part=""
            if "The soldiers John BATES, Alexander COURT, and Michael WILLIAMS enter." in line_part:
                line_part=""
            if "Go, Faulconbridge: now you have what you wanted. A landless knight makes" in line_part:
                line_part=""
            if "Lords, I am hot with haste in seeking you:" in line_part:
                line_part=""
            if "Thus wisdom wishes to appear most bright When it doth tax itself" in line_part:
                line_part=""
            if "Take, O, take those lips away, That so sweetly were forsworn;" in line_part:
                line_part=""
            if "DOGBERRY, VERGES, and Watchmen enter, along with CONRAD and BORACHIO" in line_part:
                line_part=""
            if "But shall ’t be shortly?" in line_part:
                line_part=""
            if "Trumpets and drums play military music, and soldiers fight. NORFOLK and his soldiers" in line_part:
                line_part=""
            if "Norfolk, so far as to mine enemy:   By this time, had the king permitted us," in line_part:
                line_part=""
            if "ANTIPHOLUS OF SYRACUSE, DROMIO OF SYRACUSE, and FIRST MERCHANT enter" in line_part or "ANTIPHOLUS OF EPHESUS, DROMIO OF EPHESUS, ANGELO, and BALTHASAR enter" in line_part or "SECOND MERCHANT, ANGELO, OFFICER, and ANTIPHOLUS OF EPHESUS exit" in line_part:
                line_part=""
            if "where have you left the money that I gave you?" in line_part or "his social status is too high; he's too sophisticated." in line_part:
                line_part=""
            if "ADRIANA, LUCIANA, the COURTESAN, and PINCH the Schoolmaster enter." in line_part or "The ABBESS enters with ANTIPHOLUS OF SYRACUSE and DROMIO OF SYRACUSE" in line_part:
                line_part=""
            if "PAGE, FORD, MISTRESS PAGE, MISTRESS FORD, and SIR HUGH EVANS enter" in line_part:
                line_part=""
            if "TRANIO (disguised as LUCENTIO) enters with the MERCHANT" in line_part:
                line_part=""
            if "Who is Silvia? What is she? That all our swains commend her" in line_part:
                line_part=""
            if "Nay then, the wanton lies; my face is black" in line_part:
                line_part=""
            if "Considers she my possessions?" in line_part:
                line_part=""
            if "And, madam, I must be present at your conference" in line_part or "Madam, if't please the queen to send the babe" in line_part:
                line_part=""
            if "A gross hag And, lozel, thou art worthy to be hang'd" in line_part:
                line_part=""
            if "I would you did but see how it chafes, how it rages" in line_part:
                line_part=""
            if "ACT , PROLOGUE Enter Time" in line_part or "Let me see: every 'leven wether tods" in line_part:
                line_part=""
            if "Let's see: every sheep yields eleven pounds of wool" in line_part or "They sing." in line_part:
                line_part=""
            if "It's beautiful." in line_part or "You're not a complete fool." in line_part or "Yes, but that still isn't enough." in line_part:
                line_part=""
            if "O blessed breeding sun, draw from the earth" in line_part:
                line_part=""
            if "What should they grant? what makes this pretty" in line_part:
                line_part=""
            if "PARIS, TROILUS, AENEAS, DEIPHOBUS, ANTENOR, and DIOMEDES enter" in line_part:
                line_part=""
            if "Both take and give." in line_part or "(sings) O' the twelfth day of December " in line_part or "(sings) She loves another Who calls, ha?" in line_part:
                line_part=""
            if "How does my bounteous sister? Go with me To bless this twain that they may prosperous be" in line_part:
                line_part=""
            skip_rest=False
            if count>=0:

                if len(line_part)>0 and count==0 and line_part!=" ":
                    count = (count + 1)
                    count = count % 2
                    result_file_open.write(line_part+"\n----\n")
                else:
                    if len(line_part)>0 and line_part!=" ":
                        count = (count + 1)
                        count = count % 2
                        result_file_open.write(line_part + "\n====\n")
            else:
                print(line)
                count = (count + 1)
            if "Is that so, my lords of England?" in line_part:
                break
            line_part = ""
            continue
        #skip headers and check if it need to skip rest
        if skip_header(line) and skip_rest==False:
            if RE_int_only.match(line) or "[singing]" in line or "The hobby horse" in line or "[sing]" in line or"[Singing]" in line or "[sings]" in line or "[Sings]" in line or "Go tell the hunters to wake them by blowing their horns" in line:
                skip_rest=True
                continue
            else:#clean all digits
                if any(char.isdigit() for char in line):
                    line = ''.join([i for i in line if not i.isdigit()])
                line=line.replace("\n", "")
                line=re.sub("\[.*?\]","",line)
            #    if len(line)>=2:
            #        if line[0].isupper() and line[1].islower() and line_part!="":
            #            if len(line_part)>=2:
            #                 if line_part[-2] != "." and line_part[-2] != "!"and line_part[-2] != ","and line_part[-2] != ";" and line_part[-1] != "." and line_part[-1] != "!"and line_part[-1] != "," and line_part[-1] != ";":
            #                    line=". "+line
            #            else:
            #                line = ". " + line
                line_part = line_part +" "+ line

def pdf_to_text(pdf_file_name, result_file_name):
    data_file_open = open(result_file_name, 'w', encoding='UTF-8')
    with fitz.open(pdf_file_name) as doc:
        for page in doc:
            text = page.get_text()
            text=text.replace("-", " ")
            text = text.replace("—", " ")
            text = text.replace("_", " ")
            text = text.replace("Romeo", "ROMEO")
            text = text.replace("Juliet", "JULIET")
            text = text.replace("Capulet", "CAPULET")
            text = text.replace("Montague", "MONTAGUE")
            data_file_open.write(text)



def write_data_to_file(data_file, label_file, origin_file):
    file1 = open(origin_file, 'r', encoding='UTF-8')
    data_file_open = open(data_file, 'a', encoding='UTF-8')
    label_file_open = open(label_file, 'a', encoding='UTF-8')

    Lines = file1.readlines()

    type=0
    for line in Lines:
        if skip_line_step_two(line)==True :
            if check_seperation_line(line)==True:
                type=(type+1)%2
            else:
                if type==1 :
                    label_file_open.write(line)
                else:
                    data_file_open.write(line)
        else:
            type = 0

def create_dataset(data_file, label_file, dataset_data, dataset_label):
    data_file_open = open(data_file, 'r', encoding='UTF-8')
    label_file_open = open(label_file, 'r', encoding='UTF-8')

    dataset_data_open = open(dataset_data, 'w', encoding='UTF-8')
    dataset_label_open = open(dataset_label, 'w', encoding='UTF-8')

    data_lines=data_file_open.readlines()
    label_lines = label_file_open.readlines()

    count=0

    for i in range(len(data_lines)):
        data_paragraph = data_lines[i]
        label_paragraph = label_lines[i]
        data_paragraph.replace("\n", "")
        label_paragraph.replace("\n", "")

        data_sentence_list=tokenize.sent_tokenize(data_paragraph)
        label_sentence_list =tokenize.sent_tokenize(label_paragraph)

        for j in range(min(len(data_sentence_list), len(label_sentence_list))):
            count=count+1
            dataset_data_open.write(data_sentence_list[j])
            dataset_label_open.write(label_sentence_list[j])
        dataset_data_open.write("\n")
        dataset_label_open.write("\n")

    print(count)


file_list=glob.glob("*.pdf")
#file_list=[DIGITIZED_FILE]
old_num_line_data=0
old_num_line_label=0

for file_name in file_list:

    print(file_name)
    pdf_to_text(file_name, organized_file)
    clean_text(organized_file, final_text)
    write_data_to_file("label.txt", "data.txt", final_text)

    num_lines_data = sum(1 for line in open('data.txt', encoding="UTF-8"))
    print(num_lines_data-old_num_line_data)
    num_lines_label = sum(1 for line in open('label.txt', encoding="UTF-8"))
    print(num_lines_label-old_num_line_label)

    old_num_line_data=num_lines_data
    old_num_line_label=num_lines_label

create_dataset("label.txt", "data.txt","label_f.txt", "data_f.txt")

#print(re.sub("\[.*?\]","", "[He skims the letter] This letter corroborates the friar’s story."))