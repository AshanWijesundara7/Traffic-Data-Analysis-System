# Author: Ashan Malidu Wijesundara
# Date: 2024.12.24
# Student ID: [20230392]

import csv
import tkinter as tk
from collections import defaultdict

# Task A: Input Validation
def validate_date_input(error_message="Invalid input! Please enter integers for date, month, and year."):
    while True:
        print(" Please Enter the date of the survey: (DD/MM/YYYY)")
        try:
            # Get the user input 
            date = int(input("Date (DD): "))
            # Check the values are in the range
            if date < 1 or date > 31:     
                print("Out of Range! Values must be in range 1 - 31.")
                continue
            
            month = int(input("Month (MM): "))
            if month < 1 or month > 12:
                print("Out of Range! Values must be in range 1 - 12.")
                continue
            
            year = int(input("Year (YYYY): "))
            if year < 2000 or year > 2024:
                print("Out of Range! Values must be in the range 2000 - 2024.")
                continue
            # Return the validated values
            return date, month, year 
        # Handle the invalid inputs    
        except ValueError:
            print(error_message)

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        choice = input("Do you like to analyze another file? (Y/N): ")
        choice = choice.strip()
        if choice.lower() == "y":
            return choice
        elif choice.lower() == "n":
            return choice
        else:
            print("Invalid input! Please enter (Y or N)")

# Task B: Processed Outcomes

def process_csv_data(file_name):
    """
    Processes the CSV data for the selected date and extracts outcomes.
    """
    outcomes = {
        "total_vehicles": 0,
        "total_trucks": 0,
        "electric_vehicles": 0,
        "two_wheeled_vehicles": 0,
        "buses_north": 0,
        "non_turning_vehicles": 0,
        "truck_percentage": 0,
        "average_bicycles_per_hour": 0,
        "speeding_vehicles": 0,
        "elm_vehicles": 0,
        "hanley_vehicles": 0,
        "scooter_percentage": 0,
        "peak_hour_vehicles": 0,
        "peak_hour_times": [],
        "rain_hours": 0,
    }
    
    try:       
        # Open the CSV file and read its contents
        with open(file_name, mode='r') as file:  
            reader = csv.DictReader(file)
            hourly_count = {}
            rain_hour_list = []
            bicycle_count = 0
            hours = []

            # Count the total vehicles
            for row in reader:
                outcomes["total_vehicles"] += 1

                # Count trucks
                if row["VehicleType"].lower() == "truck":
                    outcomes["total_trucks"] += 1

                # Count electric vehicles
                if row.get("elctricHybrid", "").lower() == "true":
                    outcomes["electric_vehicles"] += 1

                if row["VehicleType"].lower() in ["bicycle", "motorcycle", "scooter"]:
                    outcomes["two_wheeled_vehicles"] += 1

                
                if row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["travel_Direction_out"] == "N":
                    if row["VehicleType"].lower() == "buss":
                        outcomes["buses_north"] += 1

                if row["travel_Direction_in"] == row["travel_Direction_out"]:
                    outcomes["non_turning_vehicles"] += 1

                if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]):
                    outcomes["speeding_vehicles"] += 1

                if row["VehicleType"].lower() == "bicycle":
                    bicycle_count += 1

                 # Count vehicles on Elm Avenue/Rabbit Road and Hanley Highway/Westway
                if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                    outcomes["elm_vehicles"] += 1

                if row["JunctionName"] == "Hanley Highway/Westway":
                    outcomes["hanley_vehicles"] += 1

                 # Count scooters at Elm Avenue/Rabbit Road
                if row["VehicleType"].lower() == "scooter" and row["JunctionName"] == "Elm Avenue/Rabbit Road":
                    outcomes["scooter_percentage"] += 1

                # Track vehicles by hour on Hanley Highway/Westway
                if row["JunctionName"].lower() == "hanley highway/westway":
                    hour = row["timeOfDay"].split(":")[0]
                    hourly_count[hour] = hourly_count.get(hour, 0) + 1

                #calculate rain hours
                if row["Weather_Conditions"].strip() in ["Heavy Rain", "Light Rain"]:
                    hour = row["timeOfDay"].split(":")[0]
                    if hour not in rain_hour_list:
                        rain_hour_list.append(hour)
                 # Track all unique hours
                if "timeOfDay" in row:
                    hour = row["timeOfDay"].split(":")[0]
                    if hour not in hours:
                        hours.append(hour)

            # Calculate percentages and averages
            outcomes["scooter_percentage"] = round(
                (outcomes["scooter_percentage"] / outcomes["elm_vehicles"] * 100)
            ) if outcomes["elm_vehicles"] > 0 else 0

            outcomes["truck_percentage"] = round(
                (outcomes["total_trucks"] / outcomes["total_vehicles"] * 100)
            ) if outcomes["total_vehicles"] > 0 else 0

            total_hours = len(hours)
            if total_hours > 0:
                outcomes["average_bicycles_per_hour"] = round(bicycle_count / total_hours)

            if hourly_count:
                outcomes["peak_hour_vehicles"] = max(hourly_count.values())
                outcomes["peak_hour_times"] = [
                    f"Between {hour}:00 and {int(hour)+1}:00"
                    for hour, count in hourly_count.items()
                    if count == outcomes["peak_hour_vehicles"]
                ]
            
            outcomes["rain_hours"] = len(rain_hour_list)

    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return outcomes



def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    #print the outcomes 
    print("\nTraffic Analysis Report:")
    print(f"Total number of vehicles recorded: {outcomes['total_vehicles']}")
    print(f"Total number of trucks recorded: {outcomes['total_trucks']}")
    print(f"Total number of electric vehicles: {outcomes['electric_vehicles']}")
    print(f"Total number of two-wheeled vehicles: {outcomes['two_wheeled_vehicles']}")
    print(f"Buses leaving Elm Avenue/Rabbit Road heading North: {outcomes['buses_north']}")
    print(f"Vehicles through both junctions not turning left or right: {outcomes['non_turning_vehicles']}")
    print(f"Percentage of trucks: {outcomes['truck_percentage']}%")
    print(f"Average number of bicycles per hour: {outcomes['average_bicycles_per_hour']}")
    print(f"Vehicles recorded over the speed limit: {outcomes['speeding_vehicles']}")
    print(f"Vehicles through Elm Avenue/Rabbit Road junction: {outcomes['elm_vehicles']}")
    print(f"Vehicles through Hanley Highway/Westway junction: {outcomes['hanley_vehicles']}")
    print(f"Scooter percentage at Elm Avenue/Rabbit Road: {outcomes['scooter_percentage']}%")
    print(f"Highest number of vehicles in an hour on Hanley Highway/Westway: {outcomes['peak_hour_vehicles']}")
    print(f"Peak hours on Hanley Highway/Westway: {', '.join(outcomes['peak_hour_times'])}")
    print(f"Number of rainy hours: {outcomes['rain_hours']}")
    print()

    
# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    #open a text file and save results 
    with open(file_name, mode="a") as file:
        file.write("--- Outcomes ---\n")
        for key, value in outcomes.items():
            file.write(f"{key.replace('_', ' ').capitalize()}: {value}\n")
        file.write("\n")

#Task D
class HistogramApp:
    def __init__(self, traffic_data, date):
        self.traffic_data = []
        #load data from the file
        self.load_traffic_data(traffic_data)
        #get date for histogram
        self.date = date
        #create tkinter window
        self.root = tk.Tk()
        self.canvas = None
        #width,height and margin for canvas
        self.width = 1000
        self.height = 600
        self.margin = 100

    def load_traffic_data(self, file_name):
        #get data from the traffic file 
        try:
            with open(file_name, 'r') as file:
                reader = csv.DictReader(file)
                #store data in to dictionaries
                self.traffic_data = list(reader)
        except Exception as e:
            print(f"Error loading data: {e}")

    def setup_window(self):
        #Set tkinter window
        self.root.title("Histogram")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='#eae9d2')
        #add padding
        self.canvas.pack(padx=12.5, pady=12.5)

    def draw_histogram(self):
        #draw histogram
        elm_hourly = defaultdict(int)
        hanley_hourly = defaultdict(int)
        
        for record in self.traffic_data:
            try:
                hour = int(record["timeOfDay"].split(":")[0])
                if record["JunctionName"] == "Elm Avenue/Rabbit Road":
                    elm_hourly[hour] += 1
                elif record["JunctionName"] == "Hanley Highway/Westway":
                    hanley_hourly[hour] += 1
            except (ValueError, KeyError):
                continue
        #get maximum count 
        max_count = max(
            max(elm_hourly.values() or [0]),
            max(hanley_hourly.values() or [0])
        )
        #exit if data is empty
        if max_count == 0:
            print("No data to display")
            return

        #x and y axes scale
        x_scale = (self.width - 2 * self.margin) / 24
        y_scale = (self.height - 2 * self.margin) / (max_count + 5)
        #set width and gap each bars
        bar_width = x_scale * 0.35
        gap = x_scale * 0.05

        # Draw x and y axes
        self.canvas.create_line(
            self.margin, self.height - self.margin,
            self.width - self.margin, self.height - self.margin,
            width=2
        )
        
        self.canvas.create_line(
            self.margin, self.height - self.margin,
            self.width - self.margin, self.height - self.margin,
            width=2,
        )
        
        #add lable for y axis 
        for y in range (0, 80, 5):
            y_position = self.height - self.margin - y * y_scale
            self.canvas.create_text(
                self.margin - 10, y_position,
                text=str(y),
                font=('Times New Roman',8),
                fill='#000000',
                anchor='e'
            )
            
            self.canvas.create_line(
                self.margin - 5, y_position,
                self.margin, y_position,
                fill='#000000'
            )

        #hour labels and bars
        for hour in range(24):
            x = self.margin + hour * x_scale
            
            #Hour labels
            self.canvas.create_text(
                x + x_scale/2, self.height - self.margin/2,
                text=f"{hour:02d}",
                font=('Times New Roman', 8),
                fill="#000000"
            )

            #Elm Avenue bar
            elm_count = elm_hourly[hour]
            if elm_count > 0:
                bar_x = x + (x_scale - 2 * bar_width - gap) / 2
                height = elm_count * y_scale
                self.canvas.create_rectangle(
                    bar_x,
                    self.height - self.margin - height,
                    bar_x + bar_width,
                    self.height - self.margin,
                    fill='#204a5b',
                    outline='#FFFFFF'
                )
                self.canvas.create_text(
                    bar_x + bar_width/2,
                    self.height - self.margin - height - 5,
                    text=str(elm_count),
                    font=('Times New Roman', 8),
                    fill="#000000"
                )

            #Hanley Highway bar
            hanley_count = hanley_hourly[hour]
            if hanley_count > 0:
                bar_x = x + (x_scale - 2 * bar_width - gap) / 2 + bar_width + gap
                height = hanley_count * y_scale
                self.canvas.create_rectangle(
                    bar_x,
                    self.height - self.margin - height,
                    bar_x + bar_width,
                    self.height - self.margin,
                    fill='#74806a',
                    outline='#FFFFFF'
                )
                self.canvas.create_text(
                    bar_x + bar_width/2,
                    self.height - self.margin - height - 5,
                    text=str(hanley_count),
                    font=('Arial', 8),
                    fill="#000000"
                )

    def add_legend(self):
        #title
        raw_date = self.date.strip('traffic_data.csv')
        date_formate = f"{raw_date[:2]}/{raw_date[2:4]}/{raw_date[4:]}"
            
        title = f"Histogram of Vehicle Frequency per Hour ({date_formate})"
            
        self.canvas.create_text(
            #center the x
            self.width/2,  
            #position of the y
            20,            
            text=title,
            font=('Times New Roman', 12, 'bold'),
            anchor='n',     
            fill='#000000'
        )

        #Legend boxes
        y_pos_legend = self.margin
        
        #Elm Avenue legend
        self.canvas.create_rectangle(
            self.margin, y_pos_legend,
            self.margin + 15, y_pos_legend + 15,
            fill='#204a5b',
            outline='#FFFFFF'
        )
        self.canvas.create_text(
            self.margin + 20, y_pos_legend + 7,
            text="Elm Avenue/Rabbit Road",
            anchor='w',
            font=('Times New Roman', 10),
            fill="#000000"
        )

        #Hanley Highway legend
        x_pos_legend = self.margin + 200
        self.canvas.create_rectangle(
            x_pos_legend, y_pos_legend,
            x_pos_legend + 15, y_pos_legend + 15,
            fill='#74806a',
            outline='#FFFFFF'
        )
        self.canvas.create_text(
            x_pos_legend + 20, y_pos_legend + 7,
            text="Hanley Highway/Westway",
            anchor='w',
            font=('Times New Roman', 10),
            fill="#000000"
        )
        
        footer_text = "Hours:- 00:00 - 24:00"
        self.canvas.create_text(
            self.width / 2, self.height - self.margin / 4,
            text=footer_text,
            font=('Times New Roman',10,'bold'),
            fill="#000000"
            
        )

    def run(self):
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()

#Task E
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None
        self.outcomes = None
        self.file_name = None
        
    def load_csv_file(self, file_path):
        """
        Loads and processes a CSV file.
        Args:
            file_path (str): Path to the CSV file
        Returns:
            dict: Processed outcomes from the CSV file
        """
        #Loads and processes file name and process the CSV data
        try:
            self.file_name = file_path
            self.outcomes = process_csv_data(file_path)
            return self.outcomes
        #error handling
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return None
            
    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        #clear the current_data,outcome and file_name
        self.current_data = None
        self.outcomes = None
        self.file_name = None
        
    def process_files(self):
        """
        Main loop for processing multiple CSV files.
        """
        #Initial date input
        date, month, year = validate_date_input()
        file_name = f"traffic_data{date:02}{month:02}{year}.csv"
        print("**********************************************************")
        print(f"Date file selected is {file_name}")
        print("**********************************************************")
        
        while True:
            #Process the current file
            outcomes = self.load_csv_file(file_name)
            if outcomes:
                display_outcomes(outcomes)
                save_results_to_file(outcomes)
                
                #Create and display histogram
                histogram = HistogramApp(file_name, file_name)
                histogram.run()  

            
            #Ask the user if they want to process another file
            while True:
                    choice = input("\nDo you want to select a data file for a different date? (Y/N): ").strip()
                    if choice.upper() == 'Y':
                        #Clear previous data
                        self.clear_previous_data()
                        #get new date from the user
                        date, month, year = validate_date_input()
                        file_name = f"traffic_data{date:02}{month:02}{year}.csv"
                        print("**********************************************************")
                        print(f"Date file selected is {file_name}")
                        print("**********************************************************")
                        break
                    #exit the program if user inout n
                    elif choice.upper() == 'N':
                        print("\n------- PROGRAM TERMINATED -------")
                        return
                    else:
                        print("Invalid input! Please enter Y or N.")
#main program
if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()
    
  
