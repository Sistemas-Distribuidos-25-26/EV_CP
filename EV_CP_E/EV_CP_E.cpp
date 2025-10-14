#include <iostream>
#include <cstring>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <chrono>
#include <thread>
#include "./EV_CP_E.hpp"

int PORT = 0;
auto STATE = CPState::ACTIVE;

#define SEND_STATE send(client, &STATE, 1, 0)


void get_ko() {
	char message;
	std::cout << "[Engine] Presione una tecla para mandar un K.O" << std::endl;
	while (true)
	{
		message = std::cin.get();
		if(message) STATE = CPState::BROKEN;
	}
}

void handle_monitor(int client){
	while(true){
		char buffer[1] = {0};
		int bytes_received = recv(client, buffer, sizeof(buffer), 0);
		if (bytes_received == -1) {
			std::cerr << "Error en recv" << std::endl;
		} 
		else if(bytes_received == 0){
			std::cerr << "[Engine] El monitor cerró la conexión" << std::endl;
			return;
		}
		else {
			buffer[bytes_received] = '\0';
			
			SEND_STATE;
		}

	}
}

int main(int argc, char **argv){

	if(argc < 2){
		std::cerr << "Uso: EV_CP_E [PUERTO]" << std::endl;
		std::exit(-1);
	}

	PORT = atoi(argv[1]);

	int skt = socket(AF_INET, SOCK_STREAM, 0);
	if(skt < 0){
		std::cerr << "Error al crear el socket" << std::endl;
		exit(-1);
	}

	struct sockaddr_in server;
	memset(&server, 0, sizeof(server));
	server.sin_family = AF_INET;
	server.sin_port = htons(PORT);
	server.sin_addr.s_addr = INADDR_ANY;

    if(bind(skt, (struct sockaddr*)&server, sizeof(server)) == -1){
        std::cerr << "Error en el bind" << std::endl;
        close(skt);
        exit(-1);
    }

    if(listen(skt, 5) == -1){
        std::cerr << "Error en el listen" << std::endl;
        close(skt);
        exit(-1);
    }

	std::cout << "Escuchando en el puerto " << PORT << std::endl;
	int client;

	std::thread t(get_ko);

	while(true){
		client = accept(skt, nullptr, nullptr);
		if(client == -1){
			std::cerr << "Error en el accept" << std::endl;
			close(skt);
			exit(-1);
		}
		handle_monitor(client);
		close(client);
	}

	close(skt);
	return 0;
}