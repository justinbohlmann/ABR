# ABR Business Search

A local web application that allows you to search for businesses in the Australian Business Register (ABR) and automatically convert the results to both XML and CSV formats.

## Features

- **Web-based Interface**: Modern, responsive web interface for easy searching
- **Dual Format Output**: Generates both XML and CSV files from search results
- **Automatic Conversion**: Seamlessly converts ABR search results to structured CSV format
- **File Downloads**: Direct download links for both XML and CSV files
- **Real-time Processing**: Instant search and conversion with progress indicators

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

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
   python ABR Business search.py
   ```

5. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Enter a search term** in the search box (e.g., "Midwife", "Consulting", "Lawyer")

2. **Click "Search & Convert"** to process your search

3. **Wait for processing** - the application will show a loading spinner

4. **Download your files** - once complete, you'll see download links for:
   - **XML file**: Raw ABR search results in XML format
   - **CSV file**: Converted data in spreadsheet-friendly CSV format

## File Structure

```
ABR/
├── ABR Business search.py # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface template
├── downloads/            # Generated files (created automatically)
└── xml_to_csv_converter.py  # Standalone XML to CSV converter
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

## Technical Details

### Current Implementation

The current version uses sample data to demonstrate the functionality. In a production environment, you would need to:

1. **Register for ABR API access** at the Australian Business Register website
2. **Obtain API credentials** (authentication GUID)
3. **Modify the `search_abr_businesses()` function** in `app.py` to use real API calls

### API Integration

To integrate with the real ABR API:

1. Visit: https://abr.business.gov.au/
2. Register for API access
3. Replace the sample data generation in `app.py` with actual API calls
4. Update the authentication parameters

## Troubleshooting

### Common Issues

1. **Port already in use**: If you get an error about port 5000 being in use, modify the port in `app.py`:

   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)  # Change to different port
   ```

2. **Missing dependencies**: Ensure all requirements are installed:

   ```bash
   pip install -r requirements.txt
   ```

3. **Permission errors**: Make sure you have write permissions in the project directory for file creation

### Error Messages

- **"Please enter a search term"**: Make sure you've entered text in the search box
- **"Network error"**: Check your internet connection
- **"File not found"**: The generated files may have been moved or deleted

## Development

### Adding Features

To extend the application:

1. **Modify `app.py`** for backend logic changes
2. **Update `templates/index.html`** for frontend changes
3. **Add new routes** in Flask for additional functionality

### Customization

- **Styling**: Modify the CSS in `templates/index.html`
- **Search parameters**: Adjust the search logic in `app.py`
- **Output format**: Modify the CSV conversion function in `app.py`

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the error messages in the browser console
3. Check the Python console output for backend errors

## Example Usage

1. Start the application: `python ABR Business search.py`
2. Open browser to `http://localhost:5000`
3. Enter "Midwife" in the search box
4. Click "Search & Convert"
5. Download both XML and CSV files
6. Open the CSV file in Excel or Google Sheets for analysis

The application will generate files like:

- `ABRSearch_Midwife_20241201_143022.xml`
- `ABRSearch_Midwife_20241201_143022.csv`
