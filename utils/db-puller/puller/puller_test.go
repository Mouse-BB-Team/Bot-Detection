package puller

import (
	"db-puller/puller/schema/event"
	"fmt"
	"github.com/go-pg/pg"
	"testing"
)

func TestPull(t *testing.T) {
	options := &pg.Options{
		Addr:     ":5432",
		User:     "admin",
		Password: "admin",
		Database: "data_collection",
	}

	puller := Puller{Options: options}
	puller.Connect()
	defer puller.Close()
	result := puller.Pull(event.EventType{Id: 1}, 1.0, 10)

	fmt.Println(result)
}
