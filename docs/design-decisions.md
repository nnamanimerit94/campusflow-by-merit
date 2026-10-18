# Campusflow design decision 

## Decision 1: Ticket collection

For the ticket collection data structure, my member and i decided to use dictionary to store the tickets dictionary this is is as a result of the facf that dictionary users O(1)
 average-case time complexity for ticket lookup. while using list to search for a particular tickets which will require one to loop through all the tickets in that list but with dictionary using the key to fetch a ticket is quite easy. we decided to use strictly the id as the key.

## Decision 2: Input validation
we decided to create a function that specifically handles validating the input separated from the cli input handling first to ensure and have a clear separation of functions that handles it and also keeping the code free from unnecessary repetitive validation check

## Function Contracts

Purpose: to have a clear separated function that checks if value of affected_users is an int and the number is greated than or equal to 1 , else if valueerror or typeerror raises an exception 

Parameter: it receives the value of the affected_users

Accepted values: positive integers greater than or equal to one excluding booleans

Return value:first it checks if its a number and it returns the number back if positive

Errors: if theres an error it returns a the actual error raised 

Side effects: None. The function does not modify external data, print messages, or read user input.