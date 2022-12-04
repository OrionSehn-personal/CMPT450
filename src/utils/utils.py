
# Load CSV names for data folder
def load_csv_names():
    import os
    csv_names = []
    for file in os.listdir("data"):
        if file.endswith(".csv"):
            csv_names.append(file)
    return csv_names