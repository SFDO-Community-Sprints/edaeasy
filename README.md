### Project Name
EDAEASY

### Project Team
* Team Leader(s): Thaddaeus Dahlberg
* GitHub Scribe(s): Farrah Friedrich
* List of all Contributors: Jason Lantz, Kathy Lueckeman, Steph Sisson

### Project Vision (Your first task as a team)
Our vision for this project is to make it easier for higher ed institutions to try out the EDA/EASY/Interactions Salesforce products. The current process to install, configure and data load data takes a significant amount of manual work. This will automate the entire process in a scratch org, allowing for faster review and testing of existing functionality. 

We will create a package using CumulusCI to spin up a scratch org that will:
1. Contain EDA
2. Contain EASY with Interactions
3. Contain pre-loaded configuration and test data


## Development

To work on this project in a scratch org:

1. [Set up CumulusCI](https://cumulusci.readthedocs.io/en/latest/tutorial.html)
2. Run `cci flow run dev_org --org dev` to deploy this project.
3. Run `cci org browser dev` to open the org in your browser.
