package main

import (
	"flag"
	"fmt"
	"net"
	"strconv"
	"time"
)

const addr = "100.0.0.1:4343"

var message string

// var blockSize = 1024 * 100
var blockSizePointer = flag.Int("blocksize", 102400, "size of block in bytes")
var delayMilliseconds = flag.Int("delayMilli", 20, "delay in milliseconds")
var numBlocks = flag.Int("numBlocks", 10, "number of blocks to be requested")

func main() {
	flag.Parse()
	conn, err := net.Dial("tcp", addr)

	if err != nil {
		fmt.Println("Error establising TCP connection")
		panic(err)
	}
	requestChuckedData(conn)
}

func requestChuckedData(conn net.Conn) error {
	start := time.Now()
	for i := 0; i < *numBlocks; i++ {
		bytesToRead := *blockSizePointer
		sizeBytesString := strconv.Itoa(bytesToRead) + "\n"
		conn.Write([]byte(sizeBytesString))

		buff := make([]byte, *blockSizePointer)
		for bytesToRead > 0 {
			bytesRead, err := conn.Read(buff)
			if err != nil {
				fmt.Print("ERROR RECEIVING")
				return err
			}
			bytesToRead = bytesToRead - bytesRead
		}
		time.Sleep(time.Duration(*delayMilliseconds) * time.Millisecond)
	}
	print(time.Since(start))
	conn.Close()
	return nil
}
