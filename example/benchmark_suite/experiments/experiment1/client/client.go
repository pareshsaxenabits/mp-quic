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
var blockSize = 1024 * 1024

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
	// <-finished
	// print("finished")
}

func requestChunkedData(stream quic.Stream, finished chan bool) error {
	start := time.Now()
	for i := 0; i < 100; i++ {
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
			// fmt.Print(string(buff[:bytesRead]))
		}
		// fmt.Println()
		time.Sleep(2 * time.Millisecond)
	}
	print(time.Since(start))
	// print("Closing stream")
	stream.Close()
	// finished <- true
	return nil
}

// func main() {
// 	message = "abcdefghijklmnopqrstuvwxyz"
// 	for i := 0; i < 10; i++ {
// 		message = message + message
// 	}

// 	for i := 0; i < 1; i++ {
// 		quicConfig := &quic.Config{
// 			CreatePaths: true,
// 		}

// 		sess, err := quic.DialAddr(addr, &tls.Config{InsecureSkipVerify: true}, quicConfig)
// 		if err != nil {
// 			fmt.Println("Error Connecting")
// 			panic(err)
// 		}
// 		fmt.Println("Address Dialled")

// 		stream1, err := sess.OpenStreamSync()
// 		print("HERE")
// 		if err != nil {
// 			fmt.Println("Error Opening Stream 1")
// 			// panic(err)
// 			print(err)
// 		}
// 		finished := make(chan bool)

// 		go func() { sendDataOnStream(stream1, 1, finished) }()
// 		print("GO FUNC MADE ")
// 		<-finished
// 	}

// }

// func sendDataOnStream(stream quic.Stream, clientID int, c chan bool) error {
// 	customMessage := message + strconv.Itoa(clientID) + "\n"
// 	for i := 1; i < 100; {
// 		_, err := stream.Write([]byte(customMessage))
// 		// fmt.Println(n)
// 		time.Sleep(time.Second)
// 		if err != nil {
// 			fmt.Println("error sending in client " + string(clientID))
// 			c <- true
// 			return err
// 		}
// 	}
// 	c <- true
// 	stream.Close()
// 	return nil
// }
