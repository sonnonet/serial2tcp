#include <pthread.h>

#include <string.h>

#include <stdio.h>

#include <stdlib.h>

#include <unistd.h> //Used for UART

#include <fcntl.h> //Used for UART



#include <termios.h> //Used for UART

#include <errno.h>

#include <ctype.h>


int uart0 = -1;

int t_flag; /* flag for thread creation */
int exit_flag;
pthread_t tid;
extern FILE *stdin;

#define NUM_PRINT_BYTES  16
enum {
    STRING = 1,
    BINARY,
};

enum {
    FALSE,
    TRUE,
};

void print_bytes(int type, int length, unsigned char *buffer)
{
    int i;
    char temp[NUM_PRINT_BYTES] = {0,};

    for (i = 0; i < length; i++) {
        printf("%02x ", buffer[i]);
        temp[i%NUM_PRINT_BYTES] = buffer[i];
        if (((i + 1) % NUM_PRINT_BYTES) == 0) {
            if (type == STRING) {
                printf("\t%s", temp);
            }
            printf("\n");
            memset(temp, 0, NUM_PRINT_BYTES);
        }
    }
    if (type == STRING) {
        if (i % NUM_PRINT_BYTES != 0)
            printf("\t%s", temp);
    }
}
void *serial_rx(void *arg)
{
    unsigned char rx_bin[128] = {0,};
    unsigned char rx_hex[256] = {0,};
    int rx_length = 0;

    t_flag = 1;

    do {
        // Read up to 255 characters from the port if they are there
        rx_length = read(uart0, (void*)rx_bin, 255);
        if (rx_length > 0) {
            //Bytes received
            rx_bin[rx_length] = '\0';
            bin2hex(rx_bin, rx_length, rx_hex);
            printf("RX BUFFER(%d) : #######\n", rx_length);
            printf("  hexa string : ");
            print_bytes(BINARY, rx_length, rx_bin);
            printf("  binary : ");
            print_bytes(STRING, rx_length * 2, rx_hex);
        } else {
            /* something? */
        }
        usleep(100000);
    } while (exit_flag == FALSE);

    return NULL;
}

int rx_thread_create(void)
{
    int ret = 0;
    pthread_attr_t attr;

    ret = pthread_attr_init(&attr);
    if (ret != 0) {
        perror("pthread_attr_init failed");
        return -1;
    }

    ret = pthread_create(&tid, &attr, &serial_rx, NULL);
    if (ret != 0) {
        perror("pthread_create failed");
        return -1;
    }

    ret = pthread_attr_destroy(&attr);
    if (ret != 0) {
        perror("pthread_attr_destroy failed");
        return -1;
    }

    return ret;
}

int tx_loop(void)
{
    unsigned char tx_hex[256] = {0,};
    unsigned char tx_bin[128] = {0,};
    int count = 0;

    do {
        fscanf(stdin, "%s", tx_hex);
        printf("TX BUFFER : #######\n");
        hex2bin(tx_hex, tx_bin, strlen(tx_hex));
        printf("  hexa string : ");
        print_bytes(STRING, strlen(tx_hex), tx_hex);
        printf("  binary : ");
        print_bytes(BINARY, strlen(tx_hex) / 2, tx_bin);

        /* Filestrean, bytes to write, number of bytes to write */
        count = write(uart0, &tx_bin[0], strlen(tx_hex) / 2);
        if (count < 0) {
            printf("UART TX error\n");
            close(uart0);
            return -1;
        }
        usleep(10000);
    } while (strcmp(tx_hex, "FF") != 0);
    exit_flag = TRUE;
}

int main(void)
{

    struct termios options;

    int ret = 0;

    void *res;



    printf("Usage : type 'something', then see 'something'\n");

    printf("Usage : type 'FF' to exit\n\n");



    /* Open UART Device */

    uart0 = open("/dev/ttyAMA0", O_RDWR | O_NOCTTY | O_NDELAY);

    if (uart0 == -1) {

        printf("Error - Unable to open UART\n");

        close(uart0);

        return -1;

    }



    /* Set Config UART */

    tcgetattr(uart0, &options);

    options.c_cflag = B4800 | CS8 | CLOCAL | CREAD | IXOFF; //<Set baud rate

    options.c_iflag = IGNPAR | ICRNL;

    options.c_oflag = 0;

    options.c_lflag = 0;

    cfsetispeed(&options, B4800);

    cfsetospeed(&options, B4800);



    tcflush(uart0, TCIFLUSH);

    tcsetattr(uart0, TCSANOW, &options);



    /* RX */

    rx_thread_create();

    while (t_flag != 1) {

        usleep(10000);

    }



    /* TX */

    ret = tx_loop();

    if (ret < 0)

        return -1;



    pthread_join(tid, &res);



    close(uart0);

    return 0;
}

