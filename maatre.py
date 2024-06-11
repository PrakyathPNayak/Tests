import os
last_pos = 0
second_last_pos = 0
j = -1
word = input("Type the word in Kannada(Please use standard format if possible):")
split_form = list(word)
maatre = [0] * (len(word) + 10)
for i in range(len(word)):
    if not split_form[i] in "ಿ  ೆ  ್ ಯ ಮ" and split_form[i-1] != '್':
        j += 1
    if split_form[i] in 'ಯ ಮ ':
        j += 2
    if split_form[i] in "ಾ ಿ ೀ ು ೂ ೃ  ೆ ೇ ೈ ೊ ೋ  ೌ ಂ ಃ" and split_form[i] != ' ':
        if split_form[i] in " ಾ ೀ ೂ ೇ ೈ ೋ  ೌ ಂ ಃ":
            maatre[last_pos] = 2
    elif split_form[i] == "್":
        maatre[second_last_pos] = 2
    elif split_form[i-1] != "್" and split_form[i] != " ":
        second_last_pos = last_pos
        last_pos = j
        maatre[last_pos] = 1
os.system('cls')
print("Done calculating!")
print("".join("u" if maatre[i] == 1 else "_" if maatre[i] == 2 else " " for i in range(len(word) + 10)))
print(word)
