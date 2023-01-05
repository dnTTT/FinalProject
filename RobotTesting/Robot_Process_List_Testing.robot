*** Settings ***
Library    OperatingSystem
Library    BuiltIn

** *Variables ** *
${HOST}         localhost
${PORT}         5000
${server}

*** Test Cases ***
Test process list service
    # Start the server in a separate process
    ${server}=  Start Process python  process_list_service.py ${HOST} ${PORT}
    Sleep 2s    # Give the server time to start
    # Connect to the server
    Open Connection ${HOST} ${PORT}
    # Send a request for the list of processes
    Write To Connection processes
    # Read the response from the server
    ${response}=    Read Until EOL
    # Verify that the response is correct
    Should Be Equal ${response} expected response
    # Close the connection
    Close Connection
    # Terminate the server process
    Terminate Process ${server}

** *Keywords ** *
return_process_list
# Return a list of processes as a string
${process_list}
Run Process ps - aux
Return    ${process_list}

[Documentation] Establish connection to the TCP socket
process list service {$HOST} {$PORT}
