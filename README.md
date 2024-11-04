# GO PHOTONICS SCRAPER 💥

CLI web scraper for Go Photonics: quick access to photonics and lab equipment data for researchers 

All data is scraped from [Go Photonics](https://www.gophotonics.com/)

![https://github.com/ANG13T/satnow-scraper/blob/main/assets/PHOTONICS_1.png](https://github.com/ANG13T/satnow-scraper/blob/main/assets/PHOTONICS_1.png)

### 0x00 > Features
- Extracts details about photonics component specifications
- Extracts details about manufacturers
- Displays the data in a tabular format via TUI
- Data download support for `JSON`, `TXT`, and `CSV` formats

### 0x01 > Usage
```
git clone https://github.com/ANG13T/gophotonics-scraper.git
cd gophotonics-scraper
pip install -r requirements.txt
python3 gophotonicsscraper.py
```

### 0x02 > Previews

![https://github.com/ANG13T/satnow-scraper/blob/main/assets/SNS_3.png](https://github.com/ANG13T/satnow-scraper/blob/main/assets/PHOTONICS_1.png)

![https://github.com/ANG13T/satnow-scraper/blob/main/assets/SNS_3.png](https://github.com/ANG13T/satnow-scraper/blob/main/assets/PHOTONICS_2.png)

![https://github.com/ANG13T/satnow-scraper/blob/main/assets/SNS_3.png](https://github.com/ANG13T/satnow-scraper/blob/main/assets/PHOTONICS_3.png)

![https://github.com/ANG13T/satnow-scraper/blob/main/assets/SNS_3.png](https://github.com/ANG13T/satnow-scraper/blob/main/assets/PHOTONICS_4.png)

### 0x03 > Contributing 
Go Photonics Scraper is open to any contributions. Please fork the repository and make a pull request with the features or fixes you want to implement.

### 0x04 > Suggested Implementations
- Extract manufacturer details for catalogs that contain item information (ie. `Acousto-Optic Deflectors`). Please check `modules/scraper.py` for the `get_manufacturer_details` function.

### 0x05 > Support 
If you enjoyed Go Photonics Scraper, please consider becoming a sponsor in order to fund my future projects.

To check out my other works, visit my [GitHub profile](github.com/ANG13T).