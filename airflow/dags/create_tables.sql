drop table staging_data_usa_states_covid19;
drop table staging_data_usa_county_covid19;
drop table usa_data_covid19;
drop table date;
drop table usa_state;
drop table usa_county;


CREATE TABLE public.staging_data_usa_states_covid19 (
	date date,
	state varchar(100),
	fips  int4,
	cases int4,
	deaths int4
);

CREATE TABLE public.staging_data_usa_county_covid19 (
	date date,
	county varchar(100),
	state varchar(100),
	fips  int4,
	cases int4,
	deaths int4
);
CREATE TABLE public.usa_data_covid19 (
	country varchar(100) NOT NULL, 
	state varchar(100) NOT NULL,
	county varchar(100) NOT NULL ,
	state_fips  int4,
	county_fips  int4,
	date date,
	state_new_cases int4,
	state_new_deaths int4,
	county_new_cases int4,
	county_new_deaths int4
	
);

CREATE TABLE public.usa_state (
	state varchar(100) NOT NULL,
	state_fips int4,
	CONSTRAINT state_pkey PRIMARY KEY (state)
);

CREATE TABLE public.usa_county(
	county varchar(100) NOT NULL,
	county_fips int4,
	CONSTRAINT county_pkey PRIMARY KEY (county)
);
CREATE TABLE public.date   (
	date timestamp,
    day int4,
    week int4,
    month int4,
    year int4,
    weekday int4,
    CONSTRAINT date_pkey PRIMARY KEY (date)
);