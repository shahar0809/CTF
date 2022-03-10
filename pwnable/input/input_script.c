#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>


int main(int argc, char* argv[], char* envp[]){
	printf("Let's start hacking :)\n");
	char full_cmd[5000];

	/*************************
	 * STATIC PREPROCESSING
	 * ***********************/
	char* bin_name = "./input";
	sprintf(full_cmd, "%s", bin_name);

	/* Stage 1 */
	char* arguments[100];

	for (int i = 0; i < 100; i++) {
		arguments[i] = "0";
	}
	printf("Done prep stage 1.1\n");

	arguments['A'] = "\x00";
	arguments['B'] = "\x20\x0a\x0d";
	printf("Done prep stage 1.2\n");

	for (int i = 0; i < 100; i++) {
		strcat(full_cmd, " ");
		strcat(full_cmd, arguments[i]);
	}
	printf("Done prep stage 1\n");

	/* Stage 3 - This is pretty simple, we only need to set an environment variable using setenv() */	
	setenv("\xde\xad\xbe\xef", "\xca\xfe\xba\xbe", 1);
	printf("Done prep stage 3\n");

	/* Stage 4 - We need to create a file, with the content described */
	FILE* fp = fopen("\x0a", "wb");
	if(!fp) return 0;
	fwrite("\x00\x00\x00\x00", 1, 4, fp);
	fclose(fp);
	printf("Done prep stage 4\n");

	/*************************
	 * RUNTIME
	 * ***********************/
	// We need to use pipes, in order for parent and child to communicate
	int stdin_pipe[2];
	int stderr_pipe[2];

	pipe(stderr_pipe);
	pipe(stdin_pipe);

	// We want one thread to execute the program, and the other one to send the inputs and data over the socket
	if (fork() != 0) {
		sleep(2);

		close(stdin_pipe[0]);
		close(stderr_pipe[0]);

		printf("Writing to input\n");

		/* Stage 2 - This is the actual input in stdin, so we want to run it after all the preprocessing */
		write(stdin_pipe[1], "\x00\x0a\x00\xff", 4);
		write(stderr_pipe[1], "\x00\x0a\x02\xff", 4);
		printf("Done - Writing to input\n");

		sleep(3);

		printf("Writing to socket\n");

		/* Stage 5 - Need to send content via socket */
		int sd, cd;
		struct sockaddr_in saddr, caddr;
		sd = socket(AF_INET, SOCK_STREAM, 0);

		if(sd == -1) {
			printf("socket error, tell admin\n");
			return 0;
		}

		saddr.sin_family = AF_INET;
		saddr.sin_addr.s_addr = inet_addr("127.0.0.1");
		saddr.sin_port = htons( atoi(argv['C']) );
		printf("Connect to port\n");

	    if (connect(sd, (struct sockaddr *)&saddr, sizeof(saddr)) < 0) 
	    { 
	        printf("\nConnection Failed \n"); 
	        return -1; 
	    }
		printf("Send to input\n");


	    send(sd , "\xde\xad\xbe\xef" , 4 , 0 );
		printf("send to input\n");

	} else {
		close(stdin_pipe[1]);
		close(stderr_pipe[1]);

	    dup2(stdin_pipe[0], STDIN_FILENO);
	    dup2(stderr_pipe[0], STDERR_FILENO);

		close(stdin_pipe[0]);
	    close(stderr_pipe[0]);

	    system(full_cmd);

	}

	return 0;
}
