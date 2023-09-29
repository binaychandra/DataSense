import langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai
from langchain.memory import ConversationBufferMemory
import pandas as pd
from langchain import memory
import sqlite3
import os
import json
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
import io
import logging
import requests
import urllib3
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.callbacks import LLMonitorCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate, HumanMessage, AIMessage
from langchain.agents import create_pandas_dataframe_agent

model_id = 'gpt-3.5-turbo'

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

def summary_extractor_from_df(df:pd.DataFrame)-> str:
    chatmodel = ChatOpenAI()
    template = "You are an AI assistant and your task is to summarize the workforce distribution based on gender delimited by triple backticks \
                and output should clearly indicate how much percentage one gender is higher than other one, and based on the findings make some comments on includsiveness \
                if this is good for company or not.. limit the output in 50 words```{json_genderdf}```"
    prompt_template = ChatPromptTemplate.from_template(template)

    user_message = prompt_template.format_messages(json_genderdf = df)
    response = chatmodel(user_message)
    # print(response.content)
    return response.content

def chat_response(text:str)->str:
    chatmodel = ChatOpenAI(max_tokens=50)
    response = chatmodel.predict(text)
    return response

def chat_with_df(query, table_name = None):
    if table_name is None:
        df = pd.read_csv(r"https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
    else:
        #get data
        con = sqlite3.connect("database.db")
        df = pd.read_sql_query(f"SELECT * from {table_name}", con)

    agent = create_pandas_dataframe_agent(                      
                ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
                df,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                verbose=True
            )
    try:
        res_query = agent.run(query)
    except Exception as e:
        print(str(e))
        res_query = "ERROR"

    return res_query

def gen_chartdata(df_out, label, chart_type):
    
    print("Inside gen_chartdata.....")
    print(f"df_out --> {df_out}")
    data_dict = {
                    "labels": None,
                    "datasets": [
                        {
                            "label": "Default Label",
                            "data": None,
                            "type" : chart_type,
                            "backgroundColor": ["rgba(250, 240, 230, 0.7)"],
                            "hoverBackgroundColor": ["rgba(250, 240, 230, 1)"],
                            "borderColor": ["rgba(250, 240, 230, 1)"]
                        }
                    ]
                }
    print(f"df_out.iloc[:,0].to_list() ---> {df_out.iloc[:,0].to_list()}")
    print(f"data_dict[\"datasets\"][0][\"label\"] --> {data_dict['datasets'][0]['label']}")
    print(f"label : {label}")
    print(f"data_dict['datasets'][0]['data'] --> {data_dict['datasets'][0]['data']}")
    print(f"df_out.iloc[:,1].to_list() --> {df_out.iloc[:,1].to_list()}")

    data_dict["labels"] = df_out.iloc[:,0].to_list()
    data_dict["datasets"][0]["label"] = label
    data_dict["datasets"][0]["data"] = df_out.iloc[:,1].to_list()
    if chart_type == 'doughnut':
        data_dict["datasets"][0]["backgroundColor"] = ["rgba(120, 214, 198, 0.7)", "rgba(255, 105, 105, 0.7)", "rgba(150, 194, 145, 0.7)", "rgba(250, 240, 230, 0.7)"]
        data_dict["datasets"][0]["hoverBackgroundColor"] = ["rgba(120, 214, 198, 1)", "rgba(255, 105, 105, 1)", "rgba(150, 194, 145, 1)", "rgba(250, 240, 230, 1)"]
        data_dict["datasets"][0]["borderColor"] = ["rgba(120, 214, 198, 1)", "rgba(255, 105, 105, 1)", "rgba(150, 194, 145, 1)", "rgba(250, 240, 230, 1)"]
    
    # Serializing json  
    json_object = json.dumps(data_dict, indent = 4) 
    
    return json_object

def generate_graphdata(query, table_name = None):
    if table_name is None:
        df = pd.read_csv(r"https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
    else:
        #get data from sqlite db
        con = sqlite3.connect("database.db")
        df = pd.read_sql_query(f"SELECT * from {table_name}", con)

    jsondf = df.head(5).to_json(orient='records')
    
    prompt_template = ChatPromptTemplate.from_messages(
        [
        SystemMessage(
            content=(
                "You are a data manager and you have to assign the task to a pandas coder \
            who will be working on the steps provided by you. Assuming the pandas coder has already loaded \
            the dataset in pandas dataframe, your task is to properly provide the steps with \
            proper column names so that pandas coder can easily understand the ask and code till the processing of dataset\
            which can be used for graph creation. include steps only to process the data \
            THE STEPS SHOULD NOT CONTAIN ANY GRAPH CREATION OR PLOTTING INSTRUCTIONS.. \
            always select columns only that are mentioned \
            not any extra columns. also think through if output contains two columns if not then create the steps to \
            only include two appropriate columns in output. Also do not include any steps to select top few records.. \
            the output should be all records from the steps execution.")
        ),
        HumanMessage(content=("\
                user_input = ```plot the distribution of males and females who survived```\
            use below dataset for reference delimited by <<<>>>\
            <<<[{\"PassengerId\":1,\"Survived\":0,\"Pclass\":3,\"Name\":\"Braund, Mr. Owen Harris\",\"Sex\":\"male\",\"Age\":22.0,\"SibSp\":1,\"Parch\":0,\"Ticket\":\"A\/5 21171\",\"Fare\":7.25,\"Cabin\":null,\"Embarked\":\"S\"},{\"PassengerId\":2,\"Survived\":1,\"Pclass\":1,\"Name\":\"Cumings, Mrs. John Bradley (Florence Briggs Thayer)\",\"Sex\":\"female\",\"Age\":38.0,\"SibSp\":1,\"Parch\":0,\"Ticket\":\"PC 17599\",\"Fare\":71.2833,\"Cabin\":\"C85\",\"Embarked\":\"C\"},{\"PassengerId\":3,\"Survived\":1,\"Pclass\":3,\"Name\":\"Heikkinen, Miss. Laina\",\"Sex\":\"female\",\"Age\":26.0,\"SibSp\":0,\"Parch\":0,\"Ticket\":\"STON\/O2. 3101282\",\"Fare\":7.925,\"Cabin\":null,\"Embarked\":\"S\"},{\"PassengerId\":4,\"Survived\":1,\"Pclass\":1,\"Name\":\"Futrelle, Mrs. Jacques Heath (Lily May Peel)\",\"Sex\":\"female\",\"Age\":35.0,\"SibSp\":1,\"Parch\":0,\"Ticket\":\"113803\",\"Fare\":53.1,\"Cabin\":\"C123\",\"Embarked\":\"S\"},{\"PassengerId\":5,\"Survived\":0,\"Pclass\":3,\"Name\":\"Allen, Mr. William Henry\",\"Sex\":\"male\",\"Age\":35.0,\"SibSp\":0,\"Parch\":0,\"Ticket\":\"373450\",\"Fare\":8.05,\"Cabin\":null,\"Embarked\":\"S\"}]>>>\
            {format_instructions}\
            from these inputs extract the following information\
            steps: the steps to be performed for the execution of task\
            label: suggest label to be displayed on the graph for the required ask in less than 3 words\
            chart_type: extract what type of chart user want to see.. if not specified then suggest which one \
            would be suitable for the task.. should be one of these ['bar', 'line', 'doughnut', 'scatter', 'text']\
            output text if graph cant be plotted or user required the answer in text format")),
        AIMessage(content=("{\n\t\"steps\": \"1. Filter the dataframe to include only the rows where \'Survived\' column is equal to 1.\\n\
        2. Group the filtered dataframe by \'Sex\' column.\\n\
        3. Count the number of occurrences of each unique value in the \'Sex\' column.\\n\
        4. Create a new dataframe with two columns: \'Sex\' and \'Count\', where \'Sex\' contains the unique values from the \'Sex\' column and \'Count\' contains the corresponding counts.\\n\
        5. Select top two records from the dataframe.\",\\n\
        6. Convert the dataset to Json and create the bar graph.\"t\
        \"label\": \"Distribution of Males and Females who Survived\",\\n\t\
        \"chart_type\": \"bar\"\\n}")),
        HumanMessage(content=("The output seems not correct. the provided steps include importing matplotlib and creating the bar diagram\
        which was clearly mentioned not to include. Also steps include selecting top two records where it was mentioned \
        not to select top few records for output. you should output all records unless asked otherwise. Also steps include \
        the conversion to json which should not have been included. the output should be only pandas dataframe..\
        can you correct these and provide the response.")),
        AIMessage(content=("{\n\t\"steps\": 1. Filter the dataframe to include only the rows where \'Survived\' column is equal to 1.\\n\
        2. Group the filtered dataframe by \'Sex\' column.\\n\
        3. Count the number of occurrences of each unique value in the \'Sex\' column.\\n\
        4. Create a new dataframe with two columns: \'Sex\' and \'Count\', where \'Sex\' contains the unique values from the \'Sex\' column and \'Count\' contains the corresponding counts.\\n\
        5. Return the new dataframe.\",\\n\t\
        \"label\": \"Distribution of Males and Females who Survived\",\\n\t\
        \"chart_type\": \"bar\"\\n}")),
        HumanMessage(content=("Now the output looks perfect. This was just the way I wanted. Thanks a lot..")),
        AIMessage(content=("Thanks for the feedback, I will double check these things next time..")),
        HumanMessage(content=("\
                user_input = ```draw the bar chart for distribution of pclass and for only sex=males```\
            use below dataset for reference delimited by <<<>>>\
            <<<[{\"PassengerId\":1,\"Survived\":0,\"Pclass\":3,\"Name\":\"Braund, Mr. Owen Harris\",\"Sex\":\"male\",\"Age\":22.0,\"SibSp\":1,\"Parch\":0,\"Ticket\":\"A\/5 21171\",\"Fare\":7.25,\"Cabin\":null,\"Embarked\":\"S\"},{\"PassengerId\":2,\"Survived\":1,\"Pclass\":1,\"Name\":\"Cumings, Mrs. John Bradley (Florence Briggs Thayer)\",\"Sex\":\"female\",\"Age\":38.0,\"SibSp\":1,\"Parch\":0,\"Ticket\":\"PC 17599\",\"Fare\":71.2833,\"Cabin\":\"C85\",\"Embarked\":\"C\"},{\"PassengerId\":3,\"Survived\":1,\"Pclass\":3,\"Name\":\"Heikkinen, Miss. Laina\",\"Sex\":\"female\",\"Age\":26.0,\"SibSp\":0,\"Parch\":0,\"Ticket\":\"STON\/O2. 3101282\",\"Fare\":7.925,\"Cabin\":null,\"Embarked\":\"S\"},{\"PassengerId\":4,\"Survived\":1,\"Pclass\":1,\"Name\":\"Futrelle, Mrs. Jacques Heath (Lily May Peel)\",\"Sex\":\"female\",\"Age\":35.0,\"SibSp\":1,\"Parch\":0,\"Ticket\":\"113803\",\"Fare\":53.1,\"Cabin\":\"C123\",\"Embarked\":\"S\"},{\"PassengerId\":5,\"Survived\":0,\"Pclass\":3,\"Name\":\"Allen, Mr. William Henry\",\"Sex\":\"male\",\"Age\":35.0,\"SibSp\":0,\"Parch\":0,\"Ticket\":\"373450\",\"Fare\":8.05,\"Cabin\":null,\"Embarked\":\"S\"}]>>>\
            {format_instructions}\
            from these inputs extract the following information\
            steps: the steps to be performed for the execution of task\
            label: suggest label to be displayed on the graph for the required ask in less than 3 words\
            chart_type: extract what type of chart user want to see.. if not specified then suggest which one \
            would be suitable for the task.. should be one of these ['bar', 'line', 'doughnut', 'scatter', 'text']\
            output text if graph cant be plotted or user required the answer in text format")),
        AIMessage(content=("{\"\n\t\"steps\": \"1. Filter the dataframe to include only rows where Sex is \'male\'\\n\
        2. Group the data by Pclass and count the number of occurrences\\n\
        3. Create a new dataframe with the Pclass and count columns\\n\
        4. Sort the dataframe by Pclass\\n\
        5. Output the resulting dataframe\",\n\t\
        \"label\": \"Distribution of Pclass for males\",\n\t\
        \"chart_type\": \"bar\"\n}")),
        HumanMessage(content=("The output looks perfect. This is exactly the response I was looking for.")),
        AIMessage(content=("Thanks! Now I am more confident about the requirement. ")),
        HumanMessagePromptTemplate.from_template(
            "user_input = ```{user_input}```\
            use sample dataset below for reference delimited by <<<>>>\
            <<<{reference_data}>>>\
            {format_instructions}\
            from these inputs extract the following information\
            steps: the steps to be performed for the execution of task. stritcly remember to not include any graph or plotting related instructions..\
            label: suggest label to be displayed on the graph for the required ask in less than 3 words\
            chart_type: extract what type of chart user want to see.. if not specified then suggest which one \
            would be suitable for the task.. should be one of these ['bar', 'line', 'doughnut', 'scatter', 'text']\
            output text if graph cant be plotted or user required the answer in text format"
        ),
        ]
    )

    step_schema = ResponseSchema(name="steps",
                             description="steps to be performed for the execution of task. stritcly remember to not include any graph or plotting related instructions..")
    label_schema = ResponseSchema(name="label",
                                description="suggest label to be displayed on the graph for the required ask")
    chart_type_schema = ResponseSchema(name="chart_type",
                                        description="Suggest the type of chart to be created.. if user specified\
                                        any chart type, select that.. otherwise suggest what would be suitable for the user ask\
                                        From the user input.. should be one of these ['bar', 'line', 'doughnut', 'scatter', 'text']\
                                        output text if graph cant be plotted or user required the answer in text format")

    response_schemas = [step_schema, label_schema, chart_type_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    
    customer_messages = prompt_template.format_messages(user_input=query, 
                                                    reference_data=jsondf, 
                                                    format_instructions=format_instructions)

    llm = ChatOpenAI(model = 'gpt-3.5-turbo-0613', temperature = 0)
    response = llm(customer_messages)
    json_pandassteps_charttype = output_parser.parse(response.content)
    print("pandas steps and charttype" , json_pandassteps_charttype)
    agent = create_pandas_dataframe_agent(                 
                ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
                df, 
                agent_type=AgentType.OPENAI_FUNCTIONS,
                verbose=True,
                return_intermediate_steps=True
            )
    try:
        if json_pandassteps_charttype['chart_type'] != "text":
            agent_response = agent({
                'input': f"Remove any steps related to charts or plotting from the steps mentioned in triple backticks\
                        and Execute the Python script combining all the steps after remoing the chart related steps\
                        Please don't use any print statements. Output should be a pandas dataframe only \
                            steps to be performed : {json_pandassteps_charttype['steps']}"
            })
        else:
            chart_type, chart_label, chart_json_data = "text", None, None
            print("The text block has been activated")
            text_to_display = chat_with_df(query, table_name)
            success = True
    except langchain.schema.output_parser.OutputParserException as e:
        success = False
        chart_type, chart_label, chart_json_data = "text", None, None
        text_to_display = "OutputParserException : " + str(e)[:25] + "...."
        print(f"OutputParserException Occurred --> {str(e)}")
    except Exception as e:
        success = False
        chart_type, chart_label, chart_json_data = "text", None, None
        text_to_display = "AgentException : " + str(e)[:25] + "...."
        print(f"Exception Occurred --> {str(e)}")
    else:
        graph_data_df = agent_response['intermediate_steps'][-1][-1]
        print("intermediate steps " , agent_response['intermediate_steps'])
        if isinstance(graph_data_df, pd.DataFrame):
            final_data = dataframe_sanitizer(graph_data_df)
            chart_label = json_pandassteps_charttype['label']
            chart_type = json_pandassteps_charttype['chart_type']
            chart_json_data = gen_chartdata(final_data, chart_label, chart_type)
            success = True
            text_to_display = None
        else:
            chart_type, chart_label, chart_json_data = "text", None, None
            text_to_display = graph_data_df
            success = True
    finally:
        final_response = dict(success=success, 
                              chart_type=chart_type, 
                              chart_label=chart_label,
                              chart_json_data=chart_json_data,
                              text_to_display=text_to_display)
        return final_response

def dataframe_sanitizer(raw_dataframe):
    # Check if reset index is required or not
    new_df = raw_dataframe.copy()
    if new_df.index.name:
        new_df = new_df.reset_index()
    
    print("new_df --> ", new_df)
    # Rearrange the columns as object and int
    object_columns = [col for col, dtype in new_df.dtypes.items() if dtype not in ['int8','int16','int32','int64', 'float64', 'float32']]
    int_columns = [col for col, dtype in new_df.dtypes.items() if dtype in ['int8','int16','int32','int64', 'float64', 'float32']]
    reordered_columns = object_columns + int_columns
    print(f"object Columns , reordered columns : {object_columns}, {reordered_columns}")
    new_df_reordered = new_df[reordered_columns]
    print(f"New ordered columns : {new_df_reordered}")

    #Check if first column is object and second column is int
    try:
        if (new_df_reordered.shape[1] != 2) & (new_df_reordered.dtypes[1] not in ('int8','int16','int32','int64', 'float64', 'float32')):
            print("========Exception in shape and type==========")
            return_string = f"The output dataframe has columns count as {new_df_reordered.shape[1]}..\
                    and the datatypes of columns present as {new_df_reordered.dtypes}..\
                    so cant proceed further with plotting the same.."
            print(return_string)
            raise Exception(return_string)
        
        else: 
            new_df_reordered[new_df_reordered.columns[0]] = new_df_reordered[new_df_reordered.columns[0]].astype(str)
            return new_df_reordered
    except Exception as e:
        print("Exception occurred" , str(e))