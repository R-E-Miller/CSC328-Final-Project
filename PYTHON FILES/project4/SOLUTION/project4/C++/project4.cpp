// file: project4.cpp
// author: Dr. Schwesinger
// semester: Fall, 2023
//
#include <unistd.h>
#include <sys/wait.h>
#include <iostream>
#include <limits>
#include <ext/stdio_filebuf.h> // to convert fd to stream

// TODO: check if file descriptors get closed when the stream destructors
// are called

void parent(int pr_cw_fd[2], int cr_pw_fd[2], pid_t pid) {

    // close unused file descriptors
    // TODO: error check close
    close(pr_cw_fd[1]);
    close(cr_pw_fd[0]);

    // convert file descriptors to stream objects
    __gnu_cxx::stdio_filebuf<char> pr(pr_cw_fd[0], std::ios::in);
    __gnu_cxx::stdio_filebuf<char> pw(cr_pw_fd[1],std::ios::out);
    std::istream p_in(&pr);
    std::ostream p_out(&pw);
    p_in.exceptions(std::ifstream::failbit | std::ifstream::badbit);
    p_out.exceptions(std::ofstream::failbit | std::ofstream::badbit);
    try {

        srand(getpid());
        int rand_int = rand() % 99 + 1;
        int product = rand_int * pid;

        std::cout << "Parent sending to pipe: " << rand_int << std::endl;
        p_out << rand_int << std::endl;

        std::cout << "Parent sending to pipe: " << product << std::endl;
        p_out << product << std::endl;

        std::string response;
        getline(p_in, response);
        std::cout << "Parent received from pipe: " << response << std::endl;

        // TODO: check response and print appropriate message

        std::cout << "Parent sending to pipe: BYE" << std::endl;
        p_out << "BYE" << std::endl;
    }
    catch (std::ios::failure e) {
        std::cerr << "fstream exception" << std::endl;
    }
}

void child(int pr_cw_fd[2], int cr_pw_fd[2]) {
    // close unused file descriptors
    // TODO: error check close
    close(pr_cw_fd[0]);
    close(cr_pw_fd[1]);

    // convert file descriptors to stream objects
    __gnu_cxx::stdio_filebuf<char> cr(cr_pw_fd[0], std::ios::in);
    __gnu_cxx::stdio_filebuf<char> cw(pr_cw_fd[1], std::ios::out);
    std::istream c_in(&cr);
    std::ostream c_out(&cw);
    c_in.exceptions(std::ifstream::failbit | std::ifstream::badbit);
    c_out.exceptions(std::ofstream::failbit | std::ofstream::badbit);
    try {
        int rand_int, product;
        c_in >> rand_int;
        c_in.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Child received from pipe: " << rand_int << std::endl;

        c_in >> product;
        c_in.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Child received from pipe: " << product << std::endl;

        std::string msg = (rand_int * getpid() == product) ? "Approved" : "Denied";
        std::cout << "Child sending to pipe: " << msg << std::endl;
        c_out << msg << std::endl;

        std::string response;
        getline(c_in, response);
        std::cout << "Child received from pipe: " << response << std::endl;

        // TODO: verify that the child received "BYE"
    }
    catch (std::ios::failure e) {
        std::cerr << "fstream exception" << std::endl;
    }
}

int main() {

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
        case 0:
            child(pr_cw_fd, cr_pw_fd);
            break;
        default:
            parent(pr_cw_fd, cr_pw_fd, child_pid);
            if (wait(NULL) == -1) {
                perror("wait");
                exit(-1);
            };
            break;
    }

    return 0;
}
