package pkg

import (
	"os"
	"testing"
)

func Test_main(t *testing.T) {
	os.Setenv("SERVICE_ACCOUNT_TOKEN_FILE", "captainjackserviceaccount.json")
	defer os.Unsetenv("SERVICE_ACCOUNT_TOKEN_FILE")
	main()
}
