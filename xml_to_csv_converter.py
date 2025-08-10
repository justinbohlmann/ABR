import xml.etree.ElementTree as ET
import csv
import sys

def convert_xml_to_csv(xml_file_path, csv_file_path):
    """
    Convert ABR XML search results to CSV format.
    
    Args:
        xml_file_path (str): Path to the input XML file
        csv_file_path (str): Path to the output CSV file
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        # Define the namespace
        namespace = {'abr': 'http://abr.business.gov.au/ABRXMLSearch/'}
        
        # Find all search results records
        search_results = root.findall('.//abr:searchResultsRecord', namespace)
        
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
        
        print(f"Successfully converted {len(search_results)} records to {csv_file_path}")
        
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error converting XML to CSV: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Input and output file paths
    xml_file = "ABRSearchByNameAdvancedSimpleProtocol2017 - Midwife.xml"
    csv_file = "midwife_businesses.csv"
    
    # Convert XML to CSV
    convert_xml_to_csv(xml_file, csv_file)
