from tika import parser
import csv
import os

# take in line & month_set 
# return country name
#
def getCountryName(line_with_country_name):
    months = set(['January', 'February', 'March', 'April', 'May', 'June', 'July',\
          'August', 'September', 'October', 'November', 'December']) 
    country = ""
    for word in line_with_country_name.split():
        if word in months:
            break
        country += word + " "
    return country.replace(' ', '_')[:-1]


# take in metric_list, file_name
# return stop_index & dictionary (having data for large_territory)
#
def processBigTerritory(metric_list, file_name):
    searchfile = open(file_name, "r",encoding='utf-8')
    line_list = searchfile.readlines()  # read all lines into a list
    
    big_territory_data = {}
    
    for index, line in enumerate(line_list):  # enumerate the list and loop through it
        # to grab country name
        if "COVID-19 Community Mobility Report" in line:
            line_with_country_name = str(line_list[index+2])
            country = getCountryName(line_with_country_name)
            big_territory_data['Territory'] = country
        

        # stop at first Residential
        if metric_list[-1] in line:
            big_territory_data[metric_list[-1]] = str(line_list[index+2]).split(" ")[0][:-1]
            stop_index = index + 1
            break
        
        for metric in metric_list:
            if metric in line:
                big_territory_data[metric] = str(line_list[index+2]).split(" ")[0][:-1]
                
    searchfile.close()
    return big_territory_data, stop_index


# take in stop_index (and metric_list, file_name)
# return list[dictionaries], each dictionary contains data for a small_territory
#
def processSmallTerritory(stop_index, metric_list, file_name):
    searchfile = open(file_name, "r",encoding='utf-8')
    line_list = searchfile.readlines()  # read all lines into a list
    test_data = line_list[stop_index:]
    
    small_territory_data_list = []
    small_territory_data = {}
    for line_num, new_line in enumerate(test_data): 
        for metric in metric_list:
            if metric in new_line:
                # to grab county name
                if metric == "Retail & recreation": 
                    small_territory_data["Territory"] = str(test_data[line_num-2][:-1]).replace(' ', '_') 
                    small_territory_data["Retail & recreation"]= str(test_data[line_num+2]).split(" ")[0]

                if metric == 'Residential':
                    small_territory_data['Residential'] = str(test_data[line_num+2]).split(" ")[0]
                    small_territory_data_list.append(small_territory_data)
                    small_territory_data = {}
                
                elif metric != 'Retail & recreation' and metric != 'Residential':
                    value = str(test_data[line_num+2])
                    if value == 'Not enough data for this date\n':
                        small_territory_data[metric] = value[:-1]
                    else: 
                        small_territory_data[metric] = value.split(" ")[0]
    
    searchfile.close()
    return list(small_territory_data_list)


# take in path_to_file
# output csv files, no "return" 
#
def scrapePDFtoCSV(path_to_file):
    # ------------------------- Prepocess to temp_file ------------------------        
    # Parse data from file
    file_data = parser.from_file(path_to_file)
    # Get files text content
    text = file_data['content']
    
    # instead of passing a huge string to support functions, better write into a temp_file and pass the filename 
    with open('temp_text.txt','wt', encoding='utf-8') as text_file:
        text_file.write(file_data['content'])
        text_file.close()

    metric_list = ['Retail & recreation', 'Grocery & pharmacy', 'Parks', 'Transit stations', 'Workplace', 'Residential']
    file_data = [] # list of dictionaries to write to csv


    # ------------------ Process big territory -------------------
    big_territory_data, stop_index = processBigTerritory(metric_list, 'temp_text.txt')

    # ---------------- Process smaller territories -----------------
    small_territory_list = processSmallTerritory(stop_index, metric_list, 'temp_text.txt')

    # ------------------ Merge 2 territory data into file_data list ----------------
    small_territory_list.insert(0, big_territory_data)
    file_data = small_territory_list

    # ------------------------ Prepare to write -----------------------------
    date_published = path_to_file.split('\\')[1].split('_')[0] + "_"
    big_territory_name = str(big_territory_data['Territory'])
    storage_path = os.path.join("./csv", date_published + big_territory_name + ".csv")
                                        
    if path_to_file.find('_US_') != -1:
        storage_path = os.path.join("./csv", "US", date_published + big_territory_name + ".csv")
    
    # ------------------------ Write to CSV -----------------------------
    myFile = open(storage_path, 'w', newline='', encoding='utf-8')
    with myFile:    
        columns = ['Territory','Retail & recreation', 'Grocery & pharmacy', 'Parks', 'Transit stations', 'Workplace', 'Residential']
        # columns = ['Territory'].append(metrics_list)

        writer = csv.DictWriter(myFile, fieldnames=columns, dialect='excel')    
        writer.writeheader()
        for entity in file_data:
            writer.writerow(entity)

def main():
    for filename in os.listdir('./pdfs'):
        scrapePDFtoCSV(os.path.join('./pdfs',filename))

if __name__ == "__main__":
    main()