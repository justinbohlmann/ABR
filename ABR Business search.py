from flask import Flask, render_template, request, send_file, jsonify
import requests
import xml.etree.ElementTree as ET
import csv
import os
import tempfile
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# ABR API configuration
ABR_API_URL = "https://abr.business.gov.au/json/AbnDetails.aspx"
ABR_SEARCH_URL = "https://abr.business.gov.au/json/AbnDetails.aspx"

# Get authentication GUID from environment variable
ABR_AUTH_GUID = os.getenv('ABR_AUTH_GUID', '60ff3b3e-c2f4-4e9d-a086-78c396e7013d')

def search_abr_businesses(search_term, state_filter=None, postcode_filter=None, max_results=100000):
    """
    Search for businesses using the ABR API
    """
    try:
        # ABR API endpoint and parameters based on the working URL
        abr_url = "https://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx/ABRSearchByNameAdvancedSimpleProtocol2017"
        
        # Set postcode filter
        postcode_param = postcode_filter if postcode_filter else ''
        
        # Set state filters - if a specific state is selected, only include that state
        if state_filter:
            # Only include the selected state
            state_params = {
                'NSW': 'N', 'SA': 'N', 'ACT': 'N', 'VIC': 'N', 
                'WA': 'N', 'NT': 'N', 'QLD': 'N', 'TAS': 'N'
            }
            state_params[state_filter] = 'Y'
        else:
            # Include all states
            state_params = {
                'NSW': 'Y', 'SA': 'Y', 'ACT': 'Y', 'VIC': 'Y', 
                'WA': 'Y', 'NT': 'Y', 'QLD': 'Y', 'TAS': 'Y'
            }
        
        params = {
            'name': search_term,
            'postcode': postcode_param,
            'legalName': 'Y',
            'tradingName': 'Y',
            'businessName': 'Y',
            'activeABNsOnly': 'Y',
            'authenticationGuid': ABR_AUTH_GUID,
            'searchWidth': 'Typical',
            'minimumScore': '0',
            'maxSearchResults': str(max_results)
        }
        
        # Add state parameters
        params.update(state_params)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/xml, text/xml, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        print(f"Making request to ABR API for search term: {search_term}")
        response = requests.get(abr_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        print(f"ABR API Response Status: {response.status_code}")
        print(f"ABR API Response Length: {len(response.text)} characters")
        
        return response.text
            
    except requests.RequestException as e:
        print(f"Error making request to ABR API: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in ABR API call: {e}")
        return None

def create_sample_xml_response(search_term, business_data):
    """
    Create a sample XML response structure similar to the original file
    """
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+10:00")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    xml_template = f'''<?xml version="1.0" encoding="utf-8"?>
<ABRPayloadSearchResults xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://abr.business.gov.au/ABRXMLSearch/">
  <request>
    <nameSearchRequestAdvanced2017>
      <authenticationGUID>{str(uuid.uuid4())}</authenticationGUID>
      <name>{search_term}</name>
      <filters>
        <nameType>
          <tradingName>Y</tradingName>
          <legalName>Y</legalName>
          <businessName>Y</businessName>
        </nameType>
        <postcode />
        <stateCode>
          <QLD>Y</QLD>
          <NT>Y</NT>
          <SA>Y</SA>
          <WA>Y</WA>
          <VIC>Y</VIC>
          <ACT>Y</ACT>
          <TAS>Y</TAS>
          <NSW>Y</NSW>
        </stateCode>
        <activeABNsOnly>Y</activeABNsOnly>
      </filters>
      <searchWidth>Typical</searchWidth>
      <minimumScore>0</minimumScore>
      <maxSearchResults>100000</maxSearchResults>
    </nameSearchRequestAdvanced2017>
  </request>
  <response>
    <usageStatement>The Registrar of the ABR monitors the quality of the information available on this website and updates the information regularly. However, neither the Registrar of the ABR nor the Commonwealth guarantee that the information available through this service (including search results) is accurate, up to date, complete or accept any liability arising from the use of or reliance upon this site.</usageStatement>
    <dateRegisterLastUpdated>{current_date}</dateRegisterLastUpdated>
    <dateTimeRetrieved>{current_time}</dateTimeRetrieved>
    <searchResultsList>
      <numberOfRecords>{len(business_data)}</numberOfRecords>
      <exceedsMaximum>N</exceedsMaximum>
'''
    
    # Add business records
    for business in business_data:
        xml_template += f'''      <searchResultsRecord>
        <ABN>
          <identifierValue>{business.get('abn', '')}</identifierValue>
          <identifierStatus>{business.get('status', 'Active')}</identifierStatus>
        </ABN>
        <businessName>
          <organisationName>{business.get('name', '')}</organisationName>
          <score>{business.get('score', '98')}</score>
          <isCurrentIndicator>Y</isCurrentIndicator>
        </businessName>
        <mainBusinessPhysicalAddress>
          <stateCode>{business.get('state', '')}</stateCode>
          <postcode>{business.get('postcode', '')}</postcode>
          <isCurrentIndicator>Y</isCurrentIndicator>
        </mainBusinessPhysicalAddress>
      </searchResultsRecord>
'''
    
    xml_template += '''    </searchResultsList>
  </response>
</ABRPayloadSearchResults>'''
    
    return xml_template

def convert_xml_to_csv(xml_content, csv_file_path):
    """
    Convert XML content to CSV format
    """
    try:
        # Parse the XML content
        root = ET.fromstring(xml_content)
        
        # Define the namespace
        namespace = {'abr': 'http://abr.business.gov.au/ABRXMLSearch/'}
        
        # Find all search results records
        search_results = root.findall('.//abr:searchResultsRecord', namespace)
        
        print(f"Found {len(search_results)} search result records")
        
        # Define CSV headers
        headers = [
            'ABN',
            'ABN_Status',
            'Business_Name',
            'Name_Type',
            'Score',
            'Is_Current',
            'State_Code',
            'Postcode'
        ]
        
        # Open CSV file for writing
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            # Process each search result record
            for record in search_results:
                # Extract ABN information
                abn_elem = record.find('abr:ABN', namespace)
                abn_value = abn_elem.find('abr:identifierValue', namespace).text if abn_elem is not None else ''
                abn_status = abn_elem.find('abr:identifierStatus', namespace).text if abn_elem is not None else ''
                
                # Extract business name information
                business_name = ''
                name_type = ''
                score = ''
                is_current = ''
                
                # Check for different name types
                name_elements = [
                    ('businessName', 'Business Name'),
                    ('mainName', 'Main Name'),
                    ('mainTradingName', 'Trading Name'),
                    ('otherTradingName', 'Other Trading Name')
                ]
                
                for elem_name, type_label in name_elements:
                    name_elem = record.find(f'abr:{elem_name}', namespace)
                    if name_elem is not None:
                        org_name_elem = name_elem.find('abr:organisationName', namespace)
                        if org_name_elem is not None:
                            business_name = org_name_elem.text
                            name_type = type_label
                            
                            # Extract score and current indicator
                            score_elem = name_elem.find('abr:score', namespace)
                            score = score_elem.text if score_elem is not None else ''
                            
                            current_elem = name_elem.find('abr:isCurrentIndicator', namespace)
                            is_current = current_elem.text if current_elem is not None else ''
                            break
                
                # Extract address information
                address_elem = record.find('abr:mainBusinessPhysicalAddress', namespace)
                state_code = ''
                postcode = ''
                
                if address_elem is not None:
                    state_elem = address_elem.find('abr:stateCode', namespace)
                    state_code = state_elem.text if state_elem is not None else ''
                    
                    postcode_elem = address_elem.find('abr:postcode', namespace)
                    postcode = postcode_elem.text if postcode_elem is not None else ''
                
                # Write row to CSV
                writer.writerow([
                    abn_value,
                    abn_status,
                    business_name,
                    name_type,
                    score,
                    is_current,
                    state_code,
                    postcode
                ])
        
        return len(search_results)
        
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        print(f"XML content preview: {xml_content[:500]}...")
        return 0
    except Exception as e:
        print(f"Error converting XML to CSV: {e}")
        print(f"XML content preview: {xml_content[:500]}...")
        return 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term', '').strip()
    state_filter = request.form.get('state_filter', '').strip()
    postcode_filter = request.form.get('postcode_filter', '').strip()
    
    if not search_term:
        return jsonify({'error': 'Please enter a search term'}), 400
    
    try:
        # Call the real ABR API with filters
        print(f"Starting search for: {search_term}")
        if state_filter:
            print(f"State filter: {state_filter}")
        if postcode_filter:
            print(f"Postcode filter: {postcode_filter}")
            
        xml_content = search_abr_businesses(search_term, state_filter, postcode_filter)
        
        if xml_content is None:
            return jsonify({'error': 'Failed to retrieve data from ABR API. Please try again.'}), 500
        
        # Check if we got valid XML content
        if not xml_content.strip():
            return jsonify({'error': 'No data returned from ABR API'}), 500
        
        print(f"Received XML content length: {len(xml_content)} characters")
        
        # Create temporary files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_search_term = "".join(c for c in search_term if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_search_term = safe_search_term.replace(' ', '_')
        
        # Add filters to filename if they exist
        filename_suffix = ""
        if state_filter:
            filename_suffix += f"_{state_filter}"
        if postcode_filter:
            filename_suffix += f"_P{postcode_filter}"
        
        xml_filename = f"ABRSearch_{safe_search_term}{filename_suffix}_{timestamp}.xml"
        csv_filename = f"ABRSearch_{safe_search_term}{filename_suffix}_{timestamp}.csv"
        
        xml_filepath = os.path.join('downloads', xml_filename)
        csv_filepath = os.path.join('downloads', csv_filename)
        
        # Ensure downloads directory exists
        os.makedirs('downloads', exist_ok=True)
        
        # Save XML file
        with open(xml_filepath, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"Saved XML file: {xml_filepath}")
        
        # Convert to CSV
        records_count = convert_xml_to_csv(xml_content, csv_filepath)
        
        print(f"Converted to CSV with {records_count} records")
        
        return jsonify({
            'success': True,
            'message': f'Successfully processed {records_count} records from ABR',
            'xml_file': xml_filename,
            'csv_file': csv_filename,
            'records_count': records_count
        })
        
    except Exception as e:
        print(f"Error in search function: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join('downloads', filename),
            as_attachment=True,
            download_name=filename
        )
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    # Create downloads directory if it doesn't exist
    os.makedirs('downloads', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
