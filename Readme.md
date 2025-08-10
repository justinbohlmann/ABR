# ABR Business Search

A local web application that allows you to search for businesses in the Australian Business Register (ABR) and automatically convert the results to both XML and CSV formats.

## Features

- **Web-based Interface**: Modern, responsive web interface for easy searching
- **Dual Format Output**: Generates both XML and CSV files from search results
- **Automatic Conversion**: Seamlessly converts ABR search results to structured CSV format
- **File Downloads**: Direct download links for both XML and CSV files
- **Real-time Processing**: Instant search and conversion with progress indicators
- **Advanced Filtering**: Filter results by state/territory and postcode
- **Secure Authentication**: Environment variable-based API authentication
- **Production Ready**: Error handling and security best practices

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- ABR API authentication GUID

## Installation

1. **Clone or download the project files** to your local machine

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your ABR Authentication GUID**:
   - Get your authentication GUID from: https://abr.business.gov.au/Tools/WebServices
   - Create a `.env` file in the project root directory
   - Add your GUID to the file:
     ```
     ABR_AUTH_GUID=your_authentication_guid_here
     ```
   - **Important**: Never commit the `.env` file to version control (it's already in `.gitignore`)

4. **Run the application**:
   ```bash
   python "ABR Business search.py"
   ```

5. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Enter a search term** in the search box (e.g., "Midwife", "Consulting", "Lawyer")

2. **Optional: Apply filters**:
   - **State/Territory**: Select a specific state to narrow results
   - **Postcode**: Enter a postcode to filter by location

3. **Click "Search & Convert"** to process your search

4. **Wait for processing** - the application will show a loading spinner

5. **Download your files** - once complete, you'll see download links for:
   - **XML file**: Raw ABR search results in XML format
   - **CSV file**: Converted data in spreadsheet-friendly CSV format

## File Structure

```
ABR/
├── ABR Business search.py # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Specifies intentionally untracked files to ignore
├── .env                  # Environment variables (create this file)
├── templates/            # HTML templates for the web interface
│   └── index.html
└── downloads/            # Generated files (created automatically)
```

## CSV Output Format

The generated CSV file contains the following columns:

- **ABN**: Australian Business Number
- **ABN_Status**: Whether the ABN is Active or not
- **Business_Name**: The name of the business
- **Name_Type**: Type of name (Business Name, Main Name, Trading Name, etc.)
- **Score**: Search relevance score
- **Is_Current**: Whether the name is current (Y/N)
- **State_Code**: Australian state/territory code
- **Postcode**: Postal code

## Security Features

- **Environment Variables**: Authentication GUID stored securely in `.env` file
- **No Hardcoded Credentials**: Application fails gracefully if `.env` is missing
- **Git Protection**: `.env` file automatically excluded from version control
- **Error Handling**: Clear error messages for missing configuration

## Technical Details

### API Integration

The application integrates with the official ABR API:
- **Endpoint**: `https://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx/ABRSearchByNameAdvancedSimpleProtocol2017`
- **Authentication**: GUID-based authentication via environment variables
- **Response Format**: XML with business registration data
- **Rate Limiting**: Respects ABR API usage guidelines

### Search Capabilities

- **Name Search**: Search by business name, trading name, or legal name
- **State Filtering**: Filter results by Australian states and territories
- **Postcode Filtering**: Narrow results by specific postcodes
- **Active ABNs Only**: Returns only currently active business registrations
- **Score-based Ranking**: Results ranked by relevance score

## Troubleshooting

### Common Issues

1. **"ABR_AUTH_GUID environment variable is not set"**:
   - Create a `.env` file in the project root
   - Add your authentication GUID: `ABR_AUTH_GUID=your_guid_here`

2. **Port already in use**: If you get an error about port 5000 being in use, modify the port in the application:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)  # Change to different port
   ```

3. **Missing dependencies**: Ensure all requirements are installed:
   ```bash
   pip install -r requirements.txt
   ```

4. **No search results**: Some search terms may not return results from the ABR database. Try:
   - Different search terms
   - Removing filters
   - Checking spelling

### Error Messages

- **"Please enter a search term"**: Make sure you've entered text in the search box
- **"Failed to retrieve data from ABR API"**: Check your internet connection and authentication GUID
- **"File not found"**: The generated files may have been moved or deleted

## Development

### Adding Features

To extend the application:

1. **Modify `ABR Business search.py`** for backend logic changes
2. **Update `templates/index.html`** for frontend changes
3. **Add new routes** in Flask for additional functionality

### Customization

- **Styling**: Modify the CSS in `templates/index.html`
- **Search parameters**: Adjust the search logic in the main application file
- **Output format**: Modify the CSV conversion function

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the error messages in the browser console
3. Check the Python console output for backend errors
4. Verify your `.env` file is properly configured

## Example Usage

1. Start the application: `python "ABR Business search.py"`
2. Open browser to `http://localhost:5000`
3. Enter "consultant" in the search box
4. Enter "2232" in the postcode filter
5. Click "Search & Convert"
6. Download both XML and CSV files
7. Open the CSV file in Excel or Google Sheets for analysis

The application will generate files like:

- `ABRSearch_consultant_P2232_20250810_165504.xml`
- `ABRSearch_consultant_P2232_20250810_165504.csv`

## Security Notes

- **Never commit your `.env` file** to version control
- **Keep your authentication GUID private** and secure
- **The application will fail to start** if the `.env` file is missing or invalid
- **All sensitive data is excluded** from the GitHub repository
