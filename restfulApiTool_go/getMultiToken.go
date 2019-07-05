package main

import (
    "fmt"
    "restful"
    "sync"
)

var wg sync.WaitGroup
func getToken(token chan string, site, account, password string) {
    defer wg.Done()
    uap := &restful.Uap{
	    HostSite: site,
            ClientId: "REMOVE FOR CREDENTIAL",
	    ClientSecret: "REMOVE FOR CREDENTIAL",
    }
    uap.GetUserToken(account, password)
    token <- uap.UserToken
}

func printRes(token map[string]chan string) {
    defer wg.Done()
    siteNum := len(token)
    count := 0
    for {
        select {
	    case c := <-token["twmp"]:
		fmt.Printf("TW token: %s\n", c)
	    case c := <-token["usmp"]:
		fmt.Printf("US token: %s\n", c)
	    case c := <-token["sgmp"]:
		fmt.Printf("SG token: %s\n", c)
	    case c := <-token["eump"]:
		fmt.Printf("EU token: %s\n", c)
	    case c := <-token["cnmp"]:
		fmt.Printf("CN token: %s\n", c)
        }
	count++
	if count >= siteNum{
            break
	}
   }
}

func main() {
    tokenMap := map[string]chan string{
        "cnmp": make(chan string),
        "usmp": make(chan string),
        "twmp": make(chan string),
        "sgmp": make(chan string),
        "eump": make(chan string),
    }
    wg.Add(6)
    go getToken(tokenMap["twmp"], "mptw.com.tw", "twmp@test.com", "******")
    go getToken(tokenMap["usmp"], "mpus.com.tw", "usmp@test.com", "******")
    go getToken(tokenMap["sgmp"], "mpsg.com.tw", "sgmp@test.com", "******")
    go getToken(tokenMap["eump"], "mpeu.com.tw", "eump@test.com", "******")
    go getToken(tokenMap["cnmp"], "mpcm.com.tw", "cnmp@test.com", "******")
    go printRes(tokenMap)
    wg.Wait()
}
