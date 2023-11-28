// file: project4.c
// author: Dr. Schwesinger
// semester: Fall, 2023

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

// TODO: make functions for parent and child
//       error check close(), fdopen(), wait()

int main() {
    const int BUF_SIZE = 4096;

    int pr_cw_fd[2];
    int cr_pw_fd[2];

    if ( (pipe(pr_cw_fd) == -1) || (pipe(cr_pw_fd) == -2) ) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    int child_pid = fork();
    switch(child_pid) {
        case -1:
            perror("fork");
            exit(EXIT_FAILURE);
        case 0: // child
            {
            // close unused file descriptors
            close(pr_cw_fd[0]);
            close(cr_pw_fd[1]);

            // convert file descriptors to FILE*
            FILE* cr = fdopen(cr_pw_fd[0], "r");
            FILE* cw = fdopen(pr_cw_fd[1], "w");

            // 1. The child process will wait to receive the random number from
            // the parent, followed by the second number.
            int int1, int2;
            char cbuf[BUF_SIZE];

            fgets(cbuf, BUF_SIZE, cr);
            int1 = atoi(cbuf);
            printf("Child received from pipe: %d\n", int1);

            fgets(cbuf, BUF_SIZE, cr);
            int2 = atoi(cbuf);
            printf("Child received from pipe: %d\n", int2);
            fflush(stdout);

            // 2. The child will confirm the second number is correct. If it is
            // correct, the child will send the message “Approved” to the
            // parent. If the number is not correct, the child will send the
            // message “Denied” to the parent.
            int result = int2 / getpid();
            char* msg = (result == int1) ? "Approved" : "Denied";
            printf("Child sending to pipe: %s\n", msg);
            fflush(stdout);
            if (fprintf(cw, "%s\n", msg) < 0) {
                perror("fprintf");
                exit(EXIT_FAILURE);
            }
            fflush(cw);

            // 3. The child will then wait for another message (BYE) from the
            // parent indicating it is okay for the child to end. The child
            // process will then end.
            fgets(cbuf, BUF_SIZE, cr);
            // remove trailing new line
            int length = strlen(cbuf);
            if (cbuf[length-1] == '\n') {
                cbuf[length-1] = '\0';
            }
            printf("Child received from pipe: %s\n", cbuf);
            // TODO: verify that the child received "BYE"
            }
            break;

        default: // parent
            // close unused file descriptors
            close(pr_cw_fd[1]);
            close(cr_pw_fd[0]);

            // convert file descriptors to FILE*
            FILE* pr = fdopen(pr_cw_fd[0], "r");
            FILE* pw = fdopen(cr_pw_fd[1], "w");
            //setlinebuf(pr);
            //setlinebuf(pw);

            // 1. The parent process will generate a random number between 0
            // and 100 (not including 0 or 100), using the parent process’s PID
            // as the seed.
            srand(getpid());
            int rand_int = rand() % (100) + 1;

            // 2. The parent will send this random number to the child,
            // followed by a second message containing the product of the
            // random number and the child process’s PID.
            printf("Parent sending to pipe: %d\n", rand_int);
            fflush(stdout);
            fprintf(pw, "%d\n", rand_int);
            fflush(pw);

            printf("Parent sending to pipe: %d\n", rand_int * child_pid);
            fflush(stdout);
            if (fprintf(pw, "%d\n", rand_int * child_pid) < 0) {
                perror("fprintf");
                exit(EXIT_FAILURE);
            }
            fflush(pw);

            // 3. The parent will then wait for a response from the child.
            // After receiving a response from the child, the parent will check
            // the child’s message. If it is “Approved”, the parent will print
            // “Thanks for playing”. If the message received from the child is
            // “Denied”, the parent will print “Wrong. Please play again”.
            char pbuf[BUF_SIZE];
            fgets(pbuf, BUF_SIZE, pr);
            // remove trailing new line
            int length = strlen(pbuf);
            if (pbuf[length-1] == '\n') {
                pbuf[length-1] = '\0';
            }
            printf("Parent received from pipe: %s\n", pbuf);

            if (strcmp(pbuf, "Approved") == 0) {
                printf("Parent: Thanks for playing\n");
            }
            if (strcmp(pbuf, "Denied") == 0) {
                printf("Parent: Wrong. Please play again\n");
            }

            // 4. The parent will then send another message to the child
            // telling the child it is okay to end. This message should be
            // “BYE”. The parent will end after all child processes have ended.
            //sleep(3);

            printf("Parent sending to pipe: %s\n", "BYE");
            fprintf(pw, "%s\n", "BYE");

            wait(NULL);

            break;
    }

    return 0;
}
