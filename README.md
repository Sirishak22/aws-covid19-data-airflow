# Data Modeling Covid19 data 
### Project Overview
###### Data Analysis is playing a very key role during Pandemic of Corona Virus. Various country/state and county data is being delivered by government/agencies  in files format and currently it is being very difficult for engineers to perform their analysis without data availabe in database. 
###### This project focuses on reading these files and store in a database so that it is easily available for enginners team to run their required analysis. Postgres database is used for storing the data. Fact and dimenstion tables are designed to optimize queries on covid data analysis. Database schema is created and ETL pipeline is built for this analysis. Also perform testing to  database and ETL pipeline in Airflow by running queries to run  analytics.
The source data is in S3 and needs to be processed in data warehouse in Amazon Redshift. The source data are JSON containing number of cases/ deaths by each state/county in USA.

### Airflow Tasks
###### We will create custom operators to perform tasks such as staging the data, filling the data warehouse and running checks. The tasks will need to be linked together to achieve a coherent and sensible data flow within the pipeline.

### State/county wise dataset
###### The first dataset is a subset of real data by each state/ county. Each file is in JSON format and contains metadata about a number of new cases/ new deaths for each day. The files are partitioned state wise file and county wise file.
###### The files in the dataset are partitioned by state data and county data. For example, here are filepaths to two files in this dataset
*s3://aws-deng-covid/enigma-nytimes-data-in-usa/us_states/part-00000-aa7e3dbc-cd43-4930-9596-fb0fd4167f5a-c000.json*
*s3://aws-deng-covid/enigma-nytimes-data-in-usa/us_county/part-00000-3b0459c2-faeb-4548-a5f2-6107221e8871-c000.json*
###### And below is an example of what the data in file, looks like.
![State data format ](/state-data.png)
![County data format ](/county-data.png)
### Schema for Song Play Analysis
###### Using the state and county datasets, you'll need to create a star schema optimized for queries on data analysis. This includes the following tables
###### Fact Table
* usa_data_covid19 - records in usa_data_covid19 data associated with state and county wise number for each day
    *country,state,county,state_fips,county_fips,date,state_new_cases,state_new_deaths,county_new_cases,county_new_deaths
###### Dimension Tables
* usa_state- state information
      * state,state_fips
* usa_county- county information
      * county,county_fips
* date- date of records in usa_data_covid19 broken down into specific units
      date ,  day , week , month , year , weekday 
### Project Template
<h2>Project Template</h2>
<ul>
<li>There are three major components of the project:</li>
</ul>
<ol>
<li>Dag template with all imports and task templates.</li>
<li>Operators folder with operator templates.</li>
<li>Helper class with SQL transformations.</li>
</ol>
<ul>
<li>Add <code>default parameters</code> to the Dag template as follows:
<ul>
<li>Dag does not have dependencies on past runs</li>
<li>On failure, tasks are retried 3 times</li>
<li>Retries happen every 5 minutes</li>
<li>Catchup is turned off</li>
<li>Do not email on retry</li>
</ul>
</li>
<li>The task dependencies generate the following graph view:

<a target="_blank" rel="noopener noreferrer" href="/narayana-k/aws-covid19-data-airflow/blob/master/covid-data-airflow-graph.png"><img src="/narayana-k/aws-covid19-data-airflow/blob/master/covid-data-airflow-graph.png" alt="Fig 1: Dag with correct task dependencies" style="max-width:100%;"></a></li>

<li>There are four operators:</li>
</ul>
<ol>
<li>Stage operator
<ul>
<li>Loads JSON files from S3 to Amazon Redshift</li>
<li>Creates and runs a <code>SQL COPY</code> statement based on the parameters provided</li>
<li>Parameters should specify where in S3 file resides and the target table</li>
<li>Parameters should distinguish between JSON and CSV files</li>
<li>Contain a templated field that allows it to load files from S3 </li>
</ul>
</li>
<li>Fact and Dimension Operators
<ul>
<li>Use SQL helper class to run data transformations</li>
<li>Take as input a SQL statement and target database to run query against</li>
<li>Define a target table that will contain results of the transformation</li>
<li>Dimension loads are often done with truncate-insert pattern where target table is emptied before the load</li>
<li>Fact tables are usually so massive that they should only allow append type functionality</li>
</ul>
</li>
<li>Data Quality Operator
<ul>
<li>Run checks on the data</li>
<li>Receives one or more SQL based test cases along with the expected results and executes the tests</li>
<li>Test result and expected results are checked and if there is no match, operator should raise an exception and the task should retry and fail eventually</li>
</ul>
</li>
</ol>
<h2>Build Instructions</h2>
<p>Run <code>/opt/airflow.start.sh</code> to start the Airflow server. Access the Airflow UI by clicking <code>Access Airflow</code> button. Note that Airflow can take up to 10 minutes to create the connection due to the size of the files in S3.</p>

<h2>Project execution:</h2>
<a target="_blank" rel="noopener noreferrer" href="/narayana-k/aws-covid19-data-airflow/blob/master/covid-data-airflow-execution.png"><img src="/narayana-k/aws-covid19-data-airflow/blob/master/covid-data-airflow-execution.png" alt="Fig 1: Dag with correct task dependencies" style="max-width:100%;"></a></li>
