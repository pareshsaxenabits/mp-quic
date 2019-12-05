package main

import (
	"fmt"
	"net"
	"strconv"
)

const addr = "0.0.0.0:4343"

var fakeBuff = make([]byte, 1024*1024*10) // 10 MB

func main() {
	for i := 0; i < cap(fakeBuff); i++ {
		fakeBuff[i] = 'A'
	}

	ln, err := net.Listen("tcp", addr)
	if err != nil {
		print("Unable to make socket")
		panic(err)
	}

	conn, err := ln.Accept()

	if err != nil {
		print("ERROR ACCEPTING")
		panic(err)
	}

	fmt.Print("Connection made with ")
	fmt.Println(conn.RemoteAddr())

	finished := make(chan bool)

	go func() { handleTCPconn(conn, finished) }()
	<-finished
}

func handleTCPconn(conn net.Conn, finished chan bool) error {
	buff := make([]byte, 1000)

	for {
		var chunkSizeString = ""
		bytesRead, err := conn.Read(buff)
		if err != nil {
			break
		}

		for buff[bytesRead-1] != '\n' {
			chunkSizeString += string(buff[:bytesRead])
		}
		chunkSizeString += string(buff[:bytesRead-1]) // -1 to ignore newline

		chunkSize, err := strconv.Atoi(chunkSizeString)

		if err != nil {
			fmt.Println("Invalid chunk size sent")
		}
		fmt.Printf("Chunk size : %d\n", chunkSize)

		if chunkSize == 0 {
			break
		}

		sendChunckOnTCPConn(conn, chunkSize)

	}

	finished <- true
	return nil

}

func sendChunckOnTCPConn(conn net.Conn, size int) {
	for bytesToSend := size; bytesToSend > 0; {
		bytesSent, _ := conn.Write(fakeBuff[:bytesToSend])
		bytesToSend = bytesToSend - bytesSent
	}

}
