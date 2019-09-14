package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"io"
	"math/big"

	quic "github.com/lucas-clemente/quic-go"
)

const addr = "0.0.0.0:4242"

func main() {
	quicConfig := &quic.Config{
		CreatePaths: true,
	}
	listener, err := quic.ListenAddr(addr, generateTLSConfig(), quicConfig)

	for {
		if err != nil {
			print("Unable to make socket")
			panic(err)
		}

		sess, err := listener.Accept()
		if err != nil {
			print("Couldnt make Session")
		}
		fmt.Print("Connection made with ")
		fmt.Println(sess.RemoteAddr())

		finished := make(chan bool)

		stream1, err := sess.AcceptStream()
		if err != nil {
			fmt.Println("Couldnt make Stream 1")
		}
		go func() { handleStream(stream1, finished) }()

		// stream2, err := sess.AcceptStream()
		// if err != nil {
		// 	fmt.Println("Couldnt make Stream 2")
		// }
		// go func() { handleStream(stream2) }()

		// stream3, err := sess.AcceptStream()
		// if err != nil {
		// 	fmt.Println("Couldnt make Stream 3")
		// }
		// go func() { handleStream(stream3) }()

		// stream4, err := sess.AcceptStream()
		// if err != nil {
		// 	fmt.Println("Couldnt make Stream 4")
		// }
		// go func() { handleStream(stream4) }()

		<-finished
	}
}

func handleStream(stream quic.Stream, finished chan bool) error {
	size := 10000
	buff := make([]byte, size)

	for {
		n, err := stream.Read(buff)

		if n < size {
			buff[n] = 0
		}
		// fmt.Printf("%d : %s\n", n, string(buff[:n]))
		// fmt.Printf("%s", string(buff[:n]))
		if err == io.EOF || n == 0 {
			break
		}

	}

	finished <- true
	return nil
}

// Setup a bare-bones TLS config for the server
func generateTLSConfig() *tls.Config {
	key, err := rsa.GenerateKey(rand.Reader, 1024)
	if err != nil {
		panic(err)
	}
	template := x509.Certificate{SerialNumber: big.NewInt(1)}
	certDER, err := x509.CreateCertificate(rand.Reader, &template, &template, &key.PublicKey, key)
	if err != nil {
		panic(err)
	}
	keyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(key)})
	certPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: certDER})

	tlsCert, err := tls.X509KeyPair(certPEM, keyPEM)
	if err != nil {
		panic(err)
	}
	return &tls.Config{Certificates: []tls.Certificate{tlsCert}}
}
