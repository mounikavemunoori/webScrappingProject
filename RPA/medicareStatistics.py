import json
import pdb
import rpa
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

class HTMLParser:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def find_element_by_tag(self, tag_name):
        return self.soup.find(tag_name)

    def find_elements_by_tag(self, tag_name):
        return self.soup.find_all(tag_name)

# creating the CommonMethodsPandas for storing common methods
class CommonMethodsPandas(object):
    def __init__(self):
        # In future we can add the variables here
        pass

    def add_commas_based_on_rowspan(self, df):
        def add_commas(row):
            for col in row.index:
                rowspan = df.loc[:, col].attrs.get('rowspan', 1)
                if rowspan > 1:
                    row[col] = ', '.join(str(x) for x in row[col])
            return row

        df = df.apply(add_commas, axis=1)
        # Drop duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]
        return df

    def read_html(self, content):
        # Extract the first DataFrame object (assuming the table of interest is the first one)
        df_list = pd.read_html(str(content))
        df = df_list[0]
        return df

    def save_to_csv(self, data_frame):
        # creating the file name based on time stamp to avoid the duplicate
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f'medicareStatistics_{timestamp}.csv'
        # Save DataFrame to CSV
        data_frame.to_csv(file_name, index=False)
        print(f"HTML data has been converted and saved to {file_name}.")

# This class used to extract the table data from website
class MedicareStatistics(object):
    def __init__(self):
        self.url = 'http://medicarestatistics.humanservices.gov.au/statistics/mbs_group.jsp'
        # locators , these are used to find the web element on web page
        # Select your report options
        self.medicareReportsOnCategoryDropDown = '#GROUP'
        self.financialYearStartDate = '#START_DT'
        self.financialYearEndDate = '#END_DT'
        self.createReportButton = '(//input[@value="Create Report"])[1]'

    def initialize_browser(self):
        rpa.init()
        rpa.url(self.read_json_file('url'))
        # ensure results are fully loaded
        rpa.wait()
        print(f'Successfully launched the url {self.url}')

    def select_visible_text(self, element, text):
        # Select the desired option
        rpa.select(element, text)
        print(f'Selected the drop down value as {text}')

    def select_report_on_medicare_category_dropdown_option(self, medicare_category_drop_down_value):
        self.select_visible_text(self.medicareReportsOnCategoryDropDown, medicare_category_drop_down_value)

    def select_start_financial_year(self, financial_year_start_date):
        self.select_visible_text(self.financialYearStartDate, financial_year_start_date)
        print("Financial Year Start Date:", financial_year_start_date)

    def select_end_financial_year(self, financial_year_end_date):
        self.select_visible_text(self.financialYearEndDate, financial_year_end_date)
        print("Financial Year End Date:", financial_year_end_date)

    def click_on_create_report_button(self):
        rpa.click(self.createReportButton)
        print(f'Click on create report button successfully')

    def fetch_html_content_current_browser(self):
        current_url = rpa.url()
        response = requests.get(current_url)
        assert response.status_code == 200, 'Unable to access the current url'
        html_content = response.text
        return html_content

    def formatted_date_year_month(self, date_string):
        formatted_date = date_string.strftime('%Y%m')
        return formatted_date

    def read_json_file(self, key):
        current_directory = os.getcwd()
        json_file_path = os.path.join(current_directory, 'RPA', 'testData.json')
        with open(json_file_path) as json_file:
            data = json.load(json_file)
        return data[key]

    def get_current_financial_year_dates(self):
        today = datetime.date.today()
        current_year = today.year
        # Assuming the financial year starts on July 1st
        fiscal_start_date = datetime.date(current_year-1, 7, 1)
        # Assuming the financial year ends on June 30th of the next year
        fiscal_end_date = datetime.date(current_year, 6, 30)
        return fiscal_start_date, fiscal_end_date

    def closing_browser(self):
        rpa.close()

def main():
    # Main functionality of your program
    medicareObj = MedicareStatistics()
    # initialize the browser using rpa
    medicareObj.initialize_browser()
    # selecting the drop down value from medicare category drop down
    medicareObj.select_report_on_medicare_category_dropdown_option(medicareObj.read_json_file("medicare_category_drop_down_value"))
    # fetching the  current financial year start  and end date
    financial_year_start_date, financial_year_end_date = medicareObj.get_current_financial_year_dates()
    financial_year_start_date = medicareObj.formatted_date_year_month(financial_year_start_date)
    financial_year_end_date = medicareObj.formatted_date_year_month(financial_year_end_date)

    # selecting the start financial year
    medicareObj.select_start_financial_year(financial_year_start_date)
    # selecting the end financial year
    medicareObj.select_end_financial_year(financial_year_end_date)
    # clicking on create report
    medicareObj.click_on_create_report_button()
    # fetching the tables data
    html_content = medicareObj.fetch_html_content_current_browser()

    # creating the object for html parser
    htmlparserObj = HTMLParser(html_content)
    table_data = htmlparserObj.find_element_by_tag('table')

    # creating the object for common methods for pandas
    commonMethodsObj = CommonMethodsPandas()
    # accessing the methods of pandas
    data_frame = commonMethodsObj.read_html(table_data)
    data_frame = commonMethodsObj.add_commas_based_on_rowspan(data_frame)
    commonMethodsObj.save_to_csv(data_frame)

    # closing thr browser
    medicareObj.closing_browser()


if __name__ == '__main__':
    main()
