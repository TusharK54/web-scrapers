
import requests
from bs4 import BeautifulSoup
from sys import stdout

datasets_folder = 'datasets'

def get_student_center_response(netID:str, password:str, session:requests.Session) -> requests.Response:
    """
    Returns the HTTP response after logging into the Student Center account associated with the given credentials.
    NOTE: For some reason, the returned response is not what is expected so this function is deprecated.

    Parameters:
    netID (str)                 - The net ID of the user
    password (str)              - The password of the user
    session (requests.Session)  - A requests Session object to hold the credentials required to continue operating on the response
    """
    login_info = {'netid': netID, 'password': password}

    # Scrape action url from login url
    print('Fetching session info from login page ..', end=' ')
    stdout.flush()
    login_url = 'https://css.adminapps.cornell.edu/psp/cuselfservice/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?'
    login_response = session.get(login_url)
    soup = BeautifulSoup(login_response.text, 'lxml')
    action_url = 'https://web3.login.cornell.edu/' + soup.find('form', {'name': 'login'})['action']
    print(login_response.status_code)

    # Log into Student Center
    print('Posting login and session credentials ..', end=' ')
    stdout.flush()
    action_response = session.post(action_url, data=login_info)
    print(action_response.status_code)

    # Access the redirect to the student center page
    print('Fetching redirect to student center ....', end=' ')
    stdout.flush()
    soup = BeautifulSoup(action_response.text, 'lxml')
    credentials = soup.find('input', {'name': 'wa'})['value']
    redirect_credentials = {'wa': credentials}
    redirect_url = soup.find('form', {'name': 'bigpost'})['action']
    redirect_response = session.post(redirect_url, data=redirect_credentials)
    print(redirect_response.status_code)

    return redirect_response

if __name__ == "__main__":
    netid, password = 'tak62', 'you-thought'
    with requests.Session() as session:
        page = get_student_center_response(netid, password, session)
        soup = BeautifulSoup(page.text, 'lxml')
        print(soup)