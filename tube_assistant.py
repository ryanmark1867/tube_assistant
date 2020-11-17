# tube assistant prompted to navigate the London Underground

# common imports
import json
import openai
import yaml
import os
import pickle
import pandas as pd
from gpt import GPT
from gpt import Example

def get_path():
    '''get the path for data files

    Returns:
        path: path for data files
    '''
    rawpath = os.getcwd()
    # data is in a directory called "data" that is in the current directory
    path = os.path.abspath(os.path.join(rawpath,'data'))
    return(path)


def get_config(config_file):
    ''' open config file with name config_file that contains parameters
    for this module and return Python object

    Args:
        config_file: filename containing config parameters

    Returns:
        config: Python dictionary with config parms from config file - dictionary

    '''
    current_path = os.getcwd()
    print("current directory is: " + current_path)

    path_to_yaml = os.path.join(current_path, config_file)
    print("path_to_yaml " + path_to_yaml)
    try:
        with open(path_to_yaml, 'r') as c_file:
            config = yaml.safe_load(c_file)
        return config
    except Exception as error:
        print('Error reading the config file '+error)
       
  
def get_input(input_prompt):
    ''' prompt user for input on the command line
    
    Returns:
        input_string: input entered by the user

    '''
    try:
        # prompt user for input and save text input by user
        input_string = input(input_prompt)
    except Exception as error:
        print('ERROR', error)
    else:
        return input_string
    
def get_gpt(gpt_key, gpt_engine,gpt_temperature,gpt_max_tokens,example_file):
    ''' define a gpt object
    
    Args:
        gpt_key: key under "Secret" here https://beta.openai.com/developer-quickstart
        gpt_engine: language model identifier (see https://beta.openai.com/api-ref for valid values)
        gpt_temperature: sampling temperature - Higher values means the model will take more risks
        gpt_max_tokens: How many tokens to complete to, up to a maximum of 512.
    
    Returns:
        gpt: gpt object (newly created gpt object if use_saved_gpt is False; gpt object from pickle file if use_saved_gpt is True)

    '''
    try:
        # check whether to use gpt from pickle file
        # create a new gpt object
        openai.api_key = gpt_key
        gpt = GPT(engine=gpt_engine, temperature=gpt_temperature, max_tokens=gpt_max_tokens)
        # add examples
        # load dataframe from example file
        path = get_path()
        example_df = pd.read_csv(os.path.join(path,example_file))
        for index, row in example_df.iterrows():
            # print(row['question'],row['answer'])
            gpt.add_example(Example(row['question'],row['answer']))
    except Exception as error:
        print('ERROR', error)
    else:
        return gpt



def main():
    ''' main function for module 
    - get gpt_key - note that you will need to provide your own key 
    - once you have access to the GPT-3 beta you can find the key under "Secret" here https://beta.openai.com/developer-quickstart
    - initialize GPT object
    - provide examples of London Underground trips
    - prompt user for the trip they want to take and output GPT-3's trip suggestions
    '''
    
    # ingest config file
    config = get_config('tube_assistant_config.yml')
    print("example_file is: ",config['files']['example_file'])
    print("test_file is: ",config['files']['test_file'])
    print(config['prompts']['welcome_prompt'])
    # initialize GPT-3 env
    gpt = get_gpt(config['general']['gpt_key'], 
            config['general']['gpt_engine'],
            config['general']['gpt_temperature'],
            config['general']['gpt_max_tokens'],
            config['files']['example_file'])
    # get input requests from command line or test file and get response from GPT-3    
    if config['general']['interactive']:
        # get input interactively from the command line
        input_request = get_input(config['prompts']['input_prompt'])
        while input_request != config['prompts']['stop_string']: 
            output = gpt.submit_request(input_request)
            print(output.choices[0].text)
            input_request = get_input(config['prompts']['input_prompt'])
    else:
        # read input from test file
        test_df = pd.read_csv(os.path.join(get_path(),config['files']['test_file']))
        for index, row in test_df.iterrows():
            print(row['question'])
            print("expect:",row['expected answer'])
            output = gpt.submit_request(row['question'])
            print(output.choices[0].text)
    


if __name__ == "__main__":
    main()