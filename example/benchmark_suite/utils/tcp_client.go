package main

import (
	"fmt"
	"net"
	"strconv"
	"time"
)

const addr = "100.0.0.1:4343"

var message string
var blockSize = 1024 * 100

func main() {
	conn, err := net.Dial("tcp", addr)

	if err != nil {
		fmt.Println("Error establising TCP connection")
		panic(err)
	}

	requestChuckedData(conn)
}

func requestChuckedData(conn net.Conn) error {
	start := time.Now()
	for i := 0; i < 10; i++ {
		bytesToRead := blockSize
		sizeBytesString := strconv.Itoa(bytesToRead) + "\n"
		conn.Write([]byte(sizeBytesString))

		buff := make([]byte, blockSize)
		for bytesToRead > 0 {
			bytesRead, err := conn.Read(buff)
			if err != nil {
				fmt.Print("ERROR RECEIVING")
				return err
			}
			bytesToRead = bytesToRead - bytesRead
		}
		time.Sleep(20 * time.Millisecond)
	}
	print(time.Since(start))
	conn.Close()
	return nil
}
