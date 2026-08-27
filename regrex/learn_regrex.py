import regex as re

def detect_sensitive_information(text):

# \d is digit, \w is word, \s is space, [A-Z] Captial a-z, [a-z] small a-z, [0-9], ^ start with, $ ends with, + one or more occurance
    
    result = []

    # keywords that the OCR shd search for password
    keywords = ["password", "passwd", "pwd", "secret", "token", "api_key"]

 
    patterns = {
        "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]", 
        "CREDIT_CARD_NUMBER": r"\d{4} \d{4} \d{4} \d{4}" # have to mention r" " before the pattern else phton will assume its a raw string
    }


    for data_type,pattern in patterns.items():
        for match in re.finditer(pattern,text): # finds all the matchs one after the other. Syntax (what to find, where to find)
            value = match.group() # displays the output 
            start_position = match.start() # gives the starting position of the find
            end_position = match.end() # gives the end position of the find

            result.append({"value":value,
                           "start_position":start_position,
                           "End_position":end_position,
                           "Data_type":data_type})


    lower_text = text.lower()
    for keyword in keywords:
        keyword_position_start  = lower_text.find(keyword)

        if keyword_position_start != -1:
            keyword_posotion_end = keyword_position_start + len(keyword)
            valuee = text[keyword_position_start:keyword_posotion_end]

            result.append({
                "Value":valuee,
                "start_position":start_position,
                "End_position":end_position,
                "Keyword":keyword
            })





    return result


ans = detect_sensitive_information("My PAN is ABCDE1234F and my card is 1234 5678 9012 3456. Password: Tiger@123")
for item in ans:
    print(item)