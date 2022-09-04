from csv import DictReader

file_handle = open("Crash Statistics Victoria.csv", "r", encoding="utf8")
csv_reader = DictReader(file_handle)
count = 0
for row in csv_reader:
    if row["ALCOHOLTIME"] == "No":
        count += 1

print(count)

file_handle.close()