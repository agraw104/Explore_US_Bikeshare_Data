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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()
        if city not in CITY_DATA.keys():
            print('Please select an appropriate choice!')
        else:
            break
    time.sleep(1)

    print('Looks like you want to hear about ' + city.title() + '! If this is not true, restart the program now! \n \n')
    time.sleep(1)
    # get user input for month (all, january, february, ... , june)
    while True:
        filter = input('Would you like to filter the data by month, day, both or not at all? Type \"none\" for no time filter.\n')
        if filter == 'month':
            while True:
                day = 'all'
                month = input('Which month? January, February, March, April, May, or June?\n').lower()
                if month not in ('january','february','march', 'april', 'may', 'june'):
                    print('Oops! Please enter a valid month!')
                else:
                    break
            break

        elif filter == 'day':
            while True:
                month = 'all'
                day = input('Which day? (e.g., Sunday, Monday, Tuesday..?)\n').lower()
                if day not in ('sunday', 'monday', 'tuesday','wednesday','thursday','friday','saturday'):
                    print('Oops! Please enter a valid day!')
                else:
                    break
            break

        elif filter == 'both':
            while True:
                month = input('Which month? January, February, March, April, May, or June?\n').lower()
                if month not in ('january','february','march', 'april', 'may', 'june'):
                    print('Oops! Please enter a valid month!')
                else:
                    break
            while True:
                day = input('Which day? (e.g., Sunday, Monday, Tuesday..?)\n').lower()
                if day not in ('sunday', 'monday', 'tuesday','wednesday','thursday','friday','saturday'):
                    print('Oops! Please enter a valid day!')
                else:
                    break
            break

        elif filter == 'none':
            month = 'all'
            day = 'all'
            break

        else:
            print('Please enter a valid response!\n')


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    df['month_name'] = df['Start Time'].dt.month_name()
    most_common_month = df['month_name'].mode()[0]
    print('Most Common Month :', most_common_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Common Day of Week :', most_common_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour :', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_ss = df['Start Station'].mode()[0]
    print('The most commonly used start station is :', most_common_ss)

    # display most commonly used end station
    most_common_es = df['End Station'].mode()[0]
    print('The most commonly used end station is :', most_common_es)

    # display most frequent combination of start station and end station trip
    most_frequent_comb = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most frequent combination of start station and end station trip is :\n', most_frequent_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time is :',total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('The count for different user types are :\n', count_user_types)

    try:
        # Display counts of gender
        count_gender_types = df['Gender'].value_counts()
        print('The count for different gender types are :\n', count_gender_types)

        # Display earliest, most recent, and most common year of birth
        earliest_birthyear = df['Birth Year'].min()
        print('The earliest Birth Year is :', earliest_birthyear)

        recent_birthyear = df['Birth Year'].max()
        print('The most recent Birth Year is :', recent_birthyear)

        most_common_birthyear = df['Birth Year'].mode()[0]
        print('The most common Birth Year is :', most_common_birthyear)

    except KeyError:
        print('This city does not contain information w.r.t Gender and Birth Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    print('The first 5 rows of raw data are', df.head())
    n = 5
    while True:
        raw_data = input('Do you want to see the next 5 rows of raw data? Yes or No?').lower()
        if raw_data == 'yes':
            print(df.iloc[[n,n+1,n+2,n+3,n+4]])
            n = n+5
        elif raw_data not in ('yes','no'):
            print('Oops! Please enter a valid input!')
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
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
