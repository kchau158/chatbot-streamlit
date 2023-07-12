# Chatbot-with-Streamlit-Snowpark-OpenAPI
Overview
========
A demo of chatbot that prompts using natural language to explore data interactively.

Because chatbot will run in local machine using [Streamlit](https://docs.streamlit.io/), user will need to complete the preparation below.

Prerequisites
========
- An API key for OpenAI or another Large Language Model
- A service account to Snowflake environment
- Ability to install software on local machine such as minconda, streamlit
- (Optional) VSCode or the IDE of your choice installed

Preparing local machine
===========================
Complete the following steps in your local machine

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html). This provides an isolated local environment for running Python anv various packages from Anaconda repository.
2. If you're using a machine with an Apple M1 chip, run the following command to use conda to create a Python 3.10 virtual environment, add the Snowflake conda channel, and install the numpy and pandas packages:

    `conda create --name py310_env --override-channels -c https://repo.anaconda.com/pkgs/snowflake python=3.10 numpy pandas`
3. Activate the environment created in those instructions by running conda activate py310_env and proceed to step 6 below.If you're not using a machine with an Apple M1 chip, continue to step 4.

4. Create a conda environment by running the following command:

    `conda create --name snowpark -c https://repo.anaconda.com/pkgs/snowflake python=3.10`

5. Activate the conda environment by running the following command:

    `conda activate snowpark`

6. Install Snowpark for Python, Streamlit, and OpenAI by running the following command:

    `conda install -c https://repo.anaconda.com/pkgs/snowflake snowflake-snowpark-python openai streamlit`

Set up workspace
===========================
1. Select a local directory to clone [Chatbot With Streamlit Snowpark OpenAPI](https://github.com/khanh-chau_wwg/chatbot-with-streamlit-snowpark-openapi.git) (ex. xkxc247\workspakce)
2. Clone using following command

    `gh repo clone khanh-chau_wwg/chatbot-with-streamlit-snowpark-openapi`

3. Open Terminal and navigate to chatbot-with-streamlit-snowpark-openapi directory

4. Use editor to create andup .streamlit\secrets.toml with the following info

    <code># .streamlit/secrets.toml </code>
    <code># provide your own api key is optional

    OPENAI_API_KEY = ""</code>

    <code># use the ATLAN_SVC only for testing. This user and following info has limited access to data in Snowflake Dev</code>
    <code>[connections.snowpark]

    user = "ATLAN_SVC"

    password = "Graing3r" 

    warehouse = "DMG_WH_M"

    role = "ATLAN_SVC"

    account = "wwgraingerdev.us-east-1"</code>

5. Run command

    `streamlit run validate_credentials.py`

If you encounter errors, please ensure .streamlit\secrets.toml has the correct information.

Create API Key from OpenAPI
===========================
Follow instructions to create OpenAPI API Key (https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/)

Run Chatbot using sample customer demographics data
===========================
1. Open Terminal and navigate to chatbot-with-streamlit-snowpark-openapi directory

2. Ensure .streamlit\secrets.toml uses the ATLAN_SVC user information for Snowflake

3. Ensure snowflake.chatbot.py has the following line uncommented

    >from customer_prompts import get_system_prompt

4. Run command

    `streamlit run snowflake_chatbot.py`

5. If all goes well, chatbot will introduces itself as Frosty

>Hello there! I'm Frosty the Snowman, and I'm here to help you with your queries about the DMG.ML_TEST.CUSTOMER_INFO_VW table.
>
> ...
>
>

Try the following prompts
>Can you provide the customer ID, gender, and income of customers from 
>
>California? Limit to top 10 highest income.
>
>Please add median income for both lower and upper bound to result?
>
>Let's limit result to Fremont city in California.
>
>Would you add adjacent cities of Fremont to result, also add city name
>
>Can you provide the demographics of customers by gender and income for customers from California?

Create your own data set
===========================
The sample code provide 3 different Snowflake data sets for chatbot to use: cybersyn_prompts, callcenter_prompts and customer_prompts. The default uses customer_prompts.py. By uncommenting the appropriate code, chatbot will use the 

>#from callcenter_prompts import get_system_prompt
>
>#from cybersyn_prompts import get_system_prompt
>
>from customer_prompts import get_system_prompt

To create your own data copy the customer_prompts.py and rename to something relevant to your data set.

Then make the following changes
- Set QUALIFIED_TABLE_NAME = "<database.schema.view>" to the Snowflake table or view that you want touse
- Set TABLE_DESCRIPTION = "" with hints and rules of your data. See examples in the customer_prompts.py
- Be sure to modify .streamlit/secrets.toml to use the Snowflake credential that has access to the data

Troubleshoot errors
===========================

- Be sure to connect to Global Connect as Snowflake environment uses IP whitelisting
- Ability to connect to OpenAPI requires valid API key. Also OpenAPI charges for usage so be sure there's enough credits to power LLM interactions.

