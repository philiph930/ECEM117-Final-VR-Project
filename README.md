To run privacy policy webscraper <br />
pip install selenium <br />
pip install bs4 <br />
install firefox <br />
install geckodriver and update location of download in file <br />
then run the python file <br />
it will output all the links and the status of the privacy policy <br />
ex: <br />
{'Game': '/experiences/yeeps-hide-and-seek/7276525889052788/', 'Status': 'No mention of Collected'} <br />
{'Game': '/experiences/meta-horizon-worlds/2532035600194083/', 'Status': 'Collected and Unsecured'} <br />

Added csv file output to help with analysis, will have game name and then 0 if No Private Policy Found, 1 if Privacy Policy Found but not Secure and 2 if Privacy Policy Found and Secure <br />
