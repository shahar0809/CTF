#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(int argc, char* argv[], char* envp[]){
	printf("Let's start hacking :)\n");

	/*************************
	 * STATIC PREPROCESSING
	 * ***********************/
	const char* full_cmd = "./input"

	/* Stage 1 */
	char* arguments[100];

	for (int i = 0; i < 100; i++) {
		arguments[i] = '0';
	}

	arguments['A'] = "\x00";
	arguments['B'] = "\x20\x0a\x0d";

	for (int i = 0; i < 100; i++) {
		strcat(full_cmd, " ");
		strcat(full_cmd, arguments[i]);
	}

	/* Stage 3 - This is pretty simple, we only need to set an environment variable using setenv() */	
	setenv("\xde\xad\xbe\xef", "\xca\xfe\xba\xbe");

	/* Stage 4 - We need to create a file, with the content described */
	FILE* fp = fopen("\x0a", "wb");
	if(!fp) return 0;
	fwrite("\x00\x00\x00\x00", 1, 4, fp);
	fclose(fp);

	/*************************
	 * RUNTIME
	 * ***********************/

	system(full_cmd);

	/* Stage 2 - This is the actual input in stdin, so we want to run it after all the preprocessing */
	char buf[4];
	memcpy(buf, "\x00\x0a\x00\xff", 4);
	// send input

	memcpy(buf, "\x00\x0a\x02\xff", 4);
	// send input

	/* Stage 5 - Need to send content via socket */
	int sd, cd;
	struct sockaddr_in saddr, caddr;
	sd = socket(AF_INET, SOCK_STREAM, 0);

	if(sd == -1) {
		printf("socket error, tell admin\n");
		return 0;
	}

	saddr.sin_family = AF_INET;
	saddr.sin_addr.s_addr = INADDR_ANY;
	saddr.sin_port = htons( atoi(argv['C']) );

	// Convert IPv4 and IPv6 addresses from text to binary form 
    if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) 
    { 
        printf("\nInvalid address/ Address not supported \n"); 
        return -1; 
    } 

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) 
    { 
        printf("\nConnection Failed \n"); 
        return -1; 
    }

    send(sock , "\xde\xad\xbe\xef" , 4 , 0 ); 

	return 0;
}
