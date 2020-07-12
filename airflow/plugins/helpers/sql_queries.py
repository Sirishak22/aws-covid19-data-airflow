class SqlQueries:
    usa_covid19_insert = ("""
        insert into {}  (country,state,county,state_fips,county_fips,date,state_new_cases,state_new_deaths,county_new_cases,county_new_deaths)
        select 'USA' ,states_data.state,county_data.county,
            states_data.fips,county_data.fips,states_data.date,
            states_data.cases,states_data.deaths,
            county_data.cases,county_data.deaths
            from staging_data_usa_states_covid19 as states_data  
            JOIN staging_data_usa_county_covid19 as county_data
            on states_data.date = county_data.date
            and  states_data.state = county_data.state        
    """)
    usa_state_table_insert = ("""
        insert into {}   (state,state_fips)
        select distinct state,state_fips from usa_data_covid19
    """)
    usa_county_table_insert = ("""
        insert into {}   (county,county_fips)
        select distinct county,county_fips from usa_data_covid19
    """)
    date_table_insert = ("""
        insert into {}   (date ,  day , week , month , year , weekday )
        SELECT distinct date,  extract(day from date), extract(week from date), 
               extract(month from date), extract(year from date), extract(dayofweek from date)
               FROM usa_data_covid19
    """)