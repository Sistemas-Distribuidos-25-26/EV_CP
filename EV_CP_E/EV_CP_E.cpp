#include <iostream>
#include <cstring>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include "./EV_CP_E.hpp"

int PORT = 0;
auto STATE = CPState::ACTIVE;

int main(int argc, char **argv){

	if(argc < 3){
		std::cerr << "Uso: EV_CP_E [IP_Monitor] [Puerto_Monitor]" << std::endl;
		std::exit(-1);
	}

	PORT = atoi(argv[2]);

	int skt = socket(AF_INET, SOCK_STREAM, 0);
	if(skt < 0){
		std::cerr << "Error al crear el socket" << std::endl;
		exit(-1);
	}

	struct sockaddr_in server;
	memset(&server, 0, sizeof(server));
	server.sin_family = AF_INET;
	server.sin_port = htons(PORT);
	server.sin_addr.s_addr = inet_pton(AF_INET, argv[1], &server.sin_addr);

	if(inet_pton(AF_INET, argv[1], &server.sin_addr) != 1){
		std::cerr << "Dirección inválida" << std::endl;
		close(skt);
		exit(-1);
	}

	if(connect(skt, (struct sockaddr*)&server, sizeof(server)) < 0){
		std::cerr << "Error en la conexión" << std::endl;
		close(skt);
		exit(-1);
	}


	send(skt, &STATE, 1, 0);

	close(skt);
	return 0;
}