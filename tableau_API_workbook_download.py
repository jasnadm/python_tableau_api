from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils import querying


# Defining Tableau Server configuration details
config = {
    'tableau_prod': {  # You can name this whatever you want, ex. tableau_prod, tableau_dev etc.) and can add multiple such environments
        'server': 'https://<YOUR_SERVER_URL>.com',
        'api_version': 'API_VERSION',  # Such as 3.11
        # You could either use username and password or access tokens
        # Follow this link for how to generate access tokens:
        # https://medium.com/snake-charmer-python-and-analytics/tableau-server-on-tap-authenticating-with-a-personal-access-token-7f4affaece3e
        # Tokens available with Tableau Server 2019.4 (or newer)
        'personal_access_token_name': 'YOUR_TOKEN_NAME',
        'personal_access_token_secret': 'YOUR_TOKEN_SECRET',
        'site_name': '#',  # Default site name. TO be changed if not the default.
        'site_url': ''
    }
}

# Establish a connection with Tableau Server
conn = TableauServerConnection(config, env='tableau_prod')  # Calling one of the environemnts defined above in the 'config' variable
conn.sign_in()


# Output workbook names
workbooks_df = querying.get_workbooks_dataframe(conn)
print(workbooks_df[['name', 'id']])

# Storing the workbook IDs that are of interest
target_workbook_id = 'YOUR_WORKBOOK_ID'

# Extract workbook name for targeted workbook id
target_workbook_name = workbooks_df.loc[workbooks_df["id"] == 'YOUR_WORKBOOK_ID', 'name']
print(target_workbook_name.values)  # how to extract only the name without the punctuation

# Download report as powerpoint
response_pptx = conn.download_workbook_powerpoint(workbook_id=target_workbook_id)
with open(f'{target_workbook_name.values}.pptx', 'wb') as file:
     file.write(response_pptx.content)  # file name needs some cleaning


# Download report as pdf
pdf_params = {
    'type': 'type=Unspecified',
    'orientation': 'orientation=Landscape',
    'filter': ''  # the None value will be replaced by the values in the filter list one by one
}

# Write out to pdf
response_pdf = conn.download_workbook_pdf(workbook_id=target_workbook_id, parameter_dict=pdf_params)
with open(f'test_report_workbook_API.pdf', 'wb') as pdf_file:
         pdf_file.write(response_pdf.content)



conn.sign_out()