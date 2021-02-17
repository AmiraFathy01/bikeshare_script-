import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def cho(name, list):
    check = True
    while check:
        choise_name = input(f'Enter the {name} of your choice : ').lower()
        if choise_name in list:
            check = False
            break
        else:
            print(f'***************************\n '
                  f'oops -- you are enter the wrong {name} '
                  f'\n please enter the correct')
    return choise_name


def popular(popular_name, df):
    popular = df[popular_name].mode()[0]
    print(f'The most common {popular_name} is {popular}')
    return popular


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
    list_chioce_city = ['chicago', 'new york city', 'washington']
    print(' what is the city do u need to analysis it ?'
          '\n a:chicago '
          '\n b:new york city '
          '\n c:washington'
          ' \n you can choise the city by write the name of city ')
    city = cho('city', list_chioce_city)

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print(f'choice  the month  : {months} ')
    month = cho('month', months)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
    print(f'choice  the day  : {days} ')
    day = cho('day', days)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
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

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular('month', df)
    # display the most common day of week
    df['week'] = df['Start Time'].dt.day_name()
    popular('week', df)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular('hour', df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular('Start Station', df)

    # display most commonly used end station
    popular('End Station', df)

    # display most frequent combination of start station and end station trip
    popular_frequent = df[['Start Station', 'End Station']].mode()
    print(f'The most frequent combination of start station and end station trip is'
          f' {popular_frequent} ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print(f'total travel time is {total_travel}')
    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print(f'mean travel time is {mean_travel}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'counts of user types is {user_types}')
    try:
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print(f'counts of gender is {gender_count}')
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print(f'the earliest year of birth is {earliest_year}')
        most_recent_year = df['Birth Year'].max()
        print(f'the recent year of birth is {most_recent_year}')
        popular('Birth Year', df)
    except KeyError:
        print('*'*40)
        print('sorry there is no gender and birth day in this city try another city ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display(df):
    view_data = input(
        '\n Would you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    answer = ['yes', 'no']
    while view_data not in answer:
        print('you enter the wrong input please enter the correct answer')
        view_data = input(
            '\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input('Do you wish to continue?: ').lower()
    if view_data == 'no':
        print('Thanks for using my project ^_^ ')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
