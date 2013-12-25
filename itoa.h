
/*---------------------------------------------------------------------+
|                Copyright (c) 1996, SAS Institute Inc.                |
|                  Unpublished - All Rights Reserved                   |
|                      S A S / C   S A M P L E                         |
|                                                                      |
|         NAME: ITOA                                                   |
|     LANGUAGE: C                                                      |
|      PURPOSE: Provide a function to convert an integer to a string.  |
|        NOTES: ITOA is implemented as a full-function C MAIN          |
|               program. To implement ITOA as sub-function, remove     |
|               the C MAIN function, compile ITOA and link with your   |
|               application.                                           |
|   MVS -                                                              |
|      COMPILE, LINK, EXECUTE: SUBMIT prefix.SAMPLE.AUX(LC370CLG)      |
|        NOTES: On the EXEC statement add a: ,PARM.GO='value'          |
|               where "value" is the integer to be converted,          |
|   TSO -                                                              |
|      COMPILE: LC370 CLIST                                            |
|         LINK: CLK370 CLIST                                           |
|      EXECUTE: CALL 'your.load.library(ITOA)' 'value'                 |
|        NOTES: where "value" is the integer to be converted,          |
|   CMS -                                                              |
|      COMPILE: LC370 ITOA                                             |
|         LINK: CLINK ITOA (GENMOD                                     |
|      EXECUTE: ITOA 'value'                                           |
|        NOTES: where "value" is the integer to be converted,          |
|   MISC NOTES: This sample is a complement to the ANSI standard       |
|               function "atoi()", which converts a string to an       |
|               equivalent integer. "itoa()" is not a ANSI standard    |
|               function, but is provided for compatability with       |
|               systems that implement the function.                   |
|                                                                      |
+---------------------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INTSIZE 10           /* maximum characters integer           */

/*--------------------------------------------------------------------+
| itoa() - returns a pointer to the string equivalent or NULL if an   |
|          error occurs                                               |
+--------------------------------------------------------------------*/
char *itoa(int n);



/*--------------------------------------------------------------------+
| itoa() - manage the sign, compute the string equivalent, and call   |
| memcpy().                                                           |
+--------------------------------------------------------------------*/
char *itoa(int value)
{
int count,                   /* number of characters in string       */
    i,                       /* loop control variable                */
    sign;                    /* determine if the value is negative   */
char *ptr,                   /* temporary pointer, index into string */
     *string,                /* return value                         */
     *temp;                  /* temporary string array               */

count = 0;
if ((sign = value) < 0)      /* assign value to sign, if negative    */
   {                         /* keep track and invert value          */
   value = -value;
   count++;                  /* increment count                      */
   }

/* allocate INTSIZE plus 2 bytes (sign and NULL)                     */
temp = (char *) malloc(INTSIZE + 2);
if (temp == NULL)
   {
   return(NULL);
   }
memset(temp,'\0', INTSIZE + 2);

string = (char *) malloc(INTSIZE + 2);
if (string == NULL)
   {
   return(NULL);
   }
memset(string,'\0', INTSIZE + 2);
ptr = string;                /* set temporary ptr to string          */

/*--------------------------------------------------------------------+
| NOTE: This process reverses the order of an integer, ie:            |
|       value = -1234 equates to: char [4321-]                        |
|       Reorder the values using for {} loop below                    |
+--------------------------------------------------------------------*/
do {
   *temp++ = value % 10 + '0';   /* obtain modulus and or with '0'   */
   count++;                      /* increment count, track iterations*/
   }  while (( value /= 10) >0);

if (sign < 0)                /* add '-' when sign is negative        */
   *temp++ = '-';

*temp-- = '\0';              /* ensure null terminated and point     */
                             /* to last char in array                */

/*--------------------------------------------------------------------+
| reorder the resulting char *string:                                 |
| temp - points to the last char in the temporary array               |
| ptr  - points to the first element in the string array              |
+--------------------------------------------------------------------*/
for (i = 0; i < count; i++, temp--, ptr++)
   {
   memcpy(ptr,temp,sizeof(char));
   }

return(string);
}



