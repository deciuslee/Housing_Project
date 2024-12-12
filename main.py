# Jonathan Lee
# Purpose: Housing Project Assignment


import pandas as pd
import random
import time
import mysql.connector

from files import zipFile

try:
    # Read the zip file into a Pandas DataFrame
    df = pd.read_csv(zipFile)

    # Clean 'guid' and 'zip_code' columns
    def clean_guid(row):
        guid = str(row['guid'])   # Function to clean 'guid' column
        if len(guid) != 36:
            return None
        return guid

    def clean_zip_code(row):
        # Function to clean 'zip_code' column
        zip_code = str(row['zip_code'])
        if len(zip_code) != 5 or not zip_code.isdigit():
            state = row['state']

            # Find nearby state ZIP code if current ZIP is invalid
            matching_state = df[(df['state'] == state) & (df['zip_code'].apply(lambda x: str(x).isdigit()))]
            if not matching_state.empty:
                # Manipulate ZIP code to create a new one
                nearby_state_zip = str(matching_state.iloc[-1]['zip_code'])
                first_digit = nearby_state_zip[0]
                new_zip = first_digit + '0000'
                return int(new_zip)
            else:
                # If no valid nearby state ZIP code is found, return None (empty value)
                return None  # If no valid nearby state ZIP code is found
        # Convert zip_code to int if valid
        return int(zip_code)

    # Apply cleaning functions to DataFrame columns
    df['guid'] = df.apply(clean_guid, axis=1)
    df.dropna(subset=['guid'], inplace=True)

    df['zip_code'] = df.apply(clean_zip_code, axis=1)

    # Save the cleaned DataFrame to a new CSV file
    cleaned_zip_code = 'cleaned_zip_city_county_state.csv'
    df.to_csv(cleaned_zip_code, index=False)

except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"An error has occurred: {e}")


# Clean and process of income file data
from files import incomeFile

def clean_median_income(income):
    try:
        if not str(income).isdigit():
            # Generate a random number between 100,000 and 750,000 for corrupt data
            return random.randint(100000, 750000)
        return int(income)
    except Exception as e:
        print(f"An error occurred while cleaning median income: {e}")
        return None

try:
    income_df = pd.read_csv(incomeFile)

    # Clean the 'guid' column
    income_df['guid'] = income_df.apply(clean_guid, axis=1)
    income_df.dropna(subset=['guid'], inplace=True)

    # Clean the 'median_income' column
    income_df['median_income'] = income_df['median_income'].apply(clean_median_income)

    # Drop the 'zip_code' column
    income_df.drop('zip_code', axis=1, inplace=True)

    # Save the cleaned file
    cleaned_income_file = 'cleaned_income-info.csv'
    income_df.to_csv(cleaned_income_file, index=False)

except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"An error has occurred: {e}")

# Clean and process housing file data
from files import housingFile

def clean_housing_median_age(age):
    try:
        if not str(age).isdigit():
            return random.randint(10, 50)
        return int(age)
    except Exception as e:
        print(f"An error occurred while cleaning housing_median_age: {e}")
        return None

def clean_total_rooms(rooms):
    try:
        if not str(rooms).isdigit():
            return random.randint(1000, 2000)
        return int(rooms)
    except Exception as e:
        print(f"An error occurred while cleaning total_rooms: {e}")
        return None

def clean_total_bedrooms(bedrooms):
    try:
        if not str(bedrooms).isdigit():
            return random.randint(1000, 2000)
        return int(bedrooms)
    except Exception as e:
        print(f"An error occurred while cleaning total_bedrooms: {e}")
        return None

def clean_population(population):
    try:
        if not str(population).isdigit():
            return random.randint(5000, 10000)
        return int(population)
    except Exception as e:
        print(f"An error occurred while cleaning population: {e}")
        return None

def clean_households(households):
    try:
        if not str(households).isdigit():
            return random.randint(500, 2500)
        return int(households)
    except Exception as e:
        print(f"An error occurred while cleaning households: {e}")
        return None

def clean_median_house_value(value):
    try:
        if not str(value).isdigit():
            return random.randint(100000, 250000)
        return int(value)
    except Exception as e:
        print(f"An error occurred while cleaning median_house_value: {e}")
        return None

try:
    housing_df = pd.read_csv(housingFile)
    housing_df['guid'] = housing_df.apply(clean_guid, axis=1)
    housing_df.dropna(subset=['guid'], inplace=True)
    housing_df['housing_median_age'] = housing_df['housing_median_age'].apply(clean_housing_median_age)
    housing_df['total_rooms'] = housing_df['total_rooms'].apply(clean_total_rooms)
    housing_df['total_bedrooms'] = housing_df['total_bedrooms'].apply(clean_total_bedrooms)
    housing_df['population'] = housing_df['population'].apply(clean_population)
    housing_df['households'] = housing_df['households'].apply(clean_households)
    housing_df['median_house_value'] = housing_df['median_house_value'].apply(clean_median_house_value)
    housing_df.drop('zip_code', axis=1, inplace=True)

    cleaned_housing_file = 'cleaned_housing_data.csv'
    housing_df.to_csv(cleaned_housing_file, index=False)

except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"An error has occurred: {e}")


# Read three cleaned files
cleaned_zip_file = 'cleaned_zip_city_county_state.csv'
cleaned_income_file = 'cleaned_income-info.csv'
cleaned_housing_file = 'cleaned_housing_data.csv'

# Read CSV files into Pandas DataFrame
zip_df = pd.read_csv(cleaned_zip_file)
income_df = pd.read_csv(cleaned_income_file)
housing_df = pd.read_csv(cleaned_housing_file)

# Merge data with the same 'guid' column
combined_data = pd.merge(zip_df, income_df, on='guid')
combined_data = pd.merge(combined_data, housing_df, on='guid')

# Save merged data to 'combined_data.csv' file
combined_data.to_csv('combined_data.csv', index=False)



####MySQL####



# MySQL credential configurations.
hostname = 'hostname'
username = 'username'
password = 'password'
database_name = 'housing_project'
csv_file_path = 'combined_data.csv'

try:
    # Establish MySQL database connection
    connection = mysql.connector.connect(
        host=hostname,
        user=username,
        password=password,
        database=database_name
    )

    # Read the CSV file into DataFrame
    combined_data = pd.read_csv(csv_file_path)

    # Create a cursor to execute SQL commands
    cursor = connection.cursor()

    # Insert data from DataFrame into the housing table in MySQL database.
    insert_query = """
        INSERT INTO housing 
        (`guid`, `zip_code`, `city`, `state`, `county`, `housing_median_age`, 
        `total_rooms`, `total_bedrooms`, `population`, `households`, `median_income`, `median_house_value`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Iterate through the Pandas DataFrame and insert rows into the table
    for index, row in combined_data.iterrows():
        values = (
            row['guid'], row['zip_code'], row['city'], row['state'], row['county'],
            row['housing_median_age'], row['total_rooms'], row['total_bedrooms'],
            row['population'], row['households'], row['median_income'], row['median_house_value']
        )
        cursor.execute(insert_query, values)

    # Commit changes
    connection.commit()

except FileNotFoundError as e:
    print(f"File not found: {e}")
except mysql.connector.Error as e:
    print(f"MySQL database error: {e}")
except pd.errors.EmptyDataError as e:
    print(f"Empty data error: {e}")
except Exception as e:
    print(f"An error has occurred: {e}")




try:
    print("Beginning import")
    time.sleep(1)
    print("Cleaning Housing File data")
    time.sleep(1)
    num_records_imported = len(combined_data)
    print(f"{num_records_imported} records imported into the database")

    # Similar printing and sleep for Income and ZIP File data
    time.sleep(1)
    print("Import completed")
    time.sleep(1)
    print()
    print("Beginning validation")
    print()
    time.sleep(1)

    # User input prompt for total rooms
    total_rooms_input = input("Total rooms: ")
    total_rooms = int(total_rooms_input)

    # Execute SQL query to find total bedrooms for locations with more than 'total_rooms'
    query = f"SELECT SUM(total_bedrooms) AS total_bedrooms FROM housing WHERE total_rooms > {total_rooms}"
    cursor.execute(query)
    result = cursor.fetchone()
    total_bedrooms = result[0] if result else 0

    print(f"For locations with more than {total_rooms} rooms, there are a total of {total_bedrooms} bedrooms.")
    print()

    while True:
        # User input prompt for ZIP code
        zipcode_input = input("ZIP code: ")

        try:
            zipcode = int(zipcode_input)

            # Execute SQL query to find the median household income for the ZIP code input
            query = f"SELECT median_income FROM housing WHERE zip_code = {zipcode}"
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                median_income = result[0]
                print(f"The median household income for ZIP code {zipcode} is ${median_income:,}.")
                break
            else:
                print("Database does not have this ZIP code. Please enter a valid ZIP code.")

        except ValueError:
            print("Please enter a valid ZIP code.")

    for _ in cursor:
        pass

    # close cursor and connection
    cursor.close()
    connection.close()

    time.sleep(1)
    print()
    print("Program exiting.")

except FileNotFoundError as e:
    print(f"File not found: {e}")
except mysql.connector.Error as e:
    print(f"MySQL database error: {e}")
except pd.errors.EmptyDataError as e:
    print(f"Empty data error: {e}")
except Exception as e:
    print(f"An error has occurred: {e}")