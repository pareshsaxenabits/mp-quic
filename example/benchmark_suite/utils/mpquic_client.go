package main

import (
	"crypto/tls"
	"fmt"
	"strconv"
	"time"

	quic "github.com/lucas-clemente/quic-go"
)

const addr = "100.0.0.1:4242"

var message string
var blockSize = 1024 * 100

func main() {

	quicConfig := &quic.Config{
		CreatePaths: true,
	}

	sess, err := quic.DialAddr(addr, &tls.Config{InsecureSkipVerify: true}, quicConfig)
	if err != nil {
		fmt.Println("Error Connecting")
		panic(err)
	}

	stream1, err := sess.OpenStream()
	finished := make(chan bool)

	requestChunkedData(stream1, finished)
}

func requestChunkedData(stream quic.Stream, finished chan bool) error {
	start := time.Now()
	for i := 0; i < 10; i++ {
		bytesToRead := blockSize
		sizeBytesString := strconv.Itoa(bytesToRead) + "\n"
		stream.Write([]byte(sizeBytesString))

		buff := make([]byte, blockSize)
		for bytesToRead > 0 {
			bytesRead, err := stream.Read(buff)
			if err != nil {
				fmt.Println("ERROR requestrequestChunkedData")
				return err
			}
			bytesToRead = bytesToRead - bytesRead
		}
		time.Sleep(20 * time.Millisecond)
	}
	print(time.Since(start))
	// print("Closing stream")
	stream.Close()
	// finished <- true
	return nil
}
