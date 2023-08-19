import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv', 'washington': 'washington.csv' }

MONTH_DATA = [ 'all', 'january','february', 'march','april','may','june']

DAY_DATA = ['all','monday','tuesday','wednesday', 'thursday', 'friday','saturday', 'sunday']

#Function for filtering requirements of the user
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Initializing empty variables to store choices from user. Code is used three times for city, month, and day       respectively. 
    city_name = ' '
    # Loop for correct input is selected. Otherwise repeat
    
    while city_name.lower() not in CITY_DATA:
        #Converts user input into lower
        city_name = input("\nHello! Please input the city you would like to analyze from the available options: (Chicago, New York City, Washington) \n")
        #For when the user inputs a city not available as a option
        if city_name.lower() in CITY_DATA:
            city= CITY_DATA[city_name.lower()]
        else:
            print("\n Unfortunately the input is not in our data, please try again")
    #Same as the above but for month    
    month_name = ' '
    while month_name.lower() not in MONTH_DATA:
        # Coverts user input into lower
        month_name = input("Hello! Please input the month you would like to analyze from the available options (all, January, February, March, April, May, June)")
        #For when the user inputs a option not available
        if month_name.lower() in MONTH_DATA:
            month= month_name.lower()
        else:
            print("\n Unfortunately the input is not in our data, please try again")
    #Same as the above but for day    
    day_name = ' '
    while day_name.lower() not in DAY_DATA:
        # Coverts user input into lower
        day_name = input("Hello! Please input the day you would like to analyze from the available options (all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)")
        #For when the user inputs a option not available
        if day_name.lower() in DAY_DATA:
            day= day_name.lower()
        else:
            print("\n Unfortunately the input is not in our data, please try again")
        
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Load city data
    df = pd.read_csv(city)
    
    #Start Time column converts to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #Month and Day are extracted from Start Time into new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
                    
    #filtering by month
    if month != 'all':
        #use the index of months list for getting
        month = MONTH_DATA.index(month)
        
        #filter by month
        df = df.loc[df['month'] == month] 
        
    #filtering by day
    if day != 'all':
        
        #filter by month
        df = df.loc[df['day_of_week'] == day.title()]
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The most popular month is: " + MONTH_DATA[common_month].title())

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most popular day of the week is: " + common_day_of_week)

    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print("The most common start hour is: " + str(common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0] 
    print(f"The most commonly used start station: {common_start_station}")

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0] 
    print(f"\nThe most commonly used end station: {common_end_station}")

    # display most frequent combination of start station and end station trip
    frequent_combination = (df['Start Station'] + "||" + df['End Station']).mode()[0]
    print("The most frequent combination of start/end stations is: " + str(frequent_combination.split("||")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()   
    # formats total travel time into minutes and seconds
    minute, second = divmod(total_travel_time, 60)
    #  formats total travel time into hours and minutes
    hour, minute = divmod(minute, 60)
    print(f"The total travel time is: {hour} hours, {minute} minutes and {second} seconds.")

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())
    #formats mean travel time into minutes and seconds
    minutes, seconds = divmod(mean_travel_time, 60)
    #formats m_t_t into hours and minutes
    hours, minutes = divmod(minutes, 60)
    print(f"The average duration is {hours} hours, {minutes} minutes and {seconds} seconds.")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types by using value_counts()
    user_type = df['User Type'].value_counts()
    print(f"The type of users are given below: \n\n {user_type}")

    #Display counts of gender by using value_counts(). The try and except clause is for when the user selects a city without gender data. 
    try:
        gender = df['Gender'].value_counts()
        print(f"The types of users by gender are given below:\n\n {gender}")
    except:
        print("No Gender data available")
          
    # Display earliest, most recent, and most common year of birth. The try and except clause is for when the user selects a city without birth year column
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest birht year: {earliest}")
        print(f"\nThe most recent birth year: {recent}")
        print(f"\nThe most common birth year: {common_year}")
    except:
        print("No birth year data available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    # This is for displaying raw data on user request. Gives the user the option to view the next five rows.
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\n Would you like to view the next five rows of data? Please enter yes or no')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df[next:next+5])
 
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

          
