package main

import (
	"crypto/tls"
	"fmt"
	"strconv"
	"time"

	quic "github.com/lucas-clemente/quic-go"
)

const addr = "100.0.0.1:4242"

// message := "abcdefghijklmnopqrstuvwxyz"
var message string

func main() {
	message = "abcdefghijklmnopqrstuvwxyz"
	for i := 0; i < 10; i++ {
		message = message + message
	}

	for i := 0; i < 1; i++ {
		quicConfig := &quic.Config{
			CreatePaths: true,
		}

		sess, err := quic.DialAddr(addr, &tls.Config{InsecureSkipVerify: true}, quicConfig)
		if err != nil {
			fmt.Println("Error Connecting")
			panic(err)
		}
		fmt.Println("Address Dialled")

		stream1, err := sess.OpenStreamSync()
		print("HERE")
		if err != nil {
			fmt.Println("Error Opening Stream 1")
			// panic(err)
			print(err)
		}
		finished := make(chan bool)

		go func() { sendDataOnStream(stream1, 1, finished) }()
		print("GO FUNC MADE ")
		<-finished
	}
	// stream2, err := sess.OpenStreamSync()
	// if err != nil {
	// 	fmt.Println("Error Opening Stream 2")
	// 	panic(err)
	// }
	// go func() { sendDataOnStream(stream2, 1) }()

	// stream3, err := sess.OpenStreamSync()
	// if err != nil {
	// 	fmt.Println("Error Opening Stream 3")
	// 	panic(err)
	// }
	// go func() { sendDataOnStream(stream3, 1) }()

	// stream4, err := sess.OpenStreamSync()
	// if err != nil {
	// 	fmt.Println("Error Opening Stream 4")
	// 	panic(err)
	// }
	// go func() { sendDataOnStream(stream4, 1) }()

}

func sendDataOnStream(stream quic.Stream, clientID int, c chan bool) error {
	customMessage := message + strconv.Itoa(clientID) + "\n"
	for i := 1; i < 100; {
		_, err := stream.Write([]byte(customMessage))
		// fmt.Println(n)
		time.Sleep(time.Second)
		if err != nil {
			fmt.Println("error sending in client " + string(clientID))
			c <- true
			return err
		}
	}
	c <- true
	stream.Close()
	return nil
}
