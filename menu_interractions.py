from functions.show import * 
from functions.search import *
from functions.custom_input import *
from functions.delete import *
from functions.add import *
from functions.update import *
from config import COLUMNS_IN_SHOW, COLUMNS_IN_SEARCH

def menu_show(data):
    show(data)

    # Ask if the user wants to apply filters
    apply_filter = yesno_input('Do you want to filter the data? (y/n) ')

    while apply_filter == 'y':

        print("""Columns' indices
        1. Housing ID
        2. Housing Name
        3. Host Name
        4. Neighbourhood
        5. Price
        """)
        sort_by = int(int_input('Sort by which column? (1/2/3/4/5) ' ))
        sort_by -= 1
        while sort_by not in range(5):
            print('Your choice must be one of (1/2/3/4/5)')
            sort_by = int(int_input('Sort by which column? (1/2/3/4/5) ' ))
            sort_by -= 1
        
        ascending = True if yesno_input('sort ascending? (y/n) ') == 'y' else False

        show_filtered(data, COLUMNS_IN_SHOW[sort_by], ascending)

        print()
        apply_filter = yesno_input('Do you want to re-filter the data? (y/n) ')
    
    print('Alrighty!')
    

def menu_search(df):

    searching = True
    while searching:

        print('What do you want to search by?')
        print('0. Housing ID')
        print('1. Housing name')
        print('2. Housing host')
        print('3. Neighborhood')
        print('4. Price')
        print('5. Minimum Nights')
        
        search_by = int_input('Enter your choice (0/1/2/3/4/5) : ')
        while (search_by not in ['0', '1', '2', '3', '4', '5']):
            print('your choice must range from 0 to 5.')
            search_by = int_input('Enter your choice (0/1/2/3/4/5) : ')
        
        search_by = int(search_by)

        if (search_by not in [0, 4, 5]): # if query shouldn't be numbers
            query = input('Enter query : ')
        else:
            query = int_input('Enter query : ')
        results = search(df, query, COLUMNS_IN_SEARCH[search_by])

        results = results.head(25) if search_by != 0 else results

        rows_in_results = results.shape[0]
        if rows_in_results > 0:
            print('Here\'s what we found : ')
            print(results)
        else:
            print('housing not found.')
        
        print()
        searching = True if yesno_input('search again? (y/n) ') == 'y' else False
    
    print('Alrighty!')

def menu_add(df):

    adding = True
    while adding:

        name = input('enter housing name : ').strip()
        host_id = int_input('enter host id : ')

        host_name = input('enter host name : ').strip()
        neighbourhood_group = input('enter neighbourhood group : ').strip()
        neighbourhood = input('enter neighbourhood : ').strip()

        latitude = float_input('enter latitude : ')
        longitude = float_input('enter longitude : ')

        room_type = input('enter room type : ').strip()
        price = int_input('enter price : ').strip()
        minimum_nights = int_input('enter minimum nights : ').strip()
        availability = int_input('enter availability : ').strip()

        add_housing(df, name, host_id, host_name, neighbourhood_group,
                    neighbourhood, latitude, longitude, room_type, price, minimum_nights, availability)
        
        print()
        print(f'"{name}" added successfully!') 
        print()
        adding = True if yesno_input('add another housing data? (y/n) ') == 'y' else False
    
    print('Alrighty!')



def menu_update():

    updating = True
    while updating:

        data_id = input('enter housing ID : ')

        if (id_exists(data_id)):
            column_names = COLUMN_NAMES_BY_CATEGORY

            for column_category in column_names.keys():
                should_update = yesno_input(f'update {column_category}? (y/n) ')
                match should_update:
                    case 'y':
                        columns = column_names[column_category]

                        if (type(columns) == str):
                            column = columns
                            new_value = input(f'enter new value for {column} : ')

                            print(f'updating {column} to {new_value}...')

                            update_success = update_housing(data_id, column, new_value)

                            if update_success:
                                print(f'"{column}" updated')
                            else:
                                print(f'"{column}" was not updated')

                        else:
                            for column in columns:
                                new_value = input(f'enter new value for {column} : ')
                                
                                print(f'updating {column} to {new_value}...')

                                update_success = update_housing(data_id, column, new_value)
                                if update_success:
                                    print(f'"{column}" updated')
                                else:
                                    print(f'"{column}" was not updated')


                    case 'n':
                        print(f'bypassing {column_category}')

                    case _:
                        print('invalid choice, bypassing...')
        else:
            print('id not found.')
        
        print()
        updating = True if yesno_input('update another? (y/n)') == 'y' else False
    
    print('Alrighty!')


def menu_delete(df):

    deleting = True
    while deleting:

        housing_id = int(int_input('Enter housing ID : '))
        if (id_exists(housing_id)):
            to_be_deleted = search(df, str(housing_id), 'id')
            print('housing to be deleted:')
            print(to_be_deleted)
            
            proceed_deletion = True if yesno_input('Confirm deletion (y/n) ') == 'y' else False
            if proceed_deletion:
                delete_housing(df, housing_id)
                print('Deletion successful')
        else:
            print('id not found')

        print()
        deleting = True if yesno_input('delete another? (y/n)') == 'y' else False
    
    print('Alrighty!')