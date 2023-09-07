import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington). 
    while True:
        city = input("Please enter the city (chicago or new york city or washington): ").lower()
        # Check if user input correct city
        # If it is correct, break the loop
        if city in ['chicago', 'new york city', 'washington']:
            #print("Correct city!")
            break
        else:
            print("Invalid city. Please enter one of those (chicago, new york city, washington)!")
    
    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter the month that is in the first six months: ").lower()
        # Check if user input correct month
        # If it is correct, break the loop
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            #print("Correct month!")
            break
        else:
            print("Invalid month. Please enter the month that is in the first six month (all, january, february, ... , june)!")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter the day (all, monday, tuesday, ... sunday): ").lower()
        # Check if user input correct day
        # If it is correct, break the loop
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            #print("Correct day!")
            break
        else:
            print("Invalid day. Please enter the day of week that (all, monday, tuesday, ... sunday)!")

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
    # Load csv file
    df = pd.read_csv(CITY_DATA[city])

    # Convert the day time column to datetime
    df['start_time'] = pd.to_datetime(df['Start Time'])
    df['end_Time'] = pd.to_datetime(df['End Time'])

    # Extract month and day from Start Time
    df['month'] = df['start_time'].dt.month
    df['day'] = df['start_time'].dt.day_name()

    # Filter by month if applicable by using the index of the months list
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        # Create the new dataframe
        df = df[df['month'] == month]

    # Filter by day 
    if day != 'all':
        # Create the new dataframe
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', common_month)

    # Display the most common day of week
    common_day = df['day'].mode()[0]
    print('Most common day:', common_day)

    # Display the most common start hour
    df['hour'] = df['start_time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most common start hour:', common_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', most_common_end_station)

    # Display most frequent combination of start station and end station trip
    most_frequent_start_and_end_station = (df['Start Station'] + df['End Station']).mode()[0]
    print('Most frequent used start station and end station:', most_frequent_start_and_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:',total_travel_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:',mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print('counts of user types:',counts_of_user_types)

    # Display counts of gender
    if "Gender" in df.columns:
        counts_of_gender = df['Gender'].value_counts()
        print('Counts of genders:',counts_of_gender)
    else: print('Cannot find gender')

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_yob = df['Birth Year'].min()
        print('Earliest year of birth:',      earliest_yob)
        latest_yob = df['Birth Year'].max()
        print('Most recent year of birth:',   latest_yob)
        most_common_yob = df['Birth Year'].mode()[0]
        print('Most common year of birth:',   most_common_yob)

    else:print('Cannot find Birth Year"')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Restart feature
    end_loc = 5
    start_loc = 0
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        if view_data == 'yes':
            print(df.iloc[start_loc:end_loc])
            df.reset_index()
            start_loc += 5
            end_loc +=5
            view_data = input("Do you wish to continue?: ").lower()
        else:
            break    

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
    # Main function
	main()
